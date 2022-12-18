from bing_search import BingSearch
from google_search import GoogleSearch
from wiki_search import WikiSearch
from haystack.pipelines import Pipeline
from haystack.nodes import FARMReader, Crawler, PreProcessor, TfidfRetriever
from haystack.document_stores import InMemoryDocumentStore
from enum import Enum


class Engines(Enum):
    GOOGLE = "Google"
    BING = "Bing"
    WIKI = "Wiki"
    COMBINED = "Combined Engines"


# TODO: rename the class for clarity


class ApisSearch:
    wiki_search = WikiSearch()
    google_search = GoogleSearch()
    bing_search = BingSearch()
    search_results = {"engine": Engines.COMBINED, "results": []}
    fact_check_results = {"query": "", "answers": []}
    document_store = InMemoryDocumentStore()

    def combined_search(self, search_term: str):
        self.google_search.search(search_term)
        self.bing_search.search(search_term)
        self.wiki_search.search(search_term)
        google_result_list = self.google_search.get_search_results()["results"]
        bing_result_list = self.bing_search.get_search_results()["results"]
        wiki_result_list = self.wiki_search.get_search_results()["results"]
        self.search_results.update(
            {
                "results": ApisSearch.filter_results_by_url(
                    [*google_result_list, *bing_result_list * wiki_result_list]
                )
            }
        )

    def engine_search(self, search_term: str, engine: Engines):
        match engine:
            case Engines.GOOGLE:
                self.google_search.search(search_term)
                google_result_list = self.google_search.get_search_results()[
                    "results"
                ]
                self.search_results.update(
                    {"engine": Engines.GOOGLE, "results": google_result_list}
                )
            case Engines.BING:
                self.bing_search.search(search_term)
                bing_result_list = self.bing_search.get_search_results()[
                    "results"
                ]
                self.search_results.update(
                    {"engine": Engines.BING, "results": bing_result_list}
                )
            case Engines.WIKI:
                self.wiki_search.search(search_term)
                wiki_result_list = self.wiki_search.get_search_results()[
                    "results"
                ]
                self.search_results.update(
                    {"engine": Engines.WIKI, "results": wiki_result_list}
                )
            case _:
                raise Exception("An invalid engine was passed as parameter")

    def get_urls(self):
        return [res["url"] for res in self.search_results["results"]]

    def filter_results_by_url(results):
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

    def crawl_preprocess(
        self, output_dir="crawled_files", split_by="passage", split_length=10
    ):
        crawler = Crawler(
            urls=self.get_urls(),  # Websites to crawl
            crawler_depth=0,  # How many links to follow
            output_dir=output_dir,  # The directory to store the crawled files, not very important, we don't use the files
            overwrite_existing_files=True,
        )
        preprocessor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=True,
            split_by=split_by,
            split_length=split_length,
            split_respect_sentence_boundary=(split_by == "word"),
        )
        indexing_pipeline = Pipeline()
        indexing_pipeline.add_node(
            component=crawler, name="crawler", inputs=["File"]
        )
        indexing_pipeline.add_node(
            component=preprocessor, name="preprocessor", inputs=["crawler"]
        )
        indexing_pipeline.add_node(
            component=self.document_store,
            name="document_store",
            inputs=["preprocessor"],
        )
        indexing_pipeline.run(params={"crawler": {"return_documents": True}})

    def fact_check_1(self, query: str):
        retriever = TfidfRetriever(self.document_store)
        reader = FARMReader(
            model_name_or_path="deepset/roberta-base-squad2-distilled"
        )
        query_pipeline = Pipeline()
        query_pipeline.add_node(
            component=retriever, name="retriever", inputs=["Query"]
        )
        query_pipeline.add_node(
            component=reader, name="reader", inputs=["retriever"]
        )
        self.fact_check_results = query_pipeline.run(query=query)

    def fact_check_2(self, query: str):
        pass

    def print_fact_check_1(self):
        print("\nQuestion: ", self.fact_check_results["query"])
        print("\nAnswers:")
        for answer in self.fact_check_results["answers"]:
            print("- ", answer.answer)
        print("\n")


# TODO: remove these tests
# Temporary test
# apiSearch = ApisSearch()
# apiSearch.combined_search("Coffee")
# search_results = apiSearch.search_results()
# print(search_results)
# print(len(search_results["results"]))
# urls = apiSearch.get_urls()
# print(len(urls))

# Only to test crawling and processing
# apiSearch.engine_search("Coffee", Engines.WIKI)
# urls = apiSearch.get_urls()
# print(urls)
# apiSearch.crawl_preprocess()
# print(apiSearch.document_store.get_document_count())
# print(apiSearch.document_store.describe_documents())

# Test retriever and reader
# apiSearch.fact_check_1("Drinking coffee is bad?")
# apiSearch.print_fact_check_1()
