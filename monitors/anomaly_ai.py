"""
Statistical anomaly detection for latency metrics.
Uses Z-score and IQR methods for robust anomaly detection.
Fallback implementation - works without sklearn.
"""
import time
import logging
import statistics

logger = logging.getLogger("levqor.anomaly_ai")

class AnomalyAI:
    """Statistical anomaly detector for latency metrics (Z-score + IQR)"""
    
    def __init__(self):
        self.last_train = 0
        self.window = []
        self.mean = 0
        self.std = 0
        self.q1 = 0
        self.q3 = 0
        self.iqr = 0
        self.trained = False
    
    def fit(self, arr):
        """Calculate statistics on latency array"""
        if len(arr) < 10:
            logger.warning("Not enough data to train anomaly model")
            return
        
        self.mean = statistics.mean(arr)
        self.std = statistics.stdev(arr) if len(arr) > 1 else 0
        
        # Calculate IQR
        sorted_arr = sorted(arr)
        n = len(sorted_arr)
        self.q1 = sorted_arr[n // 4]
        self.q3 = sorted_arr[3 * n // 4]
        self.iqr = self.q3 - self.q1
        
        self.trained = True
        self.last_train = time.time()
        logger.info(f"Trained anomaly model on {len(arr)} samples (mean={self.mean:.1f}, std={self.std:.1f})")
    
    def score(self, x):
        """Score a single latency value using Z-score and IQR"""
        if not self.trained:
            return {"ready": False, "reason": "model_not_trained"}
        
        # Z-score method
        z_score = abs(x - self.mean) / (self.std + 1e-6)
        
        # IQR method
        iqr_lower = self.q1 - 1.5 * self.iqr
        iqr_upper = self.q3 + 1.5 * self.iqr
        iqr_anomaly = x < iqr_lower or x > iqr_upper
        
        # Combined detection: anomaly if Z>3 OR outside IQR bounds
        is_anomaly = z_score > 3.0 or iqr_anomaly
        
        # Normalize score to range similar to IsolationForest
        normalized_score = -z_score / 3.0  # Maps -1 to 1 roughly
        
        return {
            "ready": True,
            "score": float(normalized_score),
            "anomaly": is_anomaly,
            "latency_ms": x,
            "z_score": round(z_score, 2),
            "method": "z-score+iqr"
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
