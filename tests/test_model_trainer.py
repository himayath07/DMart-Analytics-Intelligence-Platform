"""
Tests for the model training module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import joblib

from src.model_trainer import ModelTrainer

@pytest.fixture
def sample_data():
    """Create sample training data."""
    np.random.seed(42)
    n_samples = 1000
    
    X = pd.DataFrame({
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(0, 1, n_samples),
        'feature3': np.random.normal(0, 1, n_samples)
    })
    
    # Generate target with some noise
    y = 2 * X['feature1'] + X['feature2'] - 0.5 * X['feature3'] + np.random.normal(0, 0.1, n_samples)
    
    return X, pd.Series(y)

@pytest.fixture
def model_trainer(tmp_path):
    """Create a ModelTrainer instance."""
    return ModelTrainer(str(tmp_path))

def test_train_model(model_trainer, sample_data):
    """Test model training functionality."""
    X, y = sample_data
    
    # Test XGBoost
    model_trainer.train_model(X, y, model_type='xgboost')
    assert model_trainer.model is not None
    assert hasattr(model_trainer.model, 'predict')
    assert model_trainer.feature_importance is not None
    
    # Test Random Forest
    model_trainer.train_model(X, y, model_type='random_forest')
    assert model_trainer.model is not None
    assert hasattr(model_trainer.model, 'predict')
    
    # Test invalid model type
    with pytest.raises(ValueError):
        model_trainer.train_model(X, y, model_type='invalid_model')

def test_evaluate_model(model_trainer, sample_data):
    """Test model evaluation functionality."""
    X, y = sample_data
    model_trainer.train_model(X, y)
    
    metrics = model_trainer.evaluate_model(X, y)
    
    assert isinstance(metrics, dict)
    assert 'MAE' in metrics
    assert 'RMSE' in metrics
    assert 'R2' in metrics
    assert 'MAPE' in metrics
    
    # Check metric values are reasonable
    assert 0 <= metrics['R2'] <= 1
    assert metrics['MAE'] >= 0
    assert metrics['RMSE'] >= 0
    assert metrics['MAPE'] >= 0

def test_save_load_model(model_trainer, sample_data, tmp_path):
    """Test model saving and loading functionality."""
    X, y = sample_data
    
    # Train and save model
    model_trainer.train_model(X, y)
    model_filename = "test_model.joblib"
    model_trainer.save_model(model_filename)
    
    # Check files exist
    assert (Path(model_trainer.model_dir) / model_filename).exists()
    
    # Load model and verify
    new_trainer = ModelTrainer(str(tmp_path))
    new_trainer.load_model(model_filename)
    
    # Compare predictions
    original_preds = model_trainer.predict(X)
    loaded_preds = new_trainer.predict(X)
    np.testing.assert_array_almost_equal(original_preds, loaded_preds)

def test_predict(model_trainer, sample_data):
    """Test prediction functionality."""
    X, y = sample_data
    model_trainer.train_model(X, y)
    
    # Test single prediction
    X_single = X.head(1)
    pred_single = model_trainer.predict(X_single)
    assert isinstance(pred_single, np.ndarray)
    assert len(pred_single) == 1
    
    # Test batch prediction
    X_batch = X.head(10)
    pred_batch = model_trainer.predict(X_batch)
    assert isinstance(pred_batch, np.ndarray)
    assert len(pred_batch) == 10

def test_get_feature_importance(model_trainer, sample_data):
    """Test feature importance retrieval."""
    X, y = sample_data
    model_trainer.train_model(X, y)
    
    importance = model_trainer.get_feature_importance()
    assert isinstance(importance, pd.Series)
    assert len(importance) == X.shape[1]
    assert all(importance.index == X.columns)
    
    # Test top N features
    top_2 = model_trainer.get_feature_importance(top_n=2)
    assert len(top_2) == 2