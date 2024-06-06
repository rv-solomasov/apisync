from ..parsers.parsers import BasicParser
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
        raw_type: str,  # ["text", "json"] removed Literal for old python
        json_searchpath: list = [],
        data: list = None,
        is_async: bool = False,
    ):
        self.__is_async = is_async
        self.parser = parser
        self.data = data or []
        self.raw_type = raw_type
        self.json_searchpath = json_searchpath

    def set_data(self, new_data=None):
        processed_data = self.process_data(new_data)
        if processed_data:
            if isinstance(processed_data, list):
                if self.data:
                    self.data.extend(processed_data)
                else:
                    self.data = processed_data
            elif isinstance(processed_data, dict):
                if self.data:
                    self.data.append(processed_data)
                else:
                    self.data = [processed_data]

    def process_data(self, new_data):
        temp_data = None
        if isinstance(new_data, list):
            temp_data = self.flatten_list_data(new_data)
        elif isinstance(new_data, dict):
            temp_data = self.extract_dict_data(new_data)

        return temp_data

    def get_data(self):
        return self.parser.parse(self.data)

    def is_async(self) -> bool:
        return self.__is_async

    def flatten_list_data(self, list_data):
        flat_list = []
        for item in list_data:
            if isinstance(item, list):
                flat_list.extend(self.flatten_list_data(item))
            else:
                flat_list.append(item)
        return flat_list

    def extract_dict_data(self, dict_data):
        temp_searchpath = self.json_searchpath[::-1]
        extracted_data = dict_data.copy()
        while len(temp_searchpath) > 0:
            extracted_data = extracted_data[temp_searchpath.pop()]
        return extracted_data


def create_output(output_type: str, **kwargs) -> BasicOutput:
    if output_type == "list":
        return ListOutput(**kwargs)
    else:
        raise ValueError(f"Unknown output type: {output_type}")
