"""
Initialize database and storage for the E-commerce Analytics Platform.
Creates necessary directories and initial data structures.
"""

import os
import sys
import pandas as pd
from pathlib import Path
import shutil
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def init_directories():
    """Create necessary directories if they don't exist."""
    base_dir = Path(__file__).parent.parent
    dirs = [
        base_dir / "data" / "raw",
        base_dir / "data" / "processed",
        base_dir / "data" / "features",
        base_dir / "models" / "trained",
        base_dir / "models" / "evaluation",
        base_dir / "logs"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")

def init_data():
    """Initialize data storage with example or provided data."""
    base_dir = Path(__file__).parent.parent
    source_data = base_dir / "DMart_Grocery_Sales_-_Retail_Analytics_Dataset.csv"
    
    if source_data.exists():
        # Copy to raw data directory
        dest_path = base_dir / "data" / "raw" / "sales_data.csv"
        shutil.copy2(source_data, dest_path)
        logger.info(f"Copied sales data to: {dest_path}")
        
        # Create a sample processed version
        df = pd.read_csv(source_data)
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        
        # Add some basic derived features
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['DayOfWeek'] = df['Order Date'].dt.dayofweek
        
        # Save processed version
        processed_path = base_dir / "data" / "processed" / "sales_data_processed.csv"
        df.to_csv(processed_path, index=False)
        logger.info(f"Created processed dataset at: {processed_path}")
    else:
        logger.warning(f"Source data not found at: {source_data}")

def init_env():
    """Create .env file with default configuration."""
    base_dir = Path(__file__).parent.parent
    # env_example = base_dir / ".env.example"
    env_file = base_dir / ".env"
    
    if not env_file.exists():
        config = {
            "API_PORT": "8000",
            "DEBUG_MODE": "True",
            "MODEL_PATH": "models/trained/sales_prediction_model.joblib",
            "DATA_PATH": "data/processed/sales_data_processed.csv",
            "LOG_LEVEL": "INFO",
            "FEATURE_STORE_PATH": "data/features",
            "MODEL_REGISTRY_PATH": "models/trained",
            "MONITORING_ENABLED": "True"
        }
        
        with open(env_file, 'w') as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")
        
        # Create example env file
        with open(env_example, 'w') as f:
            for key, value in config.items():
                f.write(f"{key}=<your_{key.lower()}_here>\n")
        
        logger.info(f"Created .env and .env.example files")

def main():
    """Main initialization function."""
    logger.info("Starting initialization...")
    
    try:
        init_directories()
        init_data()
        init_env()
        logger.info("Initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()