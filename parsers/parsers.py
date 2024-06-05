from abc import ABC, abstractmethod


class BasicParser(ABC):
    @abstractmethod
    def parse(self):
        pass


class JSONParser(BasicParser):
    def __init__(self):
        pass

    def parse(self, data):
        return [{f"record_{i}": record} for i, record in enumerate(data)]


def create_parser(parser_type: str, **kwargs) -> BasicParser:
    if parser_type == "json":
        return JSONParser(**kwargs)
    else:
        raise ValueError(f"Unknown parser type: {parser_type}")
