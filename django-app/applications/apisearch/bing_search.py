from typing import Final 
import requests


class BingSearch:
  BING_API_KEY: Final[str] = "d41f5a72bb714999ad527a2863d922c7"
  BING_URL: Final[str] = "https://api.bing.microsoft.com/v7.0/search"
  search_results = {"engine": "Bing", "results": []}
  def __init__(self):
    pass

  def search(self, search_term:str, count: int= 10, **kwargs):
    headers = {"Ocp-Apim-Subscription-Key": self.BING_API_KEY}
    default_params = {
      "q": search_term,
      "count": count,
      "textDecorations": True,
      "textFormat": "HTML",
      "responseFileter":["Webpages"]
    }
    default_params.update(kwargs)
    try:
      response = requests.get(self.BING_URL, headers=headers, params=default_params)
      response.raise_for_status()
      pages_list= response.json()["webPages"]["value"]
      if pages_list:
        formated_response = [ {"title": page["name"], "url": page["url"]}  for page in pages_list]
        self.search_results.update( {"results": formated_response})
    except Exception as e:
      print(e)

  def get_search_results(self):
    return self.search_results


# bing_search = BingSearch()
# bing_search.search("Coffee")
# res = bing_search.get_search_results()
# print(res)