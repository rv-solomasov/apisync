# apisync

apisync is a Python library that provides a wrapper for asynchronous calls to an API. It simplifies the process of making asynchronous requests to APIs by allowing users to specify a static URL, a variable parameter, and providing built-in capabilities to develop custom pulling engines, output types, and parsers applied to the fetched data.

## Features

- Asynchronous execution: apisync leverages asyncio to perform asynchronous API requests, allowing for improved performance and efficiency.
- Custom pulling engines: Users can develop their own pulling engines to control the behavior of API requests, such as defining concurrency settings and handling response data.
- Flexible output types: apisync supports various output types, including built-in Python types (e.g., lists, dictionaries), files (e.g., CSV, JSON), and databases, providing flexibility in how fetched data is processed and stored.
- Extensible parser functionality: Users can define custom parsers to process and transform fetched data according to their specific requirements.
