import requests 
import json
from datetime import datetime, timedelta

TIBBER_TOKEN = "YOUR_TIBBER_API_TOKEN"
THINGSPEAK_WRITE_API_KEY = "YOUR_THINGSPEAK_WRITE-ID"
TIBBER_HOME_ID = "YOUR_TIBBER_HOME_ID"



#Fetch the data from the tibber API, see https://developer.tibber.com/docs/reference for more information.

def fetch_latest_hourly_consumption():
    url = "https://api.tibber.com/v1-beta/gql"
    headers = {
        "Authorization": f"Bearer {TIBBER_TOKEN}",
        "Content-Type": "application/json"
    }

    query = f"""
    {{
      viewer {{
        home(id: "{TIBBER_HOME_ID}") {{
          consumption(resolution: HOURLY, last: 1) {{
            nodes {{
              from
              to
              cost
              unitPrice
              unitPriceVAT
              consumption
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(url, headers=headers, json={"query": query})
    data = response.json()

    try:
        node = data["data"]["viewer"]["home"]["consumption"]["nodes"][0]
        print("Latest Hourly Data:")
        print(json.dumps(node, indent=2))
        return node
    except Exception as e:
        print("Failed to fetch data:", e)
        return None

#If the Data is fetched send it to Mathworks ThingSpeak channel, up to 8 fields of a channel can be populated with data.

def send_to_thingspeak(data):
    if not data:
        return

    payload = {
        "api_key": THINGSPEAK_WRITE_API_KEY,
        "field1": data["consumption"],
        "field2": data["cost"],
        "field3": data["unitPrice"],
        "field4": data["unitPriceVAT"],
    }

    r = requests.post("https://api.thingspeak.com/update", data=payload)
    if r.status_code == 200 and r.text != "0":
        print(f"Data sent to ThingSpeak. Entry ID: {r.text}")
    else:
        print("Failed to send data to ThingSpeak:", r.status_code, r.text)

if __name__ == "__main__":

    latest_data = fetch_latest_hourly_consumption()
    send_to_thingspeak(latest_data)
