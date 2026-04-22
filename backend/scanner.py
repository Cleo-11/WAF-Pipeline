import numpy as np

from model_loader import WAFModel
from preprocess import extract_route_key, map_route_group


class WAFScanner:
    def __init__(self):
        self.model = WAFModel()

    def score_serialized(self, serialized_request: str):
        embedding = self.model.encode(serialized_request)
        route = extract_route_key(serialized_request)

        if route in self.model.route_centroids:
            centroid = self.model.route_centroids[route]
            threshold = self.model.route_thresholds[route]
            mode = "route"
        else:
            group = map_route_group(route)
            if group in self.model.group_centroids:
                centroid = self.model.group_centroids[group]
                threshold = self.model.group_thresholds[group]
                mode = "group"
            else:
                centroid = self.model.global_centroid
                threshold = self.model.global_threshold
                mode = "global"

        score = float(np.linalg.norm(embedding - centroid))
        verdict = "SUSPICIOUS" if score >= threshold else "BENIGN"

        return {
            "route": route,
            "mode": mode,
            "score": score,
            "threshold": float(threshold),
            "verdict": verdict,
            "serialized": serialized_request,
        }