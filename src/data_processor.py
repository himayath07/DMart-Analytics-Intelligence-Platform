"""
Data processing module for E-commerce sales analytics.
Handles data ingestion, cleaning, and feature engineering.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class DataProcessor:
    def __init__(self, data_path: str):
        """Initialize the data processor with path to raw data."""
        self.data_path = data_path
        self.raw_data = None
        self.processed_data = None

    def load_data(self) -> pd.DataFrame:
        """Load raw sales data from CSV."""
        self.raw_data = pd.read_csv(self.data_path)
        # Convert date column to datetime with mixed format handling
        self.raw_data['Order Date'] = pd.to_datetime(self.raw_data['Order Date'], format='mixed')
        return self.raw_data

    def clean_data(self) -> pd.DataFrame:
        """Clean and preprocess the raw data."""
        if self.raw_data is None:
            raise ValueError("No data loaded. Call load_data() first.")

        df = self.raw_data.copy()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.dropna(subset=['Order ID', 'Order Date', 'Sales'])
        
        # Add derived temporal features
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['DayOfWeek'] = df['Order Date'].dt.dayofweek
        df['Quarter'] = df['Order Date'].dt.quarter
        
        self.processed_data = df
        return df

    def engineer_features(self, lookback_days: int = 30) -> pd.DataFrame:
        """Engineer features for ML models."""
        if self.processed_data is None:
            raise ValueError("No processed data. Call clean_data() first.")

        df = self.processed_data.copy()
        
        # Sort by date
        df = df.sort_values('Order Date')
        
        # Rolling metrics by product category
        for category in df['Category'].unique():
            cat_data = df[df['Category'] == category]
            
            # Rolling average sales
            rolling_sales = cat_data.groupby('Order Date')['Sales'].sum().rolling(
                window=lookback_days, min_periods=1).mean()
                
            # Map back to main dataframe
            df.loc[df['Category'] == category, 'RollingSales30Day'] = df[
                df['Category'] == category]['Order Date'].map(rolling_sales)
        
        # Lag features
        df['SalesLastWeek'] = df.groupby('Category')['Sales'].shift(7)
        df['SalesLastMonth'] = df.groupby('Category')['Sales'].shift(30)
        
        # Promotion impact
        df['DiscountImpact'] = df['Sales'] * df['Discount']
        
        # Seasonality
        df['IsWeekend'] = df['DayOfWeek'].isin([5, 6]).astype(int)
        
        # Fill NAs from rolling/lag features
        df = df.fillna(0)
        
        # Update processed data
        self.processed_data = df
        
        return df

    def get_category_metrics(self) -> Dict[str, Dict]:
        """Calculate key metrics per product category."""
        if self.processed_data is None:
            raise ValueError("No processed data. Call clean_data() first.")

        metrics = {}
        for category in self.processed_data['Category'].unique():
            cat_data = self.processed_data[self.processed_data['Category'] == category]
            metrics[category] = {
                'TotalSales': cat_data['Sales'].sum(),
                'AvgSales': cat_data['Sales'].mean(),
                'TotalOrders': len(cat_data),
                'AvgDiscount': cat_data['Discount'].mean(),
                'TotalProfit': cat_data['Profit'].sum()
            }
        return metrics

    def prepare_training_data(
        self, 
        target_col: str = 'Sales',
        train_ratio: float = 0.8
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Prepare feature matrices and target vectors for ML training."""
        if self.processed_data is None:
            raise ValueError("No processed data. Call clean_data() first.")

        # Feature columns for ML
        feature_cols = [
            'Month', 'Quarter', 'DayOfWeek', 'IsWeekend', 
            'Discount', 'RollingSales30Day', 'SalesLastWeek',
            'SalesLastMonth', 'DiscountImpact'
        ]

        # Encode categorical features, but only for columns that exist
        categorical_cols = [c for c in ['Category', 'Sub Category', 'Region'] if c in self.processed_data.columns]
        if categorical_cols:
            data = pd.get_dummies(self.processed_data, columns=categorical_cols)
        else:
            data = self.processed_data.copy()

        # Split into features (X) and target (y)
        X = data[feature_cols]
        y = data[target_col]

        # Train/test split by time
        train_size = int(len(data) * train_ratio)
        X_train = X[:train_size]
        X_test = X[train_size:]
        y_train = y[:train_size]
        y_test = y[train_size:]

        return X_train, X_test, y_train, y_test