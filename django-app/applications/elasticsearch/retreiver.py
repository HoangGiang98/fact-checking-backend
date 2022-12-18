from fastapi import FastAPI
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from applications.factchecker.models import Answer

# initialize doc store, retriever and reader components
DOC_STORE = ElasticsearchDocumentStore(
    host="20.250.28.198", username="", password="", index="en_wiki_dpr_concat"
)
RETRIEVER = DensePassageRetriever(
    document_store=DOC_STORE,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    use_gpu=False,
    embed_title=True,
)
READER = FARMReader(
    model_name_or_path="deepset/bert-base-cased-squad2",
    context_window_size=1500,
    use_gpu=False,
)
# initialize pipeline
PIPELINE = ExtractiveQAPipeline(reader=READER, retriever=RETRIEVER)


# initialize API


def __resolve_verdict(score):
    if score >= 9.7:
        return "True"
    if score <= -0.7:
        return "False"
    return "Uncertain"


async def get_query(q: str, retriever_limit: int = 10, reader_limit: int = 3):
    """Makes query to doc store via Haystack pipeline.

    :param q: Query string representing the question being asked.
    :type q: str
    """

    print(q)

    # get answers
    response_json = PIPELINE.run(query=q)

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
