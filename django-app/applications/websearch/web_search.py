from typing import List, Dict, Tuple, Union, Any

from .enums import Engines
from .bing_search import BingSearch
from .google_search import GoogleSearch
from .wiki_search import WikiSearch
from .nli_inference import NliInference

from haystack.pipelines import  DocumentSearchPipeline
from haystack.schema import Document
from haystack.nodes import Crawler, PreProcessor,EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore
import json
import os
import shutil 

INMEMORY_DOCUMENT_STORE = InMemoryDocumentStore(similarity= "cosine", duplicate_documents= "skip", embedding_dim = 384)
class WebSearch:
  wiki_search = WikiSearch()
  google_search = GoogleSearch()
  bing_search = BingSearch()
  nli_infer = NliInference()
  search_results = {"engine": Engines.COMBINED, "results": []}
  
  retriever = EmbeddingRetriever(
    document_store= INMEMORY_DOCUMENT_STORE,
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    model_format="sentence_transformers",
  )

  def _engine_search(self, search_term:str, engine: Engines):
    if engine == Engines.GOOGLE:
      self.google_search.search(search_term)
      google_result_list = self.google_search.get_search_results()["results"]
      self.search_results.update({"engine": Engines.GOOGLE,"results": google_result_list})
      return
    elif engine == Engines.BING:
      self.bing_search.search(search_term)
      bing_result_list = self.bing_search.get_search_results()["results"]
      self.search_results.update({"engine": Engines.BING,"results": bing_result_list})
      return
    elif engine == Engines.WIKI:
      self.wiki_search.search(search_term)
      wiki_result_list = self.wiki_search.get_search_results()["results"]
      self.search_results.update({"engine": Engines.WIKI,"results": wiki_result_list})
      return
    else:
      raise Exception("An invalid engine was passed as parameter")

  def get_urls(self):
    return [ res["url"] for res in self.search_results["results"] ]

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
  
  def crawl(self, output_dir= "crawled_files") -> List[str]:
    if os.path.exists(output_dir):
      # Delete crawled_files code
      shutil.rmtree(output_dir)
    crawler = Crawler(
      urls=self.get_urls(),   # Websites to crawl
      crawler_depth=0,    # How many links to follow
      output_dir=output_dir,  # The directory to store the crawled files, not very important, we don't use the files
      overwrite_existing_files= True 
    )
    file_paths:List[str]  = crawler.crawl()
    return file_paths

  def _load_docs(self, file_paths: List[str]) -> List[Document]:
    docs = []
    for _file in file_paths:
      with open(_file.absolute(), "r") as read_file:
        doc: Document = Document.from_dict(json.load(read_file))
        url:str = doc.meta["url"]
        doc.meta["title"] = next((result["title"] for result in self.search_results["results"] if result["url"] == url), None)
        docs.append(doc)
    return docs

  def _preprocess(self, docs: List[Document], split_by = "sentence", split_length= 1):
    preprocessor = PreProcessor(
      clean_empty_lines=True,
      clean_whitespace=True,
      clean_header_footer=True,
      remove_substrings="\n",
      split_by=split_by,
      split_length= split_length,
      split_overlap=0,
      split_respect_sentence_boundary= (split_by =="word"),
    )
    # select only documents with at least 10 words. Otherwise, the documents are not very informative
    preprocessed_docs: list = []
    for doc in preprocessor.process(docs):
      content = doc.content
      if len(content.split())>=10 and not(content.startswith('","description":"')):
        preprocessed_docs.append(doc)
    return preprocessed_docs

  def _retrieve_preprocessed_docs(self, claim:str, engine: Engines = Engines.GOOGLE):
    self._engine_search(claim, engine)
    file_paths = self.crawl()
    docs = self._load_docs(file_paths)
    return self._preprocess(docs)

  def _retrieve_evidence_docs(self, preprocessed_docs: list, claim:str):
    INMEMORY_DOCUMENT_STORE.delete_documents()
    INMEMORY_DOCUMENT_STORE.write_documents(preprocessed_docs)
    INMEMORY_DOCUMENT_STORE.update_embeddings(self.retriever)
    pipeline = DocumentSearchPipeline(self.retriever)
    return pipeline.run(claim, params={"Retriever": {"top_k": 10}})

  async def fact_check_claim(self, claim:str, engine: Engines = Engines.GOOGLE):
    preprocessed_docs = self._retrieve_preprocessed_docs(claim, engine)
    evidence_docs = self._retrieve_evidence_docs(preprocessed_docs, claim)
    response = self.nli_infer.predict_veracity(evidence_docs)
    return response

  
# TODO: remove these tests 
# Temporary test 
# web_search = WebSearch()
# web_search.combined_search("Coffee")
# search_results = web_search.search_results()
# print(search_results)
# print(len(search_results["results"]))
# urls = web_search.get_urls()
# print(len(urls))

# Only to test crawling and processing
# web_search._engine_search("Drinking coffee is bad?", Engines.BING)
# urls = web_search.get_urls()
# print(urls)
# web_search.crawl_preprocess()
# print(web_search.document_store.get_document_count())
# print(web_search.document_store.describe_documents())

# Test retriever and reader
# web_search.fact_check_1("Drinking coffee is bad?")
# web_search.print_fact_check_1()

# Test sentence bert
# web_search = WebSearch()
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# future = asyncio.ensure_future(web_search.fact_check_claim("Germany is in the European Union", Engines.BING))
# loop.run_until_complete(future)
# response = future.result()
# print(response)
#print_documents(result, max_text_len=1000, print_name=True, print_meta=True)


