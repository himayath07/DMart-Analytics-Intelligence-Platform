"""
Monitoring service for the E-commerce Analytics Platform.
Tracks model performance, data drift, and system health.
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import json
import time

class MonitoringService:
    def __init__(self, config_path: str):
        """Initialize monitoring service with configuration."""
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self.metrics_history = []
        
    def _load_config(self, config_path: str) -> dict:
        """Load monitoring configuration."""
        with open(config_path) as f:
            return json.load(f)
    
    def _setup_logging(self) -> logging.Logger:
        """Configure logging for monitoring."""
        logger = logging.getLogger("monitoring")
        logger.setLevel(logging.INFO)
        
        # Add file handler
        fh = logging.FileHandler("logs/monitoring.log")
        fh.setLevel(logging.INFO)
        
        # Add console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def track_prediction(
        self,
        prediction: float,
        actual: Optional[float] = None,
        features: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> None:
        """Track a single prediction and its outcome."""
        timestamp = datetime.now()
        
        record = {
            "timestamp": timestamp,
            "prediction": prediction,
            "actual": actual,
            "features": features,
            "metadata": metadata
        }
        
        self.metrics_history.append(record)
        
        if actual is not None:
            error = abs(prediction - actual)
            error_pct = error / actual if actual != 0 else float('inf')
            
            if error_pct > self.config.get("alert_threshold", 0.2):
                self.logger.warning(
                    f"High prediction error detected: {error_pct:.2%}"
                )
    
    def check_data_drift(
        self,
        current_data: pd.DataFrame,
        reference_data: pd.DataFrame,
        features: List[str]
    ) -> Dict[str, float]:
        """Check for data drift in features."""
        drift_metrics = {}
        
        for feature in features:
            if feature in current_data.columns and feature in reference_data.columns:
                # Calculate KS statistic
                from scipy.stats import ks_2samp
                ks_stat, p_value = ks_2samp(
                    current_data[feature],
                    reference_data[feature]
                )
                
                drift_metrics[feature] = {
                    "ks_statistic": ks_stat,
                    "p_value": p_value,
                    "significant_drift": p_value < 0.05
                }
                
                if p_value < 0.05:
                    self.logger.warning(
                        f"Significant data drift detected in feature {feature}"
                    )
        
        return drift_metrics
    
    def monitor_system_health(self) -> Dict[str, any]:
        """Monitor system health metrics."""
        import psutil
        
        metrics = {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "prediction_count": len(self.metrics_history),
            "last_prediction": self.metrics_history[-1]["timestamp"] if self.metrics_history else None
        }
        
        # Check for concerning metrics
        if metrics["cpu_percent"] > 90:
            self.logger.warning("High CPU usage detected")
        if metrics["memory_percent"] > 90:
            self.logger.warning("High memory usage detected")
        if metrics["disk_percent"] > 90:
            self.logger.warning("Low disk space")
            
        return metrics
    
    def generate_monitoring_report(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, any]:
        """Generate a monitoring report for a time period."""
        if start_time is None:
            start_time = datetime.now() - timedelta(days=1)
        if end_time is None:
            end_time = datetime.now()
            
        # Filter metrics history
        period_metrics = [
            m for m in self.metrics_history
            if start_time <= m["timestamp"] <= end_time
        ]
        
        # Calculate aggregate metrics
        predictions = [m["prediction"] for m in period_metrics]
        actuals = [m["actual"] for m in period_metrics if m["actual"] is not None]
        
        report = {
            "period": {
                "start": start_time,
                "end": end_time
            },
            "predictions": {
                "count": len(predictions),
                "mean": np.mean(predictions) if predictions else None,
                "std": np.std(predictions) if predictions else None
            },
            "accuracy": {
                "mape": self._calculate_mape(predictions, actuals) if actuals else None,
                "mae": self._calculate_mae(predictions, actuals) if actuals else None
            },
            "system_health": self.monitor_system_health(),
            "alerts": self._get_alerts(start_time, end_time)
        }
        
        return report
    
    def _calculate_mape(
        self,
        predictions: List[float],
        actuals: List[float]
    ) -> float:
        """Calculate Mean Absolute Percentage Error."""
        return np.mean(np.abs((np.array(actuals) - np.array(predictions)) / np.array(actuals))) * 100
    
    def _calculate_mae(
        self,
        predictions: List[float],
        actuals: List[float]
    ) -> float:
        """Calculate Mean Absolute Error."""
        return np.mean(np.abs(np.array(actuals) - np.array(predictions)))
    
    def _get_alerts(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> List[Dict]:
        """Get alerts from log file in time period."""
        alerts = []
        log_path = "logs/monitoring.log"
        
        if Path(log_path).exists():
            with open(log_path) as f:
                for line in f:
                    try:
                        log_time = datetime.strptime(
                            line.split(' - ')[0],
                            '%Y-%m-%d %H:%M:%S,%f'
                        )
                        if start_time <= log_time <= end_time and "WARNING" in line:
                            alerts.append({
                                "timestamp": log_time,
                                "message": line.strip()
                            })
                    except:
                        continue
                        
        return alerts