# Software Technologies Documentation
## DMart Analytics Intelligence Platform

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Core Technologies](#core-technologies)
4. [Development Tools](#development-tools)
5. [Architecture & Design Patterns](#architecture--design-patterns)
6. [Dependencies](#dependencies)
7. [API Technologies](#api-technologies)
8. [Frontend Technologies](#frontend-technologies)
9. [Machine Learning Stack](#machine-learning-stack)
10. [Testing Framework](#testing-framework)
11. [Development Workflow](#development-workflow)

---

## 🎯 Overview

The **DMart Analytics Intelligence Platform** is a comprehensive e-commerce analytics and sales prediction system powered by advanced machine learning algorithms. This document provides a detailed overview of all software technologies, frameworks, libraries, and tools used in the development and deployment of this platform.

**Project Type:** Full-Stack Data Science & Analytics Application  
**Primary Language:** Python 3.8+  
**Architecture:** Microservices with API Gateway Pattern  
**Last Updated:** October 14, 2025

---

## 🛠️ Technology Stack

### **1. Backend Stack**
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | ≥3.8 | Core programming language |
| **FastAPI** | ≥0.70.0 | RESTful API framework |
| **Uvicorn** | ≥0.15.0 | ASGI server for async operations |
| **Pydantic** | ≥1.8.0 | Data validation and settings management |

### **2. Frontend Stack**
| Technology | Version | Purpose |
|------------|---------|---------|
| **Streamlit** | ≥1.15.0 | Interactive web dashboard framework |
| **Plotly** | ≥5.3.0 | Interactive data visualization |
| **Requests** | ≥2.26.0 | HTTP client for API communication |

### **3. Machine Learning Stack**
| Technology | Version | Purpose |
|------------|---------|---------|
| **XGBoost** | ≥1.5.0 | Gradient boosting ML algorithm |
| **Scikit-learn** | ≥1.0.0 | ML utilities and preprocessing |
| **Pandas** | ≥1.5.0 | Data manipulation and analysis |
| **NumPy** | ≥1.21.0 | Numerical computing |
| **Joblib** | ≥1.1.0 | Model serialization |

### **4. Testing & Quality**
| Technology | Version | Purpose |
|------------|---------|---------|
| **Pytest** | ≥6.2.5 | Unit testing framework |
| **Pytest-cov** | ≥2.12.0 | Code coverage reporting |

### **5. Utilities**
| Technology | Version | Purpose |
|------------|---------|---------|
| **python-dotenv** | ≥0.19.0 | Environment variable management |
| **Click** | ≥8.0.0 | Command-line interface creation |

---

## 🔧 Core Technologies

### **Python (≥3.8)**
- **Purpose:** Primary programming language
- **Key Features Used:**
  - Type hints and annotations
  - Async/await for concurrent operations
  - Context managers
  - Decorators
  - List comprehensions and generators
  - F-strings for string formatting
  - Dataclasses for structured data

**Why Python?**
- Rich ecosystem for data science and ML
- Excellent libraries for web development
- Strong community support
- Easy integration between components

---

### **FastAPI (≥0.70.0)**
- **Purpose:** High-performance REST API framework
- **Key Features:**
  - Automatic API documentation (OpenAPI/Swagger)
  - Type-based validation with Pydantic
  - Async request handling
  - Built-in security features
  - Dependency injection system


### **Pydantic (≥1.8.0)**
- **Purpose:** Data validation using Python type annotations
- **Key Features:**
  - Runtime type checking
  - JSON schema generation
  - Settings management
  - Custom validators
  - Serialization/deserialization


## 🎨 Frontend Technologies

### **Streamlit (≥1.15.0)**
- **Purpose:** Interactive web application framework
- **Key Features:**
  - Real-time data visualization
  - Widget-based UI components
  - Session state management
  - Caching mechanisms
  - Custom CSS styling support

**Components Used:**
- `st.selectbox` - Dropdown selections
- `st.slider` - Numeric input controls
- `st.date_input` - Date pickers
- `st.button` - Interactive buttons
- `st.plotly_chart` - Interactive charts
- `st.columns` - Layout management
- `st.tabs` - Tabbed navigation
- `st.markdown` - Custom HTML/CSS



### **Plotly (≥5.3.0)**
- **Purpose:** Interactive data visualization
- **Chart Types Used:**
  - Line charts - Time series trends
  - Bar charts - Category comparisons
  - Pie charts - Regional distribution
  - Scatter plots - Anomaly detection
  - Area charts - Sales volumes


## 🤖 Machine Learning Stack

### **XGBoost (≥1.5.0)**
- **Purpose:** Gradient boosting framework for ML
- **Algorithm:** Extreme Gradient Boosting
- **Model Performance:**
  - R² Score: **99.74%**
  - MAPE: **1.84%**
  - Training instances: 9,996 records
  - Feature count: 9 engineered features


### **Scikit-learn (≥1.0.0)**
- **Purpose:** ML utilities and preprocessing
- **Components Used:**
  - `train_test_split` - Data splitting
  - `RandomForestRegressor` - Alternative model
  - `GradientBoostingRegressor` - Ensemble method
  - Performance metrics (MAE, RMSE, R²)
  - Model evaluation tools

**Supported Models:**
1. XGBoost Regressor (Primary)
2. Random Forest Regressor
3. Gradient Boosting Regressor

---

### **Pandas (≥1.5.0)**
- **Purpose:** Data manipulation and analysis
- **Key Operations:**
  - Data loading from CSV
  - DateTime parsing and manipulation
  - GroupBy aggregations
  - Rolling window calculations
  - Feature engineering
  - Data filtering and selection


### **NumPy (≥1.21.0)**
- **Purpose:** Numerical computing
- **Operations:**
  - Array operations
  - Statistical calculations
  - Mathematical functions
  - Random number generation
  - Linear algebra

---

### **Joblib (≥1.1.0)**
- **Purpose:** Model serialization and persistence
- **Features:**
  - Efficient model saving/loading
  - Compression support
  - Large data handling
  - Parallel processing



### **System Architecture**

```
┌─────────────────────────────────────────┐
│         Frontend Layer (Streamlit)       │
│  - Interactive Dashboard                │
│  - Real-time Visualizations             │
│  - User Input Forms                     │
└───────────────┬─────────────────────────┘
                │ HTTP/REST API
                │ (Port 8501 → 8000)
┌───────────────▼─────────────────────────┐
│         Backend API (FastAPI)            │
│  - Request Validation                   │
│  - Business Logic                       │
│  - Model Orchestration                  │
└───────────────┬─────────────────────────┘
                │
     ┌──────────┼──────────┐
     │          │          │
┌────▼────┐ ┌──▼──────┐ ┌▼────────────┐
│  Data   │ │   ML    │ │   Model     │
│ Layer   │ │ Engine  │ │  Storage    │
│         │ │         │ │             │
│ CSV     │ │XGBoost  │ │ .joblib     │
│ Files   │ │Sklearn  │ │ files       │
└─────────┘ └─────────┘ └─────────────┘
```
