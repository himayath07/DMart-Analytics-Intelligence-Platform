"""
Tests for the data processing module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

from src.data_processor import DataProcessor

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'Order ID': range(1, 101),
        'Order Date': [datetime.now() - timedelta(days=x) for x in range(100)],
        'Category': ['Electronics'] * 50 + ['Clothing'] * 50,
        'Sales': np.random.uniform(100, 1000, 100),
        'Discount': np.random.uniform(0, 0.3, 100),
        'Profit': np.random.uniform(10, 200, 100)
    })

@pytest.fixture
def data_processor(tmp_path, sample_data):
    """Create a DataProcessor instance with sample data."""
    data_file = tmp_path / "test_data.csv"
    sample_data.to_csv(data_file, index=False)
    return DataProcessor(str(data_file))

def test_load_data(data_processor):
    """Test data loading functionality."""
    df = data_processor.load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'Order Date' in df.columns
    assert isinstance(df['Order Date'].iloc[0], pd.Timestamp)

def test_clean_data(data_processor):
    """Test data cleaning functionality."""
    data_processor.load_data()
    df = data_processor.clean_data()
    
    # Check derived columns
    assert 'Year' in df.columns
    assert 'Month' in df.columns
    assert 'DayOfWeek' in df.columns
    assert 'Quarter' in df.columns
    
    # Check for duplicates
    assert len(df) == len(df.drop_duplicates())
    
    # Check for missing values
    assert not df['Sales'].isnull().any()

def test_engineer_features(data_processor):
    """Test feature engineering functionality."""
    data_processor.load_data()
    data_processor.clean_data()
    df = data_processor.engineer_features()
    
    # Check engineered features
    assert 'RollingSales30Day' in df.columns
    assert 'SalesLastWeek' in df.columns
    assert 'SalesLastMonth' in df.columns
    assert 'DiscountImpact' in df.columns
    assert 'IsWeekend' in df.columns

def test_get_category_metrics(data_processor):
    """Test category metrics calculation."""
    data_processor.load_data()
    data_processor.clean_data()
    metrics = data_processor.get_category_metrics()
    
    assert isinstance(metrics, dict)
    assert 'Electronics' in metrics
    assert 'Clothing' in metrics
    
    for category in metrics:
        assert 'TotalSales' in metrics[category]
        assert 'AvgSales' in metrics[category]
        assert 'TotalOrders' in metrics[category]
        assert 'AvgDiscount' in metrics[category]
        assert 'TotalProfit' in metrics[category]

def test_prepare_training_data(data_processor):
    """Test preparation of training data."""
    data_processor.load_data()
    data_processor.clean_data()
    data_processor.engineer_features()
    
    X_train, X_test, y_train, y_test = data_processor.prepare_training_data()
    
    # Check shapes
    assert len(X_train) + len(X_test) == len(data_processor.processed_data)
    assert len(y_train) == len(X_train)
    assert len(y_test) == len(X_test)
    
    # Check feature types
    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(y_train, pd.Series)
    
    # Check for data leakage
    train_indices = X_train.index
    test_indices = X_test.index
    assert len(set(train_indices) & set(test_indices)) == 0