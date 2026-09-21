from agents import handle_query


def main():
    print("General-Purpose Assistant")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nYou: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            continue

        try:
            answer = handle_query(query)
            print(f"\nAssistant: {answer}")
        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
