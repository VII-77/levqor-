"""
Anomaly Detector
Detects unusual patterns in latency, error rates, and system metrics
"""
import statistics
import time
import random
import json
from datetime import datetime
from collections import deque
from typing import List, Dict

class AnomalyDetector:
    """Statistical anomaly detection using standard deviation"""
    
    def __init__(self, window_size: int = 20, sigma_threshold: float = 3.0):
        """
        Initialize detector
        
        Args:
            window_size: Number of samples to keep in rolling window
            sigma_threshold: Number of standard deviations for anomaly
        """
        self.window_size = window_size
        self.sigma_threshold = sigma_threshold
        self.latencies = deque(maxlen=window_size)
        self.error_counts = deque(maxlen=window_size)
        
    def add_latency_sample(self, latency_ms: float):
        """Add latency measurement"""
        self.latencies.append(latency_ms)
    
    def add_error_sample(self, error_count: int):
        """Add error count sample"""
        self.error_counts.append(error_count)
    
    def detect_latency_anomaly(self, current_latency: float) -> Dict:
        """
        Detect if current latency is anomalous
        
        Args:
            current_latency: Current latency measurement
        
        Returns:
            dict with detection results
        """
        if len(self.latencies) < 5:  # Need minimum samples
            return {
                "is_anomaly": False,
                "reason": "Insufficient data",
                "samples": len(self.latencies)
            }
        
        mean = statistics.mean(self.latencies)
        
        if len(self.latencies) < 2:
            stdev = 0
        else:
            stdev = statistics.stdev(self.latencies)
        
        if stdev == 0:
            return {
                "is_anomaly": False,
                "reason": "No variance in data"
            }
        
        z_score = (current_latency - mean) / stdev
        is_anomaly = abs(z_score) > self.sigma_threshold
        
        return {
            "is_anomaly": is_anomaly,
            "z_score": round(z_score, 2),
            "current": round(current_latency, 2),
            "mean": round(mean, 2),
            "stdev": round(stdev, 2),
            "threshold": self.sigma_threshold,
            "severity": "high" if abs(z_score) > 4 else "medium" if abs(z_score) > 3 else "low"
        }
    
    def detect_error_spike(self, current_errors: int) -> Dict:
        """Detect unusual error rate"""
        if len(self.error_counts) < 5:
            return {
                "is_spike": False,
                "reason": "Insufficient data"
            }
        
        mean = statistics.mean(self.error_counts)
        
        if len(self.error_counts) < 2:
            stdev = 0
        else:
            stdev = statistics.stdev(self.error_counts)
        
        if stdev == 0:
            # Check if current is much higher than historical zero/low errors
            is_spike = current_errors > 5
            return {
                "is_spike": is_spike,
                "current": current_errors,
                "mean": mean,
                "reason": "Sudden errors (no historical variance)"
            }
        
        z_score = (current_errors - mean) / stdev
        is_spike = z_score > self.sigma_threshold
        
        return {
            "is_spike": is_spike,
            "z_score": round(z_score, 2),
            "current": current_errors,
            "mean": round(mean, 2),
            "stdev": round(stdev, 2)
        }

def simulate_metrics() -> List[float]:
    """Generate simulated metrics with occasional anomalies"""
    # Normal metrics (50-250ms latency)
    metrics = [random.uniform(50, 250) for _ in range(20)]
    
    # Inject anomalies
    metrics.append(random.uniform(800, 1200))  # High latency anomaly
    metrics.append(random.uniform(800, 1200))  # Another spike
    metrics.append(random.uniform(50, 250))    # Back to normal
    
    return metrics

def run_detection_test():
    """Run anomaly detection test"""
    print("[🔍] Starting Anomaly Detection Test")
    print("="* 60)
    
    detector = AnomalyDetector(window_size=20, sigma_threshold=3.0)
    
    # Generate metrics
    latencies = simulate_metrics()
    
    anomalies_detected = []
    
    for i, latency in enumerate(latencies):
        # Add to detector
        detector.add_latency_sample(latency)
        
        # Check for anomaly
        result = detector.detect_latency_anomaly(latency)
        
        status = "🚨 ANOMALY" if result.get("is_anomaly") else "✓ Normal"
        
        print(f"[{i+1:2d}] {status}  Latency: {latency:6.1f}ms", end="")
        
        if result.get("is_anomaly"):
            print(f"  (z-score: {result['z_score']}, severity: {result['severity']})")
            anomalies_detected.append({
                "sample": i + 1,
                "latency": latency,
                "result": result
            })
        else:
            print()
    
    print()
    print("="* 60)
    print(f"[📊] Detection Summary:")
    print(f"    Total samples: {len(latencies)}")
    print(f"    Anomalies detected: {len(anomalies_detected)}")
    
    if anomalies_detected:
        print()
        print("[⚠️] Anomalies Details:")
        for anomaly in anomalies_detected:
            print(f"    Sample #{anomaly['sample']}: {anomaly['latency']:.1f}ms")
            print(f"      Z-score: {anomaly['result']['z_score']}")
            print(f"      Severity: {anomaly['result']['severity']}")
    
    # Log to file
    with open("logs/anomaly.log", "a") as f:
        f.write(f"\n[{datetime.utcnow().isoformat()}] Anomaly detection run\n")
        f.write(f"Detected {len(anomalies_detected)} anomalies\n")
        for anomaly in anomalies_detected:
            f.write(f"  - Sample #{anomaly['sample']}: {anomaly['latency']:.1f}ms (z={anomaly['result']['z_score']})\n")
    
    print()
    print("[✓] Log appended to: logs/anomaly.log")

if __name__ == "__main__":
    run_detection_test()
