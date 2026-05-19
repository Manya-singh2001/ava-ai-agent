import requests

def get_weather(city: str):
    try:
        url = f"https://wttr.in/{city}?format=3"
        res = requests.get(url)

        return res.text

    except Exception as e:
        return f"Weather fetch failed: {str(e)}"