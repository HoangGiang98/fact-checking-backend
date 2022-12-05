from fastapi import FastAPI
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline

# initialize doc store, retriever and reader components
DOC_STORE = ElasticsearchDocumentStore(
    host='20.208.36.26', username='', password='', index='aurelius'
)
RETRIEVER = DensePassageRetriever(
    document_store=DOC_STORE,
    query_embedding_model='facebook/dpr-question_encoder-single-nq-base',
    passage_embedding_model='facebook/dpr-ctx_encoder-single-nq-base',
    use_gpu=False,
    embed_title=True
)
READER = FARMReader(model_name_or_path='deepset/bert-base-cased-squad2',
                    context_window_size=1500,
                    use_gpu=False)
# initialize pipeline
PIPELINE = ExtractiveQAPipeline(reader=READER, retriever=RETRIEVER)
# initialize API

async def get_query(q: str, retriever_limit: int = 10, reader_limit: int = 3):
    """Makes query to doc store via Haystack pipeline.

    :param q: Query string representing the question being asked.
    :type q: str
    """
    # get answers
    return PIPELINE.run(query=q)