from ..outputs.outputs import BasicOutput
import aiohttp
import asyncio

from abc import ABC, abstractmethod


class BasicEngine(ABC):

    @abstractmethod
    async def check_auth(self) -> bool:
        pass

    @abstractmethod
    async def gather_tasks(self):
        pass

    @abstractmethod
    async def define_task(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def show(self):
        pass


class RestEngine(BasicEngine):
    def __init__(
        self,
        static_url: str,
        param_name: str,
        param_range: list,
        output: BasicOutput,
        concurrency: int = 5,
    ):
        self.static_url = static_url
        self.param_name = param_name
        self.param_range = param_range
        self.concurrency = concurrency
        self.output = output

    async def gather_tasks(self):
        async with aiohttp.ClientSession() as session:
            semaphore = asyncio.Semaphore(self.concurrency)
            if not self.output.is_async():
                lock = asyncio.Lock()
            else:
                lock = None
            tasks = [
                self.define_task(param_value, semaphore, lock, session)
                for param_value in self.param_range
            ]
            await asyncio.gather(*tasks)

    async def define_task(self, param_value, semaphore, lock, session):
        async with semaphore:
            async with session.get(
                self.static_url, params={self.param_name: param_value}
            ) as response:
                if response.status == 200:
                    if self.output.raw_type == "text":
                        new_data = await response.text()
                    else:
                        new_data = await response.json()
                if (lock is not None) and new_data:
                    async with lock:
                        self.output.set_data(new_data)
                elif new_data:
                    self.output.set_data(new_data)

    async def check_auth(self, session):
        async with session.get(self.static_url) as check_response:
            return check_response.status == 200

    def execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.gather_tasks())

    def show(self):
        return self.output.get_data()


class MultiRestEngine(BasicEngine):
    def __init__(
        self,
        url_list: list,
        output: BasicOutput,
        concurrency: int = 5,
        request_kwargs: dict = {},
    ):
        self.url_list = url_list
        self.concurrency = concurrency
        self.output = output
        self.request_kwargs = request_kwargs

    async def gather_tasks(self):
        async with aiohttp.ClientSession() as session:
            semaphore = asyncio.Semaphore(self.concurrency)
            if not self.output.is_async():
                lock = asyncio.Lock()
            else:
                lock = None
            tasks = [
                self.define_task(url, semaphore, lock, session) for url in self.url_list
            ]
            await asyncio.gather(*tasks)

    async def define_task(self, url, semaphore, lock, session):
        async with semaphore:
            new_data = None
            async with session.get(url, **self.request_kwargs) as response:
                if response.status == 200:
                    if self.output.raw_type == "text":
                        new_data = await response.text()
                    else:
                        new_data = await response.json()
                if (lock is not None) and new_data:
                    async with lock:
                        self.output.set_data(new_data)
                elif new_data:
                    self.output.set_data(new_data)

    async def check_auth(self, session):
        async with session.get(
            self.url_list[0], **self.request_kwargs
        ) as check_response:
            return check_response.status == 200

    def execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.gather_tasks())

    def show(self):
        return self.output.get_data()


def create_engine(engine_type: str, **kwargs) -> BasicEngine:
    if engine_type == "rest":
        return RestEngine(**kwargs)
    elif engine_type == "multi_rest":
        return MultiRestEngine(**kwargs)
    else:
        raise ValueError(f"Unknown engine type: {engine_type}")
