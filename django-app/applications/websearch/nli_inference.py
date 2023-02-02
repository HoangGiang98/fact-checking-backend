from .enums import Verdicts
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

SCORE_THRESHOLD: int = 70

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model_name = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

class NliInference:
  def predict_veracity (self, evidence_docs: dict):
    results = []
    verdict_counter = {
      Verdicts.SUPPORTED.value: 0,
      Verdicts.NEUTRAL.value: 0,
      Verdicts.REFUTED.value: 0
    }
    hypothesis:str = evidence_docs['query']
    evidence_sentences = evidence_docs["documents"]
    for evid_sent in evidence_sentences:
      premise: str = evid_sent.content
      input = tokenizer(premise, hypothesis, truncation=True, return_tensors="pt")
      output = model(input["input_ids"].to(device))  # device = "cuda:0" or "cpu"
      prediction = torch.softmax(output["logits"][0], -1).tolist()
      label_names = [Verdicts.SUPPORTED.value, Verdicts.NEUTRAL.value, Verdicts.REFUTED.value]
      prediction_score = {name: round(float(pred) * 100, 1) for pred, name in zip(prediction, label_names)}
      if any([True for _,v in prediction_score.items() if v >= SCORE_THRESHOLD]):
        result: dict = {
          "content": premise,
          "url": evid_sent.meta["url"],
          "title" : evid_sent.meta["title"],
          "score": prediction_score
        }
        results.append(result)
        max_key = max(prediction_score, key = prediction_score.get)
        verdict_counter[max_key] += 1
    fc_results = {
      "claim": hypothesis, "results":results, "verdict":  self._get_verdict_from_counter(verdict_counter)
    }
    return fc_results

  def _get_verdict_from_counter(self, verdict_counter: dict):
    if sum(verdict_counter.values()) <=2:
      return Verdicts.NEUTRAL.value
    if verdict_counter[Verdicts.SUPPORTED.value] == verdict_counter[Verdicts.REFUTED.value] :
      return Verdicts.NEUTRAL.value
    else:
      return max(verdict_counter, key = verdict_counter.get)