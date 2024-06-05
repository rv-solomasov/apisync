from .engines.engines import BasicEngine, create_engine
from .parsers.parsers import create_parser
from .outputs.outputs import create_output


def create_pull(
    static_url: str,
    param_name: str,
    param_range: list,
    api_type: str,
    output_type: str,
    parser_type: str,
    response_type: str,
) -> BasicEngine:
    return create_engine(
        engine_type=api_type,
        output=create_output(
            output_type=output_type,
            parser=create_parser(parser_type=parser_type),
            raw_type=response_type,
        ),
        static_url=static_url,
        param_name=param_name,
        param_range=param_range,
    )
