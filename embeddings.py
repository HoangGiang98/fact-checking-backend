from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever


doc_store = ElasticsearchDocumentStore(
    host = '127.0.0.1',
    username = '', password = '',
    index = 'test_en_concat'
)
retriever = DensePassageRetriever(
    document_store=doc_store,
    query_embedding_model='facebook/dpr-question_encoder-single-nq-base',
    passage_embedding_model='facebook/dpr-ctx_encoder-single-nq-base',
    use_gpu=False,
    embed_title=True
)
doc_store.update_embeddings(update_existing_embeddings=False, retriever=retriever, batch_size=10000)
