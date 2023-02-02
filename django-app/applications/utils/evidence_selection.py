from typing import List
from haystack.pipelines import DocumentSearchPipeline
from haystack.schema import Document
from haystack.nodes import PreProcessor, EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore


class EvidenceSelection:
    num_docs = 10

    def __init__(self, num_docs):
        self.num_docs = num_docs

    inmemory_doc_store = InMemoryDocumentStore(
        similarity="cosine", duplicate_documents="skip", embedding_dim=384
    )
    retriever = EmbeddingRetriever(
        document_store=inmemory_doc_store,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        model_format="sentence_transformers",
    )

    def _preprocess(
        self, docs: List[Document], split_by="sentence", split_length=1
    ):
        preprocessor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=True,
            remove_substrings="\n",
            split_by=split_by,
            split_length=split_length,
            split_overlap=0,
            split_respect_sentence_boundary=(split_by == "word"),
        )
        # select only documents with at least 10 words. Otherwise, the documents are not very informative
        preprocessed_docs: list = []
        for doc in preprocessor.process(docs):
            content = doc.content
            if len(content.split()) >= 10 and not (
                content.startswith('","description":"')
            ):
                preprocessed_docs.append(doc)
        return preprocessed_docs

    def retrieve_evidence_docs(self, docs: list, claim: str):
        preprocessed_docs = self._preprocess(docs)
        self.inmemory_doc_store.delete_documents()
        self.inmemory_doc_store.write_documents(preprocessed_docs)
        self.inmemory_doc_store.update_embeddings(self.retriever)
        pipeline = DocumentSearchPipeline(self.retriever)
        return pipeline.run(
            claim, params={"Retriever": {"top_k": self.num_docs}}
        )
