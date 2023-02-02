from mediawiki import MediaWiki

class WikiSearch:
    wikipedia = MediaWiki(user_agent="factChecker-User-Agent")
    search_results = {"engine": "Wikipedia", "results": []}

    def __init__(self):
        pass

    def search(self, search_term: str, count: int = 10):
        try:
            reponse_list: list = self.wikipedia.opensearch(
                search_term, results=count
            )
            no_disambiguation_response: list = list(
                filter(
                    lambda res: (not "disambiguation" in res[0]), reponse_list
                )
            )
            if no_disambiguation_response:
                formated_response: list = [
                    {"title": res[0], "url": res[2]}
                    for res in no_disambiguation_response
                ]
                self.search_results.update({"results": formated_response})
        except Exception as e:
            print(e)

    def parse_results(self, results: list):
        try:
            pages_list: list = [
                self.wikipedia.page(res["title"]) for res in results
            ]
            return [
                {"title": p.title, "content": p.content, "url": p.url}
                for p in pages_list
            ]
        except Exception as e:
            print(e)

    def get_search_results(self):
        return self.search_results
