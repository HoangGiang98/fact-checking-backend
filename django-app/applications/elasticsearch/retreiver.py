from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import DensePassageRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from applications.factchecker.models import Answer

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

SPARSE_RETRIEVER = BM25Retriever(
    document_store=SPARSE_DOC_STORE
)

READER = FARMReader(
    model_name_or_path="deepset/bert-base-cased-squad2",
    context_window_size=1500,
    use_gpu=False,
)
# initialize pipeline
DENSE_PIPELINE = ExtractiveQAPipeline(reader=READER, retriever=DENSE_RETRIEVER)
SPARSE_PIPELINE = ExtractiveQAPipeline(reader=READER, retriever=SPARSE_RETRIEVER)


# initialize API


def __resolve_verdict(score):
    if score >= 9.7:
        return "True"
    if score <= -0.7:
        return "False"
    return "Uncertain"


async def get_query(q: str):
    print(q)

    # get answers
    response_json = DENSE_PIPELINE.run(query=q)

    answers = []

    if len(response_json["answers"]) > 0:
        first_answer = Answer()
        first_answer.content = response_json["answers"][0].context
        first_answer.title = response_json["answers"][0].meta["meta"]["name"]
        first_answer.verdict = __resolve_verdict(
            response_json["answers"][0].score
        )

        answers.append(first_answer)

    if len(response_json["answers"]) > 1:
        second_answer = Answer()
        second_answer.content = response_json["answers"][1].context
        second_answer.title = response_json["answers"][1].meta["meta"]["name"]
        second_answer.verdict = __resolve_verdict(
            response_json["answers"][1].score
        )

        answers.append(second_answer)

    return answers


async def get_top10(q: str):
    print(q)

    # get answers
    response_json = SPARSE_PIPELINE.run(query=q)

    return response_json

    answers = []

    if len(response_json["answers"]) > 0:
        first_answer = Answer()
        first_answer.content = response_json["answers"][0].context
        first_answer.title = response_json["answers"][0].meta["meta"]["name"]
        first_answer.verdict = __resolve_verdict(
            response_json["answers"][0].score
        )

        answers.append(first_answer)

    if len(response_json["answers"]) > 1:
        second_answer = Answer()
        second_answer.content = response_json["answers"][1].context
        second_answer.title = response_json["answers"][1].meta["meta"]["name"]
        second_answer.verdict = __resolve_verdict(
            response_json["answers"][1].score
        )

        answers.append(second_answer)

    return answers
