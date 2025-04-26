import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import datetime
import openai
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def search_wegotused_inventory(make, model):
    base_url = "https://wegotused.com/our-inventory/"
    make_encoded = quote_plus(make.upper())
    model_encoded = quote_plus(model.upper())

    search_url = f"{base_url}?inv[yard]=all&inv[make]={make_encoded}&inv[model]={model_encoded}"
    print(f"🔗 Searching URL: {search_url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []

    if response.status_code != 200:
        print(f"❌ Failed to fetch inventory page. Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    if not table:
        print("❌ No inventory table found (maybe no matching cars).")
        return []

    rows = table.find_all('tr')[1:]  # Skip table header
    results = []

    for row in rows:
        cols = [col.text.strip() for col in row.find_all('td')]
        if len(cols) >= 9:
            result = {
                'yard': cols[0],
                'year': cols[1],
                'make': cols[2],
                'model': cols[3],
                'manufacturer': cols[4],
                'color': cols[5],
                'yard_date': cols[6],
                'row': cols[7],
                'vin': cols[8],
            }
            results.append(result)
    return results

def rank_and_display_top_matches(car_list, search_query):
    if not car_list:
        print("🚫 No cars to rank.")
        return

    car_text_list = ""
    for car in car_list:
        car_text_list += (
            f"- {car['year']} {car['make']} {car['model']} "
            f"({car['color']}) - Yard Date: {car['yard_date']}\n"
        )

    system_prompt = """
                        You are helping a user find the best matching car in a junkyard inventory.

                        The user will send you a list of cars and their details.

                        Your job:
                        - Pick the 3 best matches based on:
                            - Closest model year (+/- 5 years preferred)
                            - Similar color (exact match best)
                            - Newest yard date (prefer fresher arrivals)
                        - Assign a "Match Score" out of 100 for each pick.
                        - Output the top 3 cars as plain text, like:

                        1. 2011 Honda Civic (Black) - Yard Date: 04/10/2025 - Match Score: 95%
                        2. 2009 Honda Civic (Gray) - Yard Date: 03/15/2025 - Match Score: 88%
                        3. 2012 Honda Civic (Black) - Yard Date: 02/20/2025 - Match Score: 85%
                    """

    user_prompt = f"""
                    I am searching for: {search_query}

                    Here are the available cars:
                    {car_text_list}
                    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.2
        )

        print("\n🏆 Top 3 Recommended Cars:")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"❌ Failed to rank matches: {e}")
