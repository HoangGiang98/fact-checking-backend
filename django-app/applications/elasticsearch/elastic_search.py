import unicodedata
from typing import List, Dict, Tuple, Union, Any
from applications.utils.nli_inference import NliInference
from applications.elasticsearch.retriever import get_top_k_docs, get_query
from applications.utils.evidence_selection import EvidenceSelection
from haystack.schema import Document


class ElasticSearch:
    nli_infer = NliInference()
    evidence_selection = EvidenceSelection(num_docs=10)

    def _load_docs(self, top_k_docs: List[Document]) -> List[Document]:
        docs = []
        for doc in top_k_docs:
            title = doc.meta["meta"]["name"]
            doc.meta["title"] = title

            url = f"https://en.wikipedia.org/wiki/{title}"
            doc.meta["url"] = url
            docs.append(doc)
        return docs

    def _retrieve_docs(self, claim: str) -> List[Document]:
        top_k_docs = get_top_k_docs(claim)["documents"]
        docs = self._load_docs(top_k_docs)
        return docs

    async def elastic_bertcheck(self, claim: str) -> Dict:
        docs = self._retrieve_docs(claim)
        evidence_docs = self.evidence_selection.retrieve_evidence_docs(
            docs, claim
        )
        response = self.nli_infer.predict_veracity(evidence_docs)
        return response

    async def elastic_dprcheck(self, question: str) -> List:
        answers = get_query(question)
        return answers
