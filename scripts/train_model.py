"""
Train and evaluate machine learning models for sales prediction.
Supports multiple model types and configurations.
"""

import os
import sys
import click
import pandas as pd
import joblib
from pathlib import Path
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.data_processor import DataProcessor
from src.model_trainer import ModelTrainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option('--data-path', required=True, help='Path to training data CSV')
@click.option('--model-type', default='xgboost', 
              type=click.Choice(['xgboost', 'random_forest', 'gradient_boosting']),
              help='Type of model to train')
@click.option('--output-dir', default='../models/trained',
              help='Directory to save trained model')
@click.option('--test-size', default=0.2, help='Proportion of data for testing')
@click.option('--random-state', default=42, help='Random seed for reproducibility')
def train_model(data_path, model_type, output_dir, test_size, random_state):
    """Train a new sales prediction model."""
    try:
        logger.info(f"Starting model training with {model_type}")
        
        # Initialize processor and load data
        processor = DataProcessor(data_path)
        processor.load_data()  # Load the data into processor
        processor.clean_data()  # Clean the data
        processor.engineer_features()  # Engineer features
        
        # Prepare training data from processed data
        X_train, X_test, y_train, y_test = processor.prepare_training_data(
            train_ratio=1 - test_size  # Convert test_size to train_ratio
        )
        
        # Initialize and train model
        model_trainer = ModelTrainer(output_dir)
        model_trainer.train_model(
            X_train=X_train,
            y_train=y_train,
            model_type=model_type
        )
        
        # Evaluate model
        metrics = model_trainer.evaluate_model(X_test, y_test)
        
        # Save model and metrics
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"sales_prediction_{model_type}_{timestamp}.joblib"
        model_trainer.save_model(model_filename)
        
        # Save evaluation metrics
        metrics_file = Path(output_dir) / f"metrics_{timestamp}.json"
        pd.DataFrame([metrics]).to_json(metrics_file)
        
        logger.info(f"Model training completed. Files saved in {output_dir}")
        logger.info(f"Metrics: {metrics}")
        
    except Exception as e:
        logger.error(f"Model training failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    train_model()