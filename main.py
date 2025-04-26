import os
from dotenv import load_dotenv
from interpreter import interpreter_query
from search_inventory import search_wegotused_inventory, rank_and_display_top_matches
import openai

def main():
    load_dotenv()

    print("What car part are you looking for? I need the part and year please!")
    user_input = input("> ")

    try:
        query = interpreter_query(user_input)

        print("\n🔍 Interpreted your query as:")
        print(f"  Year:  {query.get('year', '[Not provided]')}")
        print(f"  Make:  {query['make']}")
        print(f"  Model: {query['model']}")
        print(f"  Part:  {query['part']}")

        cars = search_wegotused_inventory(query['make'], query['model'])

        if not cars:
            print("🚫 No matching cars found in the yard.")
            return

        rank_and_display_top_matches(cars, f"{query.get('year', '')} {query['make']} {query['model']} {query['part']}")

    except Exception as e:
        print(f"❌ Error interpreting input: {e}")

if __name__ == "__main__":
    main()
