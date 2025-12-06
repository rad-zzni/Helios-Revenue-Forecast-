from spoon_ai import ChatBot
import requests
import json
import os

API_KEY = os.getenv("SPOONOS_API_KEY", "dev-key")  # Set in your environment

def fetch_data():
    forecast = requests.get("http://localhost:3001/forecast").json()
    summary = requests.get("http://localhost:3001/analysis_input").json()
    return forecast, summary["analysis_input"]

def analyze_with_llm(forecast, analysis_input):
    bot = ChatBot()
    prompt = f"""
    You are the Helios Scientific Analyzer.

    Forecast data:
    {json.dumps(forecast, indent=2)}

    Summary:
    {analysis_input}

    Provide deeper insights:
    - expected yield pattern
    - risk factors
    - recommended maintenance window
    - uncertainty interpretation
    """
    return bot.chat(prompt)

def publish_hash_to_backend():
    # Step 1: get hash
    resp = requests.get("http://localhost:3001/hash_forecast").json()
    hash_value = resp["hash"]

    # Step 2: publish
    publish_resp = requests.post(
        "http://localhost:3001/publish_hash",
        json={"hash": hash_value, "apiKey": API_KEY}
    ).json()

    return publish_resp

def main():
    forecast, analysis_input = fetch_data()
    insights = analyze_with_llm(forecast, analysis_input)
    print("\n=== INSIGHTS ===\n")
    print(insights)

    # Uncomment this when you actually want to publish:
    # pub = publish_hash_to_backend()
    # print("\n=== HASH PUBLISHED ===\n", pub)

if __name__ == "__main__":
    main()