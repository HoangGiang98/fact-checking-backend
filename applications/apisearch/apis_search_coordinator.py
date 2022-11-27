from bing_search import BingSearch
from google_search import GoogleSearch
from wiki_search import WikiSearch
from haystack.pipelines import Pipeline
from haystack.nodes import Crawler, PreProcessor
from haystack.document_stores import InMemoryDocumentStore

class ApisSearchCoordinator:
  wiki_search = WikiSearch()
  google_search = GoogleSearch()
  bing_search = BingSearch()
  search_results = {"engine": "Combined Engines", "results": []}

  def search(self,search_term:str):
    self.wiki_search.search(search_term)
    self.google_search.search(search_term)
    self.bing_search.search(search_term)
    wiki_result_list = self.wiki_search.get_search_results()["results"]
    bing_result_list = self.bing_search.get_search_results()["results"]
    google_result_list = self.google_search.get_search_results()["results"]
    self.search_results.update({"results": ApisSearchCoordinator.filter_unique_results_by_url([*wiki_result_list, *bing_result_list, *google_result_list]) })


  def get_unique_urls(self):
    return [ res["url"] for res in self.search_results["results"] ]

  def get_search_results(self):
    return self.search_results

  def filter_unique_results_by_url(results):
    # initializing Key 
    memo = set()
    unique_results = []
    for result in results:
      # testing for already present value
      if result["url"] not in memo:
        unique_results.append(result)
        # adding in memo if new value
        memo.add(result["url"])
    return unique_results


#Test
apiSearch = ApisSearchCoordinator()
# apiSearch.search("Coffee")
# # search_results = apiSearch.get_search_results()
# # print(search_results)
# # print(len(search_results["results"]))
# print("------")
# urls = apiSearch.get_unique_urls()
# print(len(urls))

# Only to test crawling and processing
apiSearch.wiki_search.search("Coffee")
urls = [res["url"] for res in apiSearch.wiki_search.get_search_results()["results"][0:2]]
print(urls)
crawler = Crawler(
    urls=urls,   # Websites to crawl
    crawler_depth=0,    # How many links to follow
    output_dir="crawled_files",  # The directory to store the crawled files, not very important, we don't use the files in this example
)

preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=False,
    split_by="passage",
    split_length=1,
    split_respect_sentence_boundary=False
)

document_store = InMemoryDocumentStore()

indexing_pipeline = Pipeline()
indexing_pipeline.add_node(component=crawler, name="crawler", inputs=['File'])
indexing_pipeline.add_node(component=preprocessor, name="preprocessor", inputs=['crawler'])
indexing_pipeline.add_node(component=document_store, name="document_store", inputs=['preprocessor'])

indexing_pipeline.run(params={"crawler": {'return_documents': True}})

print(document_store.get_document_count())