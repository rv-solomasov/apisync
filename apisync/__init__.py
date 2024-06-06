from .engines.engines import BasicEngine, create_engine
from .parsers.parsers import create_parser
from .outputs.outputs import create_output


def create_pull(
    api_type: str,
    output_type: str,
    parser_type: str,
    response_type: str,
    engine_kwargs: dict = {},
    output_kwargs: dict = {},
    parser_kwargs: dict = {},
) -> BasicEngine:
    return create_engine(
        engine_type=api_type,
        output=create_output(
            output_type=output_type,
            parser=create_parser(parser_type=parser_type, **parser_kwargs),
            raw_type=response_type,
            **output_kwargs
        ),
        **engine_kwargs
    )
