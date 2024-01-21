import re
import wave
import torch
import warnings
import contextlib
import xml.etree.ElementTree as ET


class TTSModelMultiAcc_v3():
    def __init__(self, model_path, symbols, speaker_to_id, symb_ascii_dict={}, emb_dim=128):
        torch.set_grad_enabled(False)
        self.model = self.init_jit_model(model_path)
        self.symbols = symbols
        self.device = torch.device('cpu')
        self.speaker_to_id = speaker_to_id
        self.speakers = list(speaker_to_id.keys())
        self.symb_ascii_dict = symb_ascii_dict

        # ssml tags
        self.strength2time = {'x_weak': 25, 'weak': 75, 'medium': 150, 'strong': 300, 'x-strong': 1000}
        self.rate2value = {'x-slow': 0.5, 'slow': 0.8, 'medium': 1., 'fast': 1.2, 'x-fast': 1.5}
        self.pitch2value = {'x-low': 0.6, 'low': 0.8, 'medium': 1., 'high': 1.2, 'x-high': 1.4, 'robot': 0.}
        self.emb_dim = emb_dim

        self.random_emb = None
        self.debug = False

        self.valid_tags = {'break': {'strength': list(self.strength2time.keys())},
                           'prosody': {'rate': list(self.rate2value.keys()),
                                       'pitch': list(self.pitch2value.keys())}}
        self.q_model_unpacked = False

    def init_jit_model(self, model_path: str):
        torch.set_grad_enabled(False)
        model = torch.jit.load(model_path, map_location='cpu')
        model.eval()
        return model

    def symb_to_ascii(self, sentence):
        ascii_list = [self.symb_ascii_dict.get(s, s) for s in sentence]
        ascii_text = ''.join(ascii_list)
        return ascii_text

    def prepare_text_input(self, text):

        text = text.lower()
        text = text.replace('—', '–').replace('–', '–').replace('‑', '-')
        text = re.sub(r'[^{}]'.format(self.symbols[3:]), '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        sentence = self.symb_to_ascii(text)

        clean_sentence = re.sub(r'[^a-z1-9\- ]', '', sentence)
        has_text = len(clean_sentence.replace(' ', '')) > 0
        return sentence, clean_sentence, has_text

    def prepare_tts_model_input(self, text: str,
                                ssml: bool,
                                speaker_ids: list):
        if ssml:
            clean_text_list = self.process_ssml(text)
        else:
            clean_text_list = self.process_simple_text(text)

        sentences, clean_sentences, break_lens, prosody_rates, prosody_pitches = map(list, zip(*map(dict.values, clean_text_list)))
        full_text_len = sum([len(s) for s in sentences])
        if full_text_len > 1000:
            warnings.warn('Text string is longer than 1000 symbols.')

        speaker_ids = torch.LongTensor(speaker_ids)
        return sentences, clean_sentences, break_lens, prosody_rates, prosody_pitches, speaker_ids

    def to(self, device):
        self.model.tts_model = self.model.tts_model.to(device)
        self.device = device

    def get_speakers(self, speaker: str, voice_path=None):
        try:
            if speaker == 'random':
                self.load_random_voice(voice_path)
            speaker_id = self.speaker_to_id.get(speaker, None)
            if speaker_id is None:
                raise ValueError(f"`speaker` should be in {', '.join(self.speakers)}")
        except Exception as e:
            raise ValueError(f'Failed to load speaker: {speaker}, error: {e}')
        return [speaker_id]

    def process_simple_text(self, text):
        sentence, clean_sentence, has_text = self.prepare_text_input(text)
        if not has_text:
            raise ValueError
        simple_text_dict = [{'text': sentence,
                             'clean_text': clean_sentence,
                             'break_time': None,
                             'prosody_rate': 1.,
                             'prosody_pitch': 1.}]
        return simple_text_dict

    def process_ssml(self, ssml_text):
        ssml_text = re.sub(r'\s+', ' ', ssml_text).strip().replace('\n ', '\n')
        try:
            root = ET.fromstring(ssml_text)
        except Exception:
            raise ValueError("Invalid XML format")
        assert root.tag == 'speak', "Invalid SSML format: <speak> tag is essential"
        try:
            ssml_parsed = self.process_ssml_element(root)
            if self.debug:
                print(ssml_parsed)
        except AssertionError as ae:
            raise ae
        except Exception as e:
            raise ValueError(f"Failed to parse SSML: {e}")
        try:
            clean_text_list = self.process_ssml_tag_dict(ssml_parsed)
            if self.debug:
                print(clean_text_list)
        except Exception as e:
            raise ValueError(f"Failed to process SSML: {e}")
        return clean_text_list

    def process_ssml_tag_dict(self, text_break_list):
        proc_text_break_list = []
        for i, text_break_prosody in enumerate(text_break_list):
            tbreak = text_break_prosody['break']
            tprosody = text_break_prosody['prosody']
            text, clean_text, has_text = self.prepare_text_input(text_break_prosody['text'])
            break_time = int(tbreak['time']/12.5) if tbreak['time'] is not None else None
            if has_text or i == 0:
                text = self.check_text_break(text, tbreak)
                proc_text_break_list.append({'text': text,
                                             'clean_text': clean_text,
                                             'break_time': break_time,
                                             'prosody_rate': tprosody['rate'],
                                             'prosody_pitch': tprosody['pitch']})
            elif tbreak['strength'] is not None and len(proc_text_break_list) > 0:
                text = self.check_text_break(proc_text_break_list[-1]['text'], tbreak)
                proc_text_break_list[-1]['text'] = text
                if proc_text_break_list[-1]['break_time'] is None:
                    proc_text_break_list[-1]['break_time'] = break_time
                else:
                    proc_text_break_list[-1]['break_time'] = max(break_time, proc_text_break_list[-1]['break_time'])
        return proc_text_break_list

    def check_text_break(self, text, tbreak):
        if len(text) == 0 or tbreak['strength'] is not None and text[-1] not in '!,-.:;?–…':  # TODO fx dash
            text = text + '.'
        return text

    def process_ssml_element(self, element, def_strength='strong', def_rate=1., def_pitch=1.):
        parsed = []
        last_tag = None
        head_text_parsed = self.process_head_tail_text(element.text, def_rate, def_pitch)
        parsed.extend(head_text_parsed)

        for child in element:
            if child.tag == 'break':
                break_strength, break_ts = self.process_break_attrib(child.attrib)
                if len(parsed) == 0:
                    parsed.append({'text': '.',
                                   'break': {'strength': None,
                                             'time': None},
                                   'prosody': {'rate': def_rate,
                                               'pitch': def_pitch}})
                parsed[-1]['break'] = {'strength': break_strength,
                                       'time': break_ts}

            elif child.tag == 'prosody':
                prosody_rate, prosody_pitch, change_rate, change_pitch = self.process_prosody(child.attrib)
                child_rate = prosody_rate if change_rate else def_rate
                child_pitch = prosody_pitch if change_pitch else def_pitch
                child_parsed = self.process_ssml_element(child, def_strength, child_rate, child_pitch)
                parsed.extend(child_parsed)

            elif child.tag in ['p', 's']:
                break_strength = 'strong' if child.tag == 's' else 'x-strong'
                child_parsed = self.process_ssml_element(child, break_strength, def_rate, def_pitch)
                if len(parsed) > 0 and (parsed[-1]['text'] or last_tag is not None or last_tag != child.tag):
                    if parsed[-1]['break']['strength'] is None:
                        parsed[-1]['break'] = {'strength': break_strength,
                                               'time': self.strength2time[break_strength]}
                    else:
                        last_time = parsed[-1]['break']['time']
                        parsed[-1]['break'] = {'strength': break_strength,
                                               'time': max(last_time, self.strength2time[break_strength])}
                if len(child_parsed) > 0:
                    if child_parsed[-1]['break']['strength'] is None:
                        child_parsed[-1]['break'] = {'strength': break_strength,
                                                     'time': self.strength2time[break_strength]}
                    else:
                        last_time = child_parsed[-1]['break']['time']
                        child_parsed[-1]['break'] = {'strength': break_strength,
                                                     'time': max(last_time, self.strength2time[break_strength])}
                    parsed.extend(child_parsed)
            else:
                warnings.warn(f"Current model doesn't support SSML tag: {child.tag}")

            last_tag = child.tag

            if child.tail:
                tail_text = child.tail
                if tail_text[0] in '.,!?…–;:' and len(parsed) > 0:
                    lost_punct = tail_text[0]
                    parsed[-1]['text'] = parsed[-1]['text'].strip() + lost_punct
                    if len(tail_text) > 1:
                        tail_text = tail_text[1:]
                tail_text_parsed = self.process_head_tail_text(tail_text, def_rate, def_pitch)
                parsed.extend(tail_text_parsed)
        return parsed

    def process_head_tail_text(self, element_text, def_rate, def_pitch):
        text_parsed = []
        if element_text is None:
            return text_parsed
        proc_text = element_text.replace('\n', '')
        proc_text = re.sub(r'\s+', ' ', proc_text).strip()
        text_parsed.append({'text': proc_text,
                            'break': {'strength': None,
                                      'time': None},
                            'prosody': {'rate': def_rate,
                                        'pitch': def_pitch}})
        return text_parsed

    def process_break_attrib(self, attrib):
        for k in attrib.keys():
            if k not in ['strength', 'time']:
                warnings.warn(f"Current model doesn't support SSML <break> attrib: {k}")
        strength = attrib.get('strength', 'medium')
        break_time = attrib.get('time', None)
        if break_time is not None:
            if break_time.endswith('ms'):
                break_ts = int(break_time[:-2])
            elif break_time.endswith('s'):
                break_ts = int(break_time[:-1]) * 1000
            else:
                raise AssertionError("Invalid <break> tag, time should end with 'ms' or 's'")

            if break_ts >= self.strength2time['x-strong']:
                strength = 'x-strong'
            elif break_ts >= self.strength2time['strong']:
                strength = 'strong'
        else:
            if strength in self.strength2time:
                break_ts = self.strength2time[strength]
            else:
                raise AssertionError(f"Invalid <break> tag, strength should be in {', '.join(self.valid_tags['break']['strength'])}")
        if break_ts > 5000:
            warnings.warn('Cuurent model supports pauses less than 5 sec')
            break_ts = 5000
        return strength, break_ts

    def process_prosody(self, attrib):
        for k in attrib.keys():
            if k not in ['rate', 'pitch']:
                warnings.warn(f"Current model doesn't support SSML <prosody> attrib: {k}")
        rate = attrib.get('rate', None)
        pitch = attrib.get('pitch', None)
        assert rate is not None or pitch is not None, "Empty <prosody> tag"
        if rate is not None:
            change_rate = True
            if rate.endswith('%'):
                rate_val = int(rate.replace('%', '')) / 100
            else:
                rate_val = self.rate2value.get(rate, None)
                if rate_val is None:
                    raise AssertionError(f"Invalid <prosody> tag, rate should be in {', '.join(self.valid_tags['prosody']['rate'])}")
        else:
            change_rate = False
            rate_val = 1.
        if pitch is not None:
            change_pitch = True
            if pitch.endswith('%'):
                pitch_val = int(pitch.replace('%', '')[1:]) / 100
                if pitch[0] == '+':
                    pitch_val = 1. + pitch_val
                else:
                    pitch_val = 1. - pitch_val
            else:
                pitch_val = self.pitch2value.get(pitch, None)
                if pitch_val is None:
                    raise AssertionError(f"Invalid <prosody> tag, pitch should be in {', '.join(self.valid_tags['prosody']['pitch'])}")
        else:
            change_pitch = False
            pitch_val = 1.
        return rate_val, pitch_val, change_rate, change_pitch

    def transform_durs_to_ssml(self, text, symbol_durs):
        for s, dur in symbol_durs.items():
            text = text.replace(s, f'{s}<break time="{dur}ms"/>')
        text = '<speak>' + text + '</speak>'
        return text

    def apply_tts(self, text=None,
                  ssml_text=None,
                  speaker: str = 'xenia',
                  sample_rate: int = 48000,
                  put_accent=True,
                  put_yo=True,
                  voice_path=None,
                  symbol_durs=None):

        assert sample_rate in [8000, 24000, 48000], f"`sample_rate` should be in [8000, 24000, 48000], current value is {sample_rate}"
        assert speaker in self.speakers, f"`speaker` should be in {', '.join(self.speakers)}"
        assert text is not None or ssml_text is not None, "Both `text` and `ssml_text` are empty"
        assert symbol_durs is None or ssml_text is None, '`ssml_text` and `symbol_durs` are not compatible'

        if symbol_durs is not None:
            ssml_text = self.transform_durs_to_ssml(text, symbol_durs)

        ssml = ssml_text is not None
        if ssml:
            input_text = ssml_text
        else:
            input_text = text
        speaker_ids = self.get_speakers(speaker, voice_path)
        sentences, clean_sentences, break_lens, prosody_rates, prosody_pitches, sp_ids = self.prepare_tts_model_input(input_text,
                                                                                                                      ssml=ssml,
                                                                                                                      speaker_ids=speaker_ids)

        if not self.q_model_unpacked:
            self.unpack_q_model()
            self.q_model_unpacked = True

        with torch.no_grad():
            try:
                model_kwargs = {'sentences': sentences,
                                'clean_sentences': clean_sentences,
                                'break_lens': break_lens,
                                'prosody_rates': prosody_rates,
                                'prosody_pitches': prosody_pitches,
                                'speaker_ids': sp_ids,
                                'sr': sample_rate,
                                'device': str(self.device)}
                if self.model.set_accent:
                    model_kwargs['put_yo'] = put_yo
                    model_kwargs['put_accent'] = put_accent

                out, out_lens = self.model(**model_kwargs)
            except RuntimeError:
                raise Exception("Model couldn't generate your text, probably it's too long")
        audio = out.to('cpu')[0]
        return audio

    @staticmethod
    def write_wave(path, audio, sample_rate):
        """Writes a .wav file.
        Takes path, PCM audio data, and sample rate.
        """
        with contextlib.closing(wave.open(path, 'wb')) as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio)

    def save_wav(self, text=None,
                 ssml_text=None,
                 speaker: str = 'xenia',
                 audio_path: str = '',
                 sample_rate: int = 48000,
                 put_accent=True,
                 put_yo=True):

        if not audio_path:
            audio_path = 'test.wav'

        audio = self.apply_tts(text=text,
                               ssml_text=ssml_text,
                               speaker=speaker,
                               sample_rate=sample_rate,
                               put_yo=put_yo,
                               put_accent=put_accent)
        self.write_wave(path=audio_path,
                        audio=(audio * 32767).numpy().astype('int16'),
                        sample_rate=sample_rate)
        return audio_path

    def load_random_voice(self, voice_path=None):
        if voice_path is None:
            random_emb = torch.randn(2, self.emb_dim, requires_grad=False).to(self.device)
            self.random_emb = random_emb
            print("Generated new voice")
        else:
            random_emb = torch.load(voice_path, map_location=self.device)
            print(f"Loaded voice from {voice_path}")
            if self.random_emb is not None and torch.equal(self.random_emb, random_emb):
                return
        mel_weight = random_emb[0]
        dur_weight = random_emb[1, :self.emb_dim//2]
        p_weight = random_emb[1, self.emb_dim//2:]

        self.model.tts_model.tacotron.speaker_embedding.weight[-1] = mel_weight
        self.model.tts_model.dur_predictor.dur_pred.speaker_embedding.weight[-1] = dur_weight
        self.model.tts_model.pitch_predictor.pitch_pred.speaker_embedding.weight[-1] = p_weight

    def save_random_voice(self, voice_path):
        assert self.random_emb is not None, "No generated random voice"
        torch.save(self.random_emb, voice_path)
        print(f"Saved generated voice to {voice_path}")

    def unpack_q_model(self):
        if self.model.set_accent:
            quantized_weight = self.model.accentor.embedding.weight.data.clone()
            restored_weights = self.model.accentor.scale * (quantized_weight - self.model.accentor.zero_point)
            self.model.accentor.embedding.weight.data = restored_weights
