import json
import pickle
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


MODEL_DIR = Path(__file__).parent / "model" / "distilbert_waf_mlm_final"
ARTIFACT_DIR = Path(__file__).parent / "model"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def mean_pool(last_hidden_state, attention_mask):
    mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
    masked = last_hidden_state * mask
    summed = masked.sum(dim=1)
    counts = mask.sum(dim=1).clamp(min=1e-9)
    return summed / counts


class WAFModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        self.encoder = AutoModel.from_pretrained(MODEL_DIR).to(device)
        self.encoder.eval()

        self.global_centroid = np.load(ARTIFACT_DIR / "waf_global_centroid.npy")

        with open(ARTIFACT_DIR / "waf_global_threshold.json", "r", encoding="utf-8") as f:
            self.global_threshold = float(json.load(f)["threshold"])

        with open(ARTIFACT_DIR / "waf_route_centroids.pkl", "rb") as f:
            self.route_centroids = pickle.load(f)

        with open(ARTIFACT_DIR / "waf_route_thresholds.json", "r", encoding="utf-8") as f:
            self.route_thresholds = {k: float(v) for k, v in json.load(f).items()}

        with open(ARTIFACT_DIR / "waf_group_centroids.pkl", "rb") as f:
            self.group_centroids = pickle.load(f)

        with open(ARTIFACT_DIR / "waf_group_thresholds.json", "r", encoding="utf-8") as f:
            self.group_thresholds = {k: float(v) for k, v in json.load(f).items()}

    @torch.no_grad()
    def encode(self, text: str) -> np.ndarray:
        enc = self.tokenizer(
            [text],
            truncation=True,
            padding=True,
            max_length=64,
            return_tensors="pt",
        )
        input_ids = enc["input_ids"].to(device)
        attention_mask = enc["attention_mask"].to(device)

        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        pooled = mean_pool(outputs.last_hidden_state, attention_mask)
        return pooled.cpu().numpy()[0]