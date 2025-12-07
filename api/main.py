"""
FastAPI service for sales prediction and analytics.
Provides REST endpoints for predictions and insights.
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
import joblib
import logging
from datetime import datetime, timedelta

app = FastAPI(title="E-commerce Sales Analytics API")
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api.log')
    ]
)
logger = logging.getLogger(__name__)
logger.debug('Starting FastAPI application')

# Load model and scaler at startup
model = None

# Find the latest model file
model_dir = "../models/trained"
try:
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.joblib') and not f.endswith('_importance.csv')]
    if not model_files:
        raise FileNotFoundError('No model files found')
    latest_model = sorted(model_files)[-1]
    MODEL_PATH = os.path.join(model_dir, latest_model)
    logger.info(f'Using latest model: {MODEL_PATH}')
except Exception as e:
    logger.error(f'Error finding model file: {str(e)}')
    MODEL_PATH = None

try:
    logger.debug(f'Attempting to load model from {MODEL_PATH}')
    if not os.path.exists(MODEL_PATH):
        logger.error(f'Model file not found at {MODEL_PATH}')
        raise FileNotFoundError(f'Model file not found at {MODEL_PATH}')
    model = joblib.load(MODEL_PATH)
    logger.info('Model loaded successfully')
except Exception as e:
    logger.error(f'Error loading model: {str(e)}')
    logger.debug('Model loading error details:', exc_info=True)

from pydantic import Field

class PredictionRequest(BaseModel):
    category: str = Field(..., description="Product category")
    subcategory: str = Field(..., description="Product subcategory")
    region: str = Field(..., description="Sales region")
    date: str = Field(..., description="Prediction date in YYYY-MM-DD format")
    discount: float = Field(..., description="Applied discount value")
    historical_sales: Optional[List[float]] = Field(None, description="List of historical sales values")

class PredictionResponse(BaseModel):
    predicted_sales: float = Field(..., description="Predicted sales value")
    confidence_interval: Optional[Dict[str, float]] = Field(None, description="Prediction confidence interval")
    feature_importance: Optional[Dict[str, float]] = Field(None, description="Feature importance scores")

@app.post("/predict", response_model=PredictionResponse)
async def predict_sales(request: PredictionRequest):
    """Generate sales prediction for given features."""
    logger.info(f"Received prediction request for {request.category} - {request.subcategory}")
    
    if model is None:
        logger.error("Model not loaded. Check MODEL_PATH and model loading at startup")
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        # Convert request to feature vector
        logger.info("Converting request to feature vector")
        features = _prepare_features(request)
        logger.debug(f"Feature matrix shape: {features.shape}")
        
        # Generate prediction
        logger.info("Generating prediction")
        prediction = model.predict(features)[0]
        logger.info(f"Raw prediction value: {prediction}")
        
        # Calculate confidence interval based on model's historical performance
        # Using MAPE of 1.84% from metrics, we can estimate a reasonable confidence interval
        confidence_margin = 0.05  # 5% margin based on model performance
        confidence = {
            'lower': prediction * (1 - confidence_margin),
            'upper': prediction * (1 + confidence_margin)
        }

        response = PredictionResponse(
            predicted_sales=float(prediction),
            confidence_interval=confidence
        )
        logger.info(f"Prediction response prepared: {response.dict()}")
        return response

    except ValueError as e:
        logger.error(f"Value error in prediction: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in prediction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Check API health status."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics/{category}")
async def get_category_metrics(category: str):
    """Get historical metrics for a product category."""
    try:
        # Example metrics (replace with actual data access)
        metrics = {
            "total_sales": 1000000,
            "avg_daily_sales": 5000,
            "growth_rate": 0.15,
            "top_products": ["Product A", "Product B"],
            "seasonal_patterns": {
                "high_season": ["December", "January"],
                "low_season": ["August", "September"]
            }
        }
        return metrics

    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def _prepare_features(request: PredictionRequest) -> pd.DataFrame:
    """Convert API request to feature vector for model."""
    logger.debug(f"Preparing features for request: {request.dict()}")
    
    try:
        # Convert date to temporal features
        date = datetime.strptime(request.date, "%Y-%m-%d")
        
        features = {
            'Month': date.month,
            'Quarter': (date.month - 1) // 3 + 1,
            'DayOfWeek': date.weekday(),
            'IsWeekend': 1 if date.weekday() >= 5 else 0,
            'Discount': request.discount,
            'RollingSales30Day': 0.0,  # Will be calculated from historical_sales
            'DiscountImpact': 0.0,  # Will be calculated based on historical sales and discount
            'SalesLastWeek': 0.0,
            'SalesLastMonth': 0.0
        }
        
        # Add historical sales features if provided
        if request.historical_sales:
            # Calculate RollingSales30Day (30-day moving average)
            recent_sales = request.historical_sales[-30:] if len(request.historical_sales) >= 30 else request.historical_sales
            features['RollingSales30Day'] = sum(recent_sales) / len(recent_sales)
            
            # Calculate SalesLastWeek and SalesLastMonth
            features['SalesLastWeek'] = request.historical_sales[-7] if len(request.historical_sales) >= 7 else 0
            features['SalesLastMonth'] = sum(request.historical_sales[-30:]) / 30 if len(request.historical_sales) >= 30 else 0
            
            # Calculate DiscountImpact based on recent sales and current discount
            avg_sales = features['RollingSales30Day']
            features['DiscountImpact'] = avg_sales * request.discount
        
        # Create DataFrame with only the features the model was trained on
        df = pd.DataFrame([features])
        
        # The model only expects these 9 features (no categorical features)
        model_features = [
            'Month', 'Quarter', 'DayOfWeek', 'IsWeekend', 'Discount',
            'RollingSales30Day', 'SalesLastWeek', 'SalesLastMonth', 'DiscountImpact'
        ]
        
        # Create the final feature matrix with only the required columns
        result = df[model_features].fillna(0)
        logger.debug(f"Feature matrix shape: {result.shape}")
        logger.debug(f"Feature columns: {result.columns.tolist()}")
        
        return result
    except Exception as e:
        logger.error(f"Error preparing features: {e}", exc_info=True)
        raise ValueError(f"Error preparing features: {str(e)}")