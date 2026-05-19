import requests

def web_search(query: str):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"

    try:
        res = requests.get(url).json()

        if res.get("Abstract"):
            return res["Abstract"]

        if res.get("RelatedTopics"):
            return res["RelatedTopics"][0].get("Text", "No results found.")

        return "No useful results found."

    except Exception as e:
        return f"Search failed: {str(e)}"