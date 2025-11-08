"""
ML-based anomaly detection for latency metrics using IsolationForest.
Trains in-memory on sliding window of recent latencies.
"""
from sklearn.ensemble import IsolationForest
import numpy as np
import time
import logging

logger = logging.getLogger("levqor.anomaly_ai")

class AnomalyAI:
    """IsolationForest-based anomaly detector for latency metrics"""
    
    def __init__(self):
        self.clf = None
        self.last_train = 0
        self.window = []
    
    def fit(self, arr):
        """Train model on latency array"""
        if len(arr) < 10:
            logger.warning("Not enough data to train anomaly model")
            return
        
        X = np.array(arr).reshape(-1, 1)
        self.clf = IsolationForest(
            contamination=0.03,
            random_state=42,
            n_estimators=100
        ).fit(X)
        self.last_train = time.time()
        logger.info(f"Trained anomaly model on {len(arr)} samples")
    
    def score(self, x):
        """Score a single latency value"""
        if not self.clf:
            return {"ready": False, "reason": "model_not_trained"}
        
        score = self.clf.decision_function(np.array([[x]]))[0]
        is_anomaly = score < -0.15
        
        return {
            "ready": True,
            "score": float(score),
            "anomaly": is_anomaly,
            "latency_ms": x
        }
    
    def update_window(self, lat):
        """Add latency to sliding window and retrain if needed"""
        self.window.append(lat)
        
        # Keep last 500 samples
        if len(self.window) > 500:
            self.window = self.window[-500:]
        
        # Retrain every 5 minutes if we have enough data
        if len(self.window) >= 100 and time.time() - self.last_train > 300:
            self.fit(self.window)
    
    def predict(self, lat):
        """Update model and predict anomaly for given latency"""
        self.update_window(lat)
        return self.score(lat)


# Global model instance
model = AnomalyAI()


def predict(latency_ms):
    """Predict if latency is anomalous"""
    return model.predict(latency_ms)


def get_stats():
    """Get model statistics"""
    return {
        "ready": model.clf is not None,
        "window_size": len(model.window),
        "last_train": model.last_train,
        "time_since_train": time.time() - model.last_train if model.last_train else None
    }
