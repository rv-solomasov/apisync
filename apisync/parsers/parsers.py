from abc import ABC, abstractmethod
import pandas as pd


class BasicParser(ABC):
    @abstractmethod
    def parse(self):
        pass


class JSONParser(BasicParser):
    def __init__(self):
        pass

    def parse(self, data):
        return [{f"record_{i}": record} for i, record in enumerate(data)]


class PandasParser(BasicParser):
    def __init__(self):
        pass

    def parse(self, data):
        try:
            return pd.DataFrame(data)
        except:
            raise ValueError("Cannot convert to a dataframe")


class DummyParser(BasicParser):
    def __init__(self):
        pass

    def parse(self, data):
        return data


def create_parser(parser_type: str, **kwargs) -> BasicParser:
    if parser_type == "json":
        return JSONParser(**kwargs)
    elif parser_type == "pandas":
        return PandasParser(**kwargs)
    elif parser_type == "dummy":
        return DummyParser(**kwargs)
    else:
        raise ValueError(f"Unknown parser type: {parser_type}")
