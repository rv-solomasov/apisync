from apisync import create_pull


def main():
    test_engine = create_pull(
        static_url="https://api.restful-api.dev/objects",
        param_name="id",
        param_range=[1, 2, 3],
        api_type="rest",
        output_type="list",
        parser_type="json",
        response_type="json",
    )

    # Execute the engine to pull data from the API synchronously
    test_engine.execute()

    # Print the data collected by the output
    print(test_engine.show())


if __name__ == "__main__":
    main()
