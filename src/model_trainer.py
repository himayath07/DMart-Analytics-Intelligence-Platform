"""
Model training and evaluation module for sales prediction.
Supports multiple model types and hyperparameter tuning.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self, model_dir: str):
        """Initialize model trainer with directory for saving models."""
        self.model_dir = model_dir
        self.model = None
        self.feature_importance = None

    def train_model(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        model_type: str = 'xgboost',
        params: Optional[Dict] = None
    ) -> None:
        """Train a new model with specified parameters."""
        logger.info(f"Training {model_type} model...")

        if model_type == 'xgboost':
            default_params = {
                'n_estimators': 100,
                'max_depth': 6,
                'learning_rate': 0.1,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'random_state': 42
            }
            if params:
                default_params.update(params)
            self.model = XGBRegressor(**default_params)

        elif model_type == 'random_forest':
            default_params = {
                'n_estimators': 100,
                'max_depth': 10,
                'random_state': 42
            }
            if params:
                default_params.update(params)
            self.model = RandomForestRegressor(**default_params)

        elif model_type == 'gradient_boosting':
            default_params = {
                'n_estimators': 100,
                'max_depth': 5,
                'learning_rate': 0.1,
                'random_state': 42
            }
            if params:
                default_params.update(params)
            self.model = GradientBoostingRegressor(**default_params)

        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        # Train the model
        self.model.fit(X_train, y_train)

        # Store feature importance
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X_train.columns
            ).sort_values(ascending=False)

    def evaluate_model(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict[str, float]:
        """Evaluate model performance on test data."""
        if self.model is None:
            raise ValueError("No model trained. Call train_model() first.")

        # Make predictions
        y_pred = self.model.predict(X_test)

        # Calculate metrics
        metrics = {
            'MAE': mean_absolute_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'R2': r2_score(y_test, y_pred)
        }

        # Calculate MAPE
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        metrics['MAPE'] = mape

        logger.info("Model Evaluation Metrics:")
        for metric, value in metrics.items():
            logger.info(f"{metric}: {value:.4f}")

        return metrics

    def save_model(self, filename: str) -> None:
        """Save trained model to disk."""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")

        model_path = f"{self.model_dir}\\{filename}"
        joblib.dump(self.model, model_path)
        logger.info(f"Model saved to {model_path}")

        # Save feature importance if available
        if self.feature_importance is not None:
            importance_path = f"{self.model_dir}/{filename}_importance.csv"
            self.feature_importance.to_csv(importance_path)
            logger.info(f"Feature importance saved to {importance_path}")

    def load_model(self, filename: str) -> None:
        """Load trained model from disk."""
        model_path = f"{self.model_dir}\\{filename}"
        self.model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")

        # Load feature importance if available
        importance_path = f"{self.model_dir}/{filename}_importance.csv"
        try:
            self.feature_importance = pd.read_csv(importance_path, index_col=0).squeeze()
            logger.info(f"Feature importance loaded from {importance_path}")
        except FileNotFoundError:
            logger.warning("No feature importance file found.")

    def predict(
        self,
        X: pd.DataFrame,
        return_confidence: bool = False
    ) -> np.ndarray:
        """Generate predictions for new data."""
        if self.model is None:
            raise ValueError("No model loaded. Train or load a model first.")

        predictions = self.model.predict(X)

        if return_confidence and hasattr(self.model, 'predict_proba'):
            confidence = self.model.predict_proba(X)
            return predictions, confidence

        return predictions

    def get_feature_importance(self, top_n: Optional[int] = None) -> pd.Series:
        """Get feature importance scores."""
        if self.feature_importance is None:
            raise ValueError("No feature importance available.")

        if top_n:
            return self.feature_importance.head(top_n)
        return self.feature_importance