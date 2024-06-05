from ..parsers.parsers import BasicParser
from typing import Literal
from abc import ABC, abstractmethod


class BasicOutput(ABC):
    @abstractmethod
    def is_async(self) -> bool:
        pass

    @abstractmethod
    def set_data(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class ListOutput(BasicOutput):
    def __init__(
        self,
        parser: BasicParser,
        raw_type: Literal["text", "json"],
        data: list = None,
        is_async: bool = False,
    ):
        self.__is_async = is_async
        self.parser = parser
        self.data = data or []
        self.raw_type = raw_type

    def set_data(self, new_data):
        self.data.extend(new_data)

    def get_data(self):
        return self.parser.parse(self.data)

    def is_async(self) -> bool:
        return self.__is_async


def create_output(output_type: str, **kwargs) -> BasicOutput:
    if output_type == "list":
        return ListOutput(**kwargs)
    else:
        raise ValueError(f"Unknown output type: {output_type}")
