from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import DensePassageRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.pipelines import DocumentSearchPipeline
from applications.factchecker.models import Answer
from applications.utils.enums import VerdictsDPR

# initialize doc store, retriever and reader components
DENSE_DOC_STORE = ElasticsearchDocumentStore(
    host="176.105.202.80", username="", password="", index="test_en_concat"
)
SPARSE_DOC_STORE = ElasticsearchDocumentStore(
    host="176.105.202.80", username="", password="", index="en_wiki_concat"
)
DENSE_RETRIEVER = DensePassageRetriever(
    document_store=DENSE_DOC_STORE,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    use_gpu=False,
    embed_title=True,
)

SPARSE_RETRIEVER = BM25Retriever(document_store=SPARSE_DOC_STORE)

READER = FARMReader(
    model_name_or_path="deepset/bert-base-cased-squad2",
    context_window_size=1500,
    use_gpu=False,
)
# initialize pipeline
DENSE_PIPELINE = ExtractiveQAPipeline(reader=READER, retriever=DENSE_RETRIEVER)
SPARSE_PIPELINE = DocumentSearchPipeline(retriever=SPARSE_RETRIEVER)


def get_query(q: str):
    # get answers
    response_json = DENSE_PIPELINE.run(query=q)
    response_json["answers"].sort(key=lambda x: abs(x.score), reverse=True)

    answers = []
    verdict = VerdictsDPR.LOW_SIMILARITY

    if len(response_json["answers"]) > 0:
        first_answer = Answer()
        first_answer.content = response_json["answers"][0].context
        first_answer.similarity_dpr = response_json["answers"][0].score * 100
        if response_json["answers"][0].score > 0.8:
            verdict = VerdictsDPR.HIGH_SIMILARITY
        if response_json["answers"][0].score < -0.8:
            verdict = VerdictsDPR.NO_SIMILARITY
        title = response_json["answers"][0].meta["meta"]["name"]
        first_answer.title = title
        first_answer.url = f"https://en.wikipedia.org/wiki/{title}"
        answers.append(first_answer)

    if len(response_json["answers"]) > 1:
        second_answer = Answer()
        second_answer.content = response_json["answers"][1].context
        second_answer.similarity_dpr = response_json["answers"][1].score * 100
        title = response_json["answers"][1].meta["meta"]["name"]
        second_answer.title = title
        second_answer.url = f"https://en.wikipedia.org/wiki/{title}"
        answers.append(second_answer)

    return {"verdict": verdict.value, "results": answers}


def get_top_k_docs(q: str, k: int = 10):
    # get answers
    response_json = SPARSE_PIPELINE.run(
        query=q, params={"Retriever": {"top_k": k}}
    )
    return response_json
