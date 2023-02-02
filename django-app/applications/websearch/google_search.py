from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Final


class GoogleSearch:
    GOOGLE_API_KEY: Final[str] = "AIzaSyBLbCeqGUdjmFgXE43PrUNOAlrVKIOsET0"
    GOOGLE_CSE_ID: Final[str] = "67d9a70a5f5ab4b62"
    search_results = {"engine": "Google", "results": []}

    def __init__(self):
        pass

    # Query parameters list: https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
    def search(self, search_term: str, **kwargs):
        service = build("customsearch", "v1", developerKey=self.GOOGLE_API_KEY)
        defautt_options = {
            "c2coff": "1",
            "fields": "items(title,formattedUrl)",
        }
        defautt_options.update(kwargs)
        try:
            response = (
                service.cse()
                .list(q=search_term, cx=self.GOOGLE_CSE_ID, **defautt_options)
                .execute()
            )
            pages_list = response["items"]
            if pages_list:
                formated_response = [
                    {"title": page["title"], "url": page["formattedUrl"]}
                    for page in pages_list
                ]
                self.search_results.update({"results": formated_response})
        except HttpError as e:
            print(e)

    def get_search_results(self):
        return self.search_results


# gg_search = GoogleSearch()
# res = gg_search.search("Coffee")

# print(res)
