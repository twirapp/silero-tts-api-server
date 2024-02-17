from litestar.openapi.spec import Example

text_examples = [
    Example("ru_1", value="Съешьте ещё этих мягких французских булочек, да выпейте чаю."),
    Example("ru_2", value="В недрах тундры выдры в гетрах тырят в вёдра ядра кедров."),
    Example("en_1", value="Can you can a canned can into an un-canned can like a canner can can a canned can into an un-canned can?"),
]

speaker_examples = [
    Example("ru_aidar", value="aidar"),
    Example("ru_baya", value="baya"),
    Example("en_0", value="en_0"),
]

sample_rate_examples = [
    Example("8 000", value=8_000),
    Example("24 000", value=24_000),
    Example("48 000", value=48_000),
]
