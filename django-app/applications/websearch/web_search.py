from typing import List, Dict, Tuple, Union, Any

from .bing_search import BingSearch
from .google_search import GoogleSearch
from applications.utils.enums import Engines
from .wiki_search import WikiSearch
from applications.utils.nli_inference import NliInference
from applications.utils.evidence_selection import EvidenceSelection
from haystack.schema import Document
from haystack.nodes import Crawler

import json
import os
import shutil


CRAWLED_OUTPUT_DIR = "crawled_files"


class WebSearch:
    wiki_search = WikiSearch()
    google_search = GoogleSearch()
    bing_search = BingSearch()
    nli_infer = NliInference()
    evidence_selection = EvidenceSelection(num_docs=10)
    crawler = Crawler(
        crawler_depth=0,  # How many links to follow
        output_dir=CRAWLED_OUTPUT_DIR,  # The directory to store the crawled files, not very important, we don't use the files
        overwrite_existing_files=True,
    )

    def _engine_search(self, search_term: str, engine: Engines):
        if engine == Engines.GOOGLE:
            self.google_search.search(search_term)
            google_result_list = self.google_search.get_search_results()[
                "results"
            ]
            return {"engine": Engines.GOOGLE, "results": google_result_list}
        elif engine == Engines.BING:
            self.bing_search.search(search_term)
            bing_result_list = self.bing_search.get_search_results()["results"]
            return {"engine": Engines.BING, "results": bing_result_list}
        elif engine == Engines.WIKI:
            self.wiki_search.search(search_term)
            wiki_result_list = self.wiki_search.get_search_results()["results"]
            return {"engine": Engines.WIKI, "results": wiki_result_list}
        else:
            raise Exception("An invalid engine was passed as parameter")

    def _crawl(self, search_results: Dict) -> List[str]:
        if os.path.exists(CRAWLED_OUTPUT_DIR):
            # Delete crawled_files code
            shutil.rmtree(CRAWLED_OUTPUT_DIR)
        crawled_urls = [res["url"] for res in search_results["results"]]
        file_paths: List[str] = self.crawler.crawl(urls=crawled_urls)
        return file_paths

    def _load_docs(
        self, file_paths: List[str], search_results: Dict
    ) -> List[Document]:
        docs = []
        for _file in file_paths:
            with open(_file.absolute(), "r") as read_file:
                doc: Document = Document.from_dict(json.load(read_file))
                url: str = doc.meta["url"]
                doc.meta["title"] = next(
                    (
                        result["title"]
                        for result in search_results["results"]
                        if result["url"] == url
                    ),
                    None,
                )
                docs.append(doc)
        return docs

    def _retrieve_docs(
        self, claim: str, engine: Engines = Engines.GOOGLE
    ) -> List[Document]:
        search_results = self._engine_search(claim, engine)
        file_paths = self._crawl(search_results)
        docs = self._load_docs(file_paths, search_results)
        return docs

    async def webcheck(
        self, claim: str, engine: Engines = Engines.GOOGLE
    ) -> Dict:
        docs = self._retrieve_docs(claim, engine)
        evidence_docs = self.evidence_selection.retrieve_evidence_docs(
            docs, claim
        )
        response = self.nli_infer.predict_veracity(evidence_docs)
        return response
