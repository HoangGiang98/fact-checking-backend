from lxml.html.clean import Cleaner

from .enums import VerdictsNLI
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from applications.factchecker.models import Answer
import torch

SCORE_THRESHOLD: int = 70

device = (
    torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
)
model_name = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)


def extract_score(prediction_score, param):
    if param in prediction_score:
        return prediction_score[param]


class NliInference:
    cleaner = Cleaner(
        style=True,
        links=True,
        add_nofollow=True,
        page_structure=True,
        safe_attrs_only=True,
        scripts=True,
        forms=True,
        frames=True,
        embedded=True,
        processing_instructions=True,
        meta=True,
        inline_style=True,
        comments=True,
    )

    def predict_veracity(self, evidence_docs: dict):
        results = []
        verdict_counter = {
            VerdictsNLI.SUPPORTED.value: 0,
            VerdictsNLI.NEUTRAL.value: 0,
            VerdictsNLI.REFUTED.value: 0,
        }
        hypothesis: str = evidence_docs["query"]
        evidence_sentences = evidence_docs["documents"]
        for evid_sent in evidence_sentences:
            premise: str = evid_sent.content
            input = tokenizer(
                premise, hypothesis, truncation=True, return_tensors="pt"
            )
            output = model(
                input["input_ids"].to(device)
            )  # device = "cuda:0" or "cpu"
            prediction = torch.softmax(output["logits"][0], -1).tolist()
            label_names = [
                VerdictsNLI.SUPPORTED.value,
                VerdictsNLI.NEUTRAL.value,
                VerdictsNLI.REFUTED.value,
            ]
            prediction_score = {
                name: round(float(pred) * 100, 1)
                for pred, name in zip(prediction, label_names)
            }
            if any(
                [
                    True
                    for _, v in prediction_score.items()
                    if v >= SCORE_THRESHOLD
                ]
            ):
                result = Answer()
                result.content = (
                    self.cleaner.clean_html("<p>" + premise + "</p>")
                    .replace("<p>", "")
                    .replace("</p>", "")
                )
                result.url = evid_sent.meta["url"]
                result.title = evid_sent.meta["title"]
                result.supported_nli = extract_score(
                    prediction_score, VerdictsNLI.SUPPORTED.value
                )
                result.refuted_nli = extract_score(
                    prediction_score, VerdictsNLI.REFUTED.value
                )
                result.not_enough_info_nli = extract_score(
                    prediction_score, VerdictsNLI.NEUTRAL.value
                )
                results.append(result)
                max_key = max(prediction_score, key=prediction_score.get)
                verdict_counter[max_key] += 1

        return {
            "verdict": self._get_verdict_from_counter(verdict_counter),
            "results": results,
        }

    def _get_verdict_from_counter(self, verdict_counter: dict):
        if sum(verdict_counter.values()) <= 2:
            return VerdictsNLI.NEUTRAL.value
        if (
            verdict_counter[VerdictsNLI.SUPPORTED.value]
            == verdict_counter[VerdictsNLI.REFUTED.value]
        ):
            return VerdictsNLI.NEUTRAL.value
        else:
            return max(verdict_counter, key=verdict_counter.get)
