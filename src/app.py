"""
Streamlit frontend for E-commerce sales analytics dashboard.
Provides interactive visualizations and forecasting interface.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional
import json
import os

# Page config with modern aesthetics
st.set_page_config(
    page_title="Ecommerce Sales Prediction and Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra Modern CSS Design System
st.markdown("""
<style>
    /* Premium Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Sophisticated gradient animations */
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes meshGradient {
        0% { background-position: 0% 0%; }
        25% { background-position: 100% 0%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 0%; }
    }
    
    /* Premium dark background with mesh gradient */
    .main {
        background: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
            linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #0f1729 50%, #1e2139 75%, #0d1117 100%);
        background-size: 400% 400%;
        animation: meshGradient 20s ease infinite;
        background-attachment: fixed;
        padding: 0;
        min-height: 100vh;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1800px;
    }
    
    /* Premium Navigation Header */
    .nav-header {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        padding: 1.5rem 2.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .nav-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
        animation: navShine 3s infinite;
    }
    
    @keyframes navShine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .nav-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }
    
    .nav-subtitle {
        color: rgba(148, 163, 184, 0.9);
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 0.5rem;
        letter-spacing: 0.02em;
    }
    
    /* Modern Metric Cards */
    .metric-card-modern {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 16px;
        padding: 1.75rem;
        border: 1px solid rgba(99, 102, 241, 0.15);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    
    .metric-card-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .metric-card-modern:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 
            0 20px 60px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .metric-card-modern:hover::before {
        opacity: 1;
    }
    
    .metric-label-modern {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(148, 163, 184, 0.8);
        margin-bottom: 0.75rem;
    }
    
    .metric-value-modern {
        font-size: 2.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        letter-spacing: -0.02em;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-change {
        font-size: 0.875rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        margin-top: 0.5rem;
    }
    
    .metric-change-positive {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    .metric-change-negative {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    /* Premium Sidebar Design */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: rgba(226, 232, 240, 0.9);
    }
    
    [data-testid="stSidebar"] strong {
        color: #a78bfa;
        font-weight: 600;
    }
    
    /* Modern Glassmorphic Cards */
    .glass-card-modern {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(99, 102, 241, 0.15);
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card-modern::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
        transition: left 0.6s;
    }
    
    .glass-card-modern:hover {
        transform: translateY(-6px);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 
            0 20px 60px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .glass-card-modern:hover::after {
        left: 100%;
    }
    
    /* Premium Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        background-size: 200% 200%;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        text-transform: none;
        letter-spacing: 0.01em;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5);
        background-position: 100% 0;
    }
    
    .stButton > button:hover::before {
        transform: translateX(100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Modern Input Fields */
    .stSelectbox > div > div,
    .stDateInput > div > div,
    .stNumberInput > div > div {
        background: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover,
    .stDateInput > div > div:hover,
    .stNumberInput > div > div:hover {
        border-color: rgba(99, 102, 241, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .stSelectbox > div > div:focus-within,
    .stDateInput > div > div:focus-within,
    .stNumberInput > div > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    .stSelectbox input,
    .stDateInput input,
    .stNumberInput input {
        color: #f8fafc !important;
        font-weight: 500 !important;
    }
    
    /* Modern Slider */
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
    }
    
    .stSlider > div > div > div {
        background: rgba(99, 102, 241, 0.2) !important;
    }
    
    .stSlider [role="slider"] {
        background: white !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Modern Alerts */
    .stSuccess {
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        color: #4ade80;
        backdrop-filter: blur(10px);
        font-weight: 500;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        color: #f87171;
        backdrop-filter: blur(10px);
        font-weight: 500;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        color: #60a5fa;
        backdrop-filter: blur(10px);
        font-weight: 500;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.15);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        color: #fbbf24;
        backdrop-filter: blur(10px);
        font-weight: 500;
    }
    
    /* Modern Charts */
    .js-plotly-plot {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(99, 102, 241, 0.3);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 14px;
        padding: 0.5rem;
        border: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: rgba(226, 232, 240, 0.7);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        border: none;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(99, 102, 241, 0.1);
        color: rgba(226, 232, 240, 0.95);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        transform: none !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Modern Prediction Result Card */
    .prediction-result-modern {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        background-size: 200% 200%;
        border-radius: 20px;
        padding: 2.5rem;
        color: white;
        text-align: center;
        animation: gradientFlow 8s ease infinite, fadeInScale 0.6s ease-out;
        box-shadow: 0 16px 48px rgba(99, 102, 241, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }
    
    .prediction-result-modern::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 2px);
        background-size: 40px 40px;
        animation: sparkleMove 20s linear infinite;
        opacity: 0.4;
    }
    
    @keyframes sparkleMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(40px, 40px); }
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .prediction-value {
        font-size: 3rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }
    
    /* Modern Section Headers */
    .section-header-modern {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(99, 102, 241, 0.2);
        letter-spacing: -0.01em;
    }
    
    /* Modern Insight Cards */
    .insight-card-modern {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .insight-card-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        border-radius: 16px 16px 0 0;
    }
    
    .insight-card-modern:hover {
        transform: translateY(-6px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 16px 48px rgba(99, 102, 241, 0.3);
    }
    
    .insight-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    }
    
    .insight-title {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(148, 163, 184, 0.9);
        margin-bottom: 0.75rem;
    }
    
    .insight-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .insight-subtitle {
        font-size: 0.875rem;
        color: rgba(148, 163, 184, 0.8);
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Modern DataFrames */
    [data-testid="stDataFrame"] {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(20px);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stDataFrame"] table {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stDataFrame"] th {
        background: rgba(99, 102, 241, 0.2) !important;
        color: #f8fafc !important;
        font-weight: 600 !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
    }
    
    [data-testid="stDataFrame"] td {
        border-color: rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        color: #e2e8f0;
    }
    
    .stCheckbox > label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px);
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500;
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-color: rgba(99, 102, 241, 0.2) !important;
        border-top-color: #6366f1 !important;
    }
    
    /* Modern scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.4);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
    }
    
    /* Responsive design improvements */
    @media (max-width: 768px) {
        .nav-title {
            font-size: 1.5rem;
        }
        
        .metric-value-modern {
            font-size: 1.75rem;
        }
        
        .prediction-value {
            font-size: 2rem;
        }
        
        .insight-value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# API endpoint - configurable for cloud deployment
API_URL = os.environ.get("API_URL", None)  # None = standalone mode without API

# USD to INR conversion rate (approximate)
USD_TO_INR = 83.0

def format_inr(amount: float) -> str:
    """Format amount in Indian Rupee format with ₹ symbol"""
    if amount >= 10000000:  # 1 Crore
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh
        return f"₹{amount/100000:.2f} L"
    elif amount >= 1000:  # 1 Thousand
        return f"₹{amount/1000:.2f} K"
    else:
        return f"₹{amount:,.2f}"

def load_data() -> pd.DataFrame:
    """Load and cache the sales data."""
    @st.cache_data
    def _load_data(uploaded_file=None):
        import os

        # If uploaded file is provided, use it directly
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            if 'Order Date' in df.columns:
                df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
            return df

        # Candidate paths to try (in order)
        candidates = []

        # 1) Data folder inside the workspace
        workspace_data = os.path.join(os.path.dirname(__file__), '..', 'data')
        candidates.append(os.path.abspath(os.path.join(workspace_data, 'DMart_Grocery_Sales_-_Retail_Analytics_Dataset.csv')))

        # 2) Environment variable DATA_PATH
        env_path = os.environ.get('DATA_PATH')
        if env_path:
            candidates.append(os.path.abspath(env_path))

        # 3) Current working directory
        candidates.append(os.path.abspath('DMart_Grocery_Sales_-_Retail_Analytics_Dataset.csv'))

        # 4) Original path (kept for backward compatibility)
        candidates.append(r"c:\Users\mohdh\Downloads\ecommerce_analytics\data\DMart_Grocery_Sales_-_Retail_Analytics_Dataset.csv")

        found = None
        for p in candidates:
            try:
                if os.path.exists(p):
                    found = p
                    break
            except Exception:
                continue

        if found is None:
            # Return None to trigger file uploader in main
            return None
        
        df = pd.read_csv(found)

        # Ensure Order Date is parsed to datetime
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        return df
    
    # Check if file uploader is needed
    data = _load_data()
    if data is None:
        st.warning("📂 Sales data CSV not found. Please upload the dataset below.")
        uploaded = st.file_uploader("Upload DMart CSV file", type=['csv'], key='data_uploader')
        if uploaded is not None:
            data = _load_data(uploaded)
        else:
            st.info("👆 Please upload the DMart_Grocery_Sales_-_Retail_Analytics_Dataset.csv file to continue.")
            st.stop()
    
    return data

def main():
    """Main Streamlit application."""
    
    # Initialize session state to prevent tab redirect issues
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    
    # Modern Navigation Header
    st.markdown("""
        <div class="nav-header">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2.5rem;">📊</div>
                <div>
                    <h1 class="nav-title">Ecommerce Sales Prediction & Analysis</h1>
                    <p class="nav-subtitle">AI-Powered Insights • XGBoost ML • Real-time Analytics</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Modern Sidebar design
    with st.sidebar:
            st.markdown("""
            <div style='text-align: center; padding: 0.75rem; 
                        background: rgba(99, 102, 241, 0.15);
                        backdrop-filter: blur(20px);
                        border: 1px solid rgba(99, 102, 241, 0.3);
                        border-radius: 14px; margin-bottom: 1rem;
                        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);'>
                <h2 style='margin: 0; font-size: 1.1rem; font-weight: 700;
                           background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%);
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                           background-clip: text;'>
                    ⚙️ Dashboard Controls
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Date range selector with better UX
            st.markdown("<p style='color: #cbd5e1; font-weight: 600; font-size: 0.875rem; margin-bottom: 0.5rem;'>📅 TIME PERIOD</p>", unsafe_allow_html=True)
            date_range = st.date_input(
                "Select Date Range",
                value=(df['Order Date'].min().date(), df['Order Date'].max().date()),
                label_visibility="collapsed"
            )
            
            # Ensure date_range is always a tuple with 2 values
            if not isinstance(date_range, tuple):
                date_range = (date_range, date_range)
            elif len(date_range) == 1:
                date_range = (date_range[0], date_range[0])
            
            st.markdown("<div style='margin: 0.75rem 0; height: 1px; background: rgba(99, 102, 241, 0.2);'></div>", unsafe_allow_html=True)
            
            # Category filters with select all option
            st.markdown("<p style='color: #cbd5e1; font-weight: 600; font-size: 0.875rem; margin-bottom: 0.5rem;'>🏷️ CATEGORIES</p>", unsafe_allow_html=True)
            select_all = st.checkbox("Select All Categories", value=True)
            
            if select_all:
                categories = df['Category'].unique().tolist()
            else:
                categories = st.multiselect(
                    "Choose categories",
                    options=df['Category'].unique(),
                    default=[df['Category'].unique()[0]],
                    label_visibility="collapsed"
                )
            
            
            st.markdown("<div style='margin: 0.75rem 0; height: 1px; background: rgba(99, 102, 241, 0.2);'></div>", unsafe_allow_html=True)
            
            # Region filter
            st.markdown("<p style='color: #cbd5e1; font-weight: 600; font-size: 0.875rem; margin-bottom: 0.5rem;'>🌍 REGIONS</p>", unsafe_allow_html=True)
            regions = st.multiselect(
                "Select Regions",
                options=df['Region'].unique(),
                default=df['Region'].unique(),
                label_visibility="collapsed"
            )
            
            st.markdown("<div style='margin: 0.75rem 0; height: 1px; background: rgba(99, 102, 241, 0.2);'></div>", unsafe_allow_html=True)
            
            # Time Aggregation Toggle
            st.markdown("<p style='color: #cbd5e1; font-weight: 600; font-size: 0.875rem; margin-bottom: 0.5rem;'>📊 VIEW MODE</p>", unsafe_allow_html=True)
            view_mode = st.selectbox(
                "Select view mode",
                options=["Daily", "Monthly"],
                index=0,
                label_visibility="collapsed"
            )
    
    # Filter data
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range[0], date_range[1]
    else:
        start_date = date_range if not isinstance(date_range, (list, tuple)) else date_range[0] if date_range else df['Order Date'].min()
        end_date = start_date
    
    mask = (
        (df['Order Date'].dt.date >= start_date) &
        (df['Order Date'].dt.date <= end_date) &
        (df['Category'].isin(categories)) &
        (df['Region'].isin(regions))
    )
    filtered_df = df[mask]
    
    # KPI Metrics with modern cards
    st.markdown("<h2 class='section-header-modern'>💼 Key Performance Indicators</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = filtered_df['Sales'].sum()
        prev_sales = df[df['Order Date'].dt.date < date_range[0]]['Sales'].sum()
        sales_growth = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
        
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label-modern">TOTAL SALES</div>
            <div class="metric-value-modern">{format_inr(total_sales)}</div>
            <div class="metric-change {'metric-change-positive' if sales_growth > 0 else 'metric-change-negative'}">
                {'↑' if sales_growth > 0 else '↓'} {abs(sales_growth):.1f}% vs previous
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        total_profit = filtered_df['Profit'].sum()
        profit_margin = (total_profit/total_sales*100) if total_sales > 0 else 0
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label-modern">TOTAL PROFIT</div>
            <div class="metric-value-modern">{format_inr(total_profit)}</div>
            <div class="metric-change metric-change-positive">
                {profit_margin:.1f}% margin
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        avg_order = filtered_df['Sales'].mean()
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label-modern">AVG ORDER VALUE</div>
            <div class="metric-value-modern">{format_inr(avg_order)}</div>
            <div class="metric-subtitle">
                {len(filtered_df):,} orders
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        total_discount = filtered_df['Discount'].sum() * filtered_df['Sales'].sum()
        avg_discount = filtered_df['Discount'].mean() * 100
        st.markdown(f"""
        <div class="metric-card-modern">
            <div class="metric-label-modern">TOTAL DISCOUNT</div>
            <div class="metric-value-modern">{format_inr(total_discount)}</div>
            <div class="metric-change metric-change-negative">
                Avg: {avg_discount:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Modern Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends & Analytics", "📊 Category Insights", "🔮 AI Predictions", "🎯 Smart Insights"])
    
    with tab1:
        st.markdown("<h3 class='section-header-modern'>📈 Sales & Profit Trends</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Sales Trend with enhanced styling - respects view mode
            if view_mode == "Monthly":
                # Group by month
                temp_df = filtered_df.copy()
                temp_df['YearMonth'] = temp_df['Order Date'].dt.to_period('M').dt.to_timestamp()
                sales_data = temp_df.groupby('YearMonth').agg({
                    'Sales': 'sum',
                    'Profit': 'sum'
                }).reset_index()
                x_data = sales_data['YearMonth']
                chart_title = 'Monthly Sales & Profit Trends'
                x_axis_title = 'Month'
            else:
                # Group by day
                sales_data = filtered_df.groupby('Order Date').agg({
                    'Sales': 'sum',
                    'Profit': 'sum'
                }).reset_index()
                x_data = sales_data['Order Date']
                chart_title = 'Daily Sales & Profit Trends'
                x_axis_title = 'Date'
            
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=x_data,
                y=sales_data['Sales'],
                name='Sales',
                line=dict(color='#6366f1', width=3),
                fill='tozeroy',
                fillcolor='rgba(99, 102, 241, 0.15)'
            ))
            
            fig_trend.add_trace(go.Scatter(
                x=x_data,
                y=sales_data['Profit'],
                name='Profit',
                line=dict(color='#a855f7', width=3),
                fill='tozeroy',
                fillcolor='rgba(168, 85, 247, 0.15)'
            ))
            
            fig_trend.update_layout(
                title={
                    'text': chart_title,
                    'font': {'size': 18, 'color': '#f8fafc', 'family': 'Inter'}
                },
                xaxis_title=x_axis_title,
                yaxis_title='Amount (₹)',
                template='plotly_dark',
                hovermode='x unified',
                height=400,
                font=dict(family='Inter', color='#e2e8f0'),
                plot_bgcolor='rgba(15, 23, 42, 0.4)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    gridcolor='rgba(99, 102, 241, 0.1)',
                    zerolinecolor='rgba(99, 102, 241, 0.2)'
                ),
                yaxis=dict(
                    gridcolor='rgba(99, 102, 241, 0.1)',
                    zerolinecolor='rgba(99, 102, 241, 0.2)'
                ),
                legend=dict(
                    bgcolor='rgba(15, 23, 42, 0.6)',
                    bordercolor='rgba(99, 102, 241, 0.3)',
                    borderwidth=1
                )
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Period Summary")
            
            # Top performing period
            if len(sales_data) > 0 and not sales_data.empty:
                best_period = sales_data.loc[sales_data['Sales'].idxmax()]
                period_label = "Best Month" if view_mode == "Monthly" else "Best Day"
                date_col = 'YearMonth' if view_mode == "Monthly" else 'Order Date'
                date_format = '%b %Y' if view_mode == "Monthly" else '%d %b %Y'
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #10b981; margin: 0;">{period_label}</h4>
                    <p style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">
                        {best_period[date_col].strftime(date_format)}
                    </p>
                    <p style="color: #6b7280; margin: 0;">
                        Sales: {format_inr(best_period['Sales'])}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #6b7280; margin: 0;">No Data Available</h4>
                    <p style="color: #9ca3af; margin: 0.5rem 0;">
                        Please adjust your filters
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Growth rate
            min_periods = 2 if view_mode == "Monthly" else 14
            if len(sales_data) > min_periods:
                compare_window = 1 if view_mode == "Monthly" else 7
                recent_avg = sales_data.tail(compare_window)['Sales'].mean()
                older_avg = sales_data.head(compare_window)['Sales'].mean()
                growth = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
                growth_label = "Month-over-Month" if view_mode == "Monthly" else "Weekly Growth"
                growth_desc = "Recent vs Previous" if view_mode == "Monthly" else "Recent vs Previous Week"
                
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #667eea; margin: 0;">{growth_label}</h4>
                    <p style="font-size: 1.5rem; font-weight: 600; margin: 0.5rem 0; 
                       color: {'#10b981' if growth > 0 else '#ef4444'};">
                        {growth:+.1f}%
                    </p>
                    <p style="color: #6b7280; margin: 0; font-size: 0.9rem;">
                        {growth_desc}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Detailed Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales by Category with enhanced design
            cat_sales = filtered_df.groupby('Category').agg({
                'Sales': 'sum',
                'Profit': 'sum',
                'Order ID': 'count'
            }).reset_index().sort_values('Sales', ascending=True)
            
            fig_cat = go.Figure(go.Bar(
                x=cat_sales['Sales'],
                y=cat_sales['Category'],
                orientation='h',
                marker=dict(
                    color=cat_sales['Sales'],
                    colorscale='Purples',
                    showscale=False
                ),
                text=[format_inr(x) for x in cat_sales['Sales']],
                textposition='auto',
            ))
            
            fig_cat.update_layout(
                title='Sales by Category',
                xaxis_title='Sales (₹)',
                yaxis_title='',
                template='plotly_white',
                height=400,
                font=dict(family='Inter'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_cat, use_container_width=True)
        
        with col2:
            # Regional Performance
            region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
            
            fig_region = go.Figure(go.Pie(
                labels=region_sales['Region'],
                values=region_sales['Sales'],
                hole=0.4,
                marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']),
                textinfo='label+percent',
                textfont=dict(size=14, family='Inter')
            ))
            
            fig_region.update_layout(
                title='Regional Distribution',
                template='plotly_white',
                height=400,
                font=dict(family='Inter'),
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_region, use_container_width=True)
        
        # Top Products
        st.markdown("#### 🏆 Top Performing Subcategories")
        top_products = filtered_df.groupby('Sub Category').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count'
        }).reset_index().sort_values('Sales', ascending=False).head(10)
        
        top_products['Sales'] = top_products['Sales'].apply(format_inr)
        top_products['Profit'] = top_products['Profit'].apply(format_inr)
        top_products.columns = ['Subcategory', 'Sales', 'Profit', 'Orders']
        
        st.dataframe(
            top_products,
            use_container_width=True,
            hide_index=True,
            height=400
        )
    
    with tab3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center;'>
            <h2 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 800;'>
                🔮 AI-Powered Sales Predictions
            </h2>
            <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem; font-size: 1.1rem;'>
                Get accurate sales forecasts powered by XGBoost ML
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.98); padding: 2rem; border-radius: 20px; 
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2); margin-bottom: 1.5rem;'>
                <h3 style='color: #667eea; margin: 0 0 1.5rem 0; font-size: 1.8rem; font-weight: 700;'>
                    ⚙️ Configure Prediction Parameters
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            pred_col1, pred_col2, pred_col3 = st.columns(3)
            
            with pred_col1:
                st.markdown("<p style='color: #1e293b; font-weight: 600; margin-bottom: 0.5rem;'>📦 Category</p>", unsafe_allow_html=True)
                pred_category = st.selectbox(
                    "Category",
                    options=df['Category'].unique(),
                    help="Select product category for prediction",
                    label_visibility="collapsed"
                )
            
            with pred_col2:
                st.markdown("<p style='color: #1e293b; font-weight: 600; margin-bottom: 0.5rem;'>📅 Target Date</p>", unsafe_allow_html=True)
                pred_date = st.date_input(
                    "Target Date",
                    value=datetime.now() + timedelta(days=30),
                    min_value=datetime.now(),
                    help="Select future date for prediction",
                    label_visibility="collapsed"
                )
            
            with pred_col3:
                st.markdown("<p style='color: #1e293b; font-weight: 600; margin-bottom: 0.5rem;'>💰 Discount</p>", unsafe_allow_html=True)
                pred_discount = st.slider(
                    "Discount",
                    min_value=0.0,
                    max_value=50.0,
                    value=10.0,
                    step=1.0,
                    help="Set discount percentage",
                    label_visibility="collapsed"
                )
                st.markdown(f"<p style='color: #f093fb; font-weight: 700; font-size: 1.2rem; text-align: center; margin-top: 0.5rem;'>{pred_discount:.0f}%</p>", unsafe_allow_html=True)
            
            # Region selector for prediction
            st.markdown("<p style='color: #1e293b; font-weight: 600; margin: 1rem 0 0.5rem 0;'>🌍 Region</p>", unsafe_allow_html=True)
            pred_region = st.selectbox(
                "Region",
                options=['North', 'South', 'East', 'West', 'Central'],
                help="Select target region",
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Generate AI Prediction", use_container_width=True):
                with st.spinner('🧠 AI is analyzing patterns...'):
                    try:
                        # Calculate historical sales for the selected category and region
                        category_data = df[
                            (df['Category'] == pred_category) & 
                            (df['Region'] == pred_region)
                        ].sort_values('Order Date')
                        
                        # Get last 60 days of sales data for better predictions
                        historical_sales = category_data.groupby('Order Date')['Sales'].sum().tail(60).tolist()
                        
                        # If no historical data, use category average
                        if not historical_sales:
                            category_avg = df[df['Category'] == pred_category]['Sales'].mean()
                            historical_sales = [category_avg] * 30
                        
                        # Check if API is configured
                        if API_URL is None:
                            # Standalone mode: use simple prediction based on historical average
                            avg_sales = np.mean(historical_sales) if historical_sales else df[df['Category'] == pred_category]['Sales'].mean()
                            # Apply discount factor (higher discount typically increases volume slightly)
                            discount_factor = 1 + (pred_discount / 100) * 0.5  # 50% effectiveness
                            pred_sales = avg_sales * discount_factor
                            
                            st.markdown(f"""
                            <div class="prediction-result">
                                <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                                    <div style="font-size: 3rem;">🎯</div>
                                    <h2 style="margin: 0; font-size: 1.8rem; font-weight: 700; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                                        Estimated Sales
                                    </h2>
                                </div>
                                <h1 style="margin: 1rem 0; font-size: 4rem; font-weight: 900; text-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                                    {format_inr(pred_sales)}
                                </h1>
                                <p style="margin: 0; opacity: 0.95; font-size: 1.2rem; font-weight: 500;">
                                    📅 {pred_date.strftime('%d %B %Y')}
                                </p>
                                <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem;">
                                    📦 {pred_category} | 🌍 {pred_region} | 💰 {pred_discount:.0f}% discount
                                </p>
                                <p style="margin: 1rem 0 0 0; opacity: 0.8; font-size: 0.85rem;">
                                    ℹ️ Standalone mode (historical average-based estimation)
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show confidence range based on std dev
                            std_dev = np.std(historical_sales) if len(historical_sales) > 1 else pred_sales * 0.15
                            lower = max(0, pred_sales - 1.96 * std_dev)
                            upper = pred_sales + 1.96 * std_dev
                            
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.98); padding: 2rem; border-radius: 20px; 
                                        box-shadow: 0 10px 40px rgba(0,0,0,0.2); margin-top: 1.5rem; text-align: center;">
                                <h4 style="color: #667eea; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">
                                    📊 Estimated Range
                                </h4>
                                <p style="font-size: 1.6rem; font-weight: 700; margin: 0; 
                                          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                                          -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                                    {format_inr(lower)} - {format_inr(upper)}
                                </p>
                                <p style="color: #6b7280; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                                    Based on historical data variance
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # API mode: use ML model
                            # Prepare prediction request with historical data
                            request_data = {
                                "category": pred_category,
                                "subcategory": df[df['Category'] == pred_category]['Sub Category'].iloc[0],
                                "region": pred_region,
                                "date": pred_date.strftime("%Y-%m-%d"),
                                "discount": pred_discount / 100,
                                "historical_sales": historical_sales
                            }
                            
                            # Call prediction API
                            response = requests.post(
                                f"{API_URL}/predict",
                                json=request_data,
                                timeout=10
                            )
                            
                            if response.status_code == 200:
                                prediction = response.json()
                                pred_sales = prediction['predicted_sales'] * USD_TO_INR
                                
                                st.markdown(f"""
                                <div class="prediction-result-modern">
                                    <div style="position: relative; z-index: 1;">
                                        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                                            <div style="font-size: 3rem;">🎯</div>
                                            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 700;">
                                                Predicted Sales
                                            </h2>
                                        </div>
                                        <div class="prediction-value">{format_inr(pred_sales)}</div>
                                        <p style="margin: 0; opacity: 0.95; font-size: 1.1rem; font-weight: 500;">
                                            📅 {pred_date.strftime('%d %B %Y')}
                                        </p>
                                        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">
                                            📦 {pred_category} | 🌍 {pred_region} | 💰 {pred_discount:.0f}% discount
                                        </p>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if prediction.get('confidence_interval'):
                                    lower = prediction['confidence_interval']['lower'] * USD_TO_INR
                                    upper = prediction['confidence_interval']['upper'] * USD_TO_INR
                                    
                                    st.markdown(f"""
                                    <div class="glass-card-modern" style="margin-top: 1.5rem; text-align: center;">
                                        <h4 style="color: #a78bfa; margin: 0 0 1rem 0; font-size: 1.1rem; font-weight: 600;">
                                            📊 Confidence Range
                                        </h4>
                                        <p style="font-size: 1.6rem; font-weight: 700; margin: 0; 
                                                  background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
                                                  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                                                  background-clip: text;">
                                            {format_inr(lower)} - {format_inr(upper)}
                                        </p>
                                        <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.875rem;">
                                            95% confidence interval based on model accuracy
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="glass-card-modern" style="background: rgba(239, 68, 68, 0.15); 
                                            border: 1px solid rgba(239, 68, 68, 0.3); text-align: center;">
                                    <h3 style="margin: 0; font-size: 1.25rem; color: #f87171;">❌ Prediction Error</h3>
                                    <p style="margin: 0.5rem 0 0 0; color: #fca5a5;">Please check your inputs and try again.</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                    except requests.exceptions.Timeout:
                        st.markdown("""
                        <div class="glass-card-modern" style="background: rgba(251, 191, 36, 0.15); 
                                    border: 1px solid rgba(251, 191, 36, 0.3); text-align: center;">
                            <h3 style="margin: 0; font-size: 1.25rem; color: #fbbf24;">⏱️ Request Timeout</h3>
                            <p style="margin: 0.5rem 0 0 0; color: #fcd34d;">Server is taking too long. Please try again.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except requests.exceptions.ConnectionError:
                        st.markdown("""
                        <div class="glass-card-modern" style="background: rgba(239, 68, 68, 0.15); 
                                    border: 1px solid rgba(239, 68, 68, 0.3); text-align: center;">
                            <h3 style="margin: 0; font-size: 1.25rem; color: #f87171;">🔌 Connection Error</h3>
                            <p style="margin: 0.5rem 0 0 0; color: #fca5a5;">Cannot connect to prediction server. Please ensure the API is running on port 8000.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                                    padding: 2rem; border-radius: 20px; color: white; text-align: center;">
                            <h3 style="margin: 0; font-size: 1.5rem;">❌ Unexpected Error</h3>
                            <p style="margin: 0.5rem 0 0 0;">{str(e)}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 1.5rem; border-radius: 20px; margin-bottom: 1.5rem; text-align: center;
                        box-shadow: 0 10px 40px rgba(245, 87, 108, 0.3);'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem; font-weight: 700;'>
                    💡 Prediction Insights
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Historical average for comparison
            hist_avg = filtered_df[filtered_df['Category'] == pred_category]['Sales'].mean()
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.98); padding: 1.8rem; border-radius: 20px; 
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2); margin-bottom: 1.5rem; text-align: center;'>
                <h4 style='color: #667eea; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;'>
                    📊 Historical Average
                </h4>
                <p style='font-size: 2.2rem; font-weight: 800; margin: 0; 
                          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    {format_inr(hist_avg)}
                </p>
                <p style='color: #6b7280; margin: 0.5rem 0 0 0; font-size: 0.95rem; font-weight: 500;'>
                    for {pred_category}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Discount impact info
            st.markdown("""
            <div style='background: rgba(255,255,255,0.98); padding: 1.8rem; border-radius: 20px; 
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2); margin-bottom: 1.5rem;'>
                <h4 style='color: #764ba2; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;'>
                    💰 Discount Impact
                </h4>
                <p style='font-size: 0.95rem; color: #374151; line-height: 1.6; margin: 0;'>
                    Higher discounts typically increase sales volume but may reduce profit margins.
                    Our AI considers historical patterns to provide accurate predictions.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Model info
            st.markdown("""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        padding: 1.8rem; border-radius: 20px; 
                        box-shadow: 0 10px 40px rgba(56, 239, 125, 0.3);'>
                <h4 style='color: white; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;'>
                    🤖 Model Info
                </h4>
                <p style='font-size: 0.9rem; color: rgba(255,255,255,0.95); line-height: 1.8; margin: 0;'>
                    <strong>Algorithm:</strong> XGBoost<br>
                    <strong>Accuracy:</strong> 99.74% R²<br>
                    <strong>Error Rate:</strong> 1.84% MAPE<br>
                    <strong>Last Updated:</strong> Oct 11, 2025
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🚨 Smart Insights & Anomaly Detection")
        
        # Anomaly Detection
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Calculate anomalies
            daily_sales_anom = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()
            window_size = 7
            daily_sales_anom['MA7'] = daily_sales_anom['Sales'].rolling(window=window_size).mean()
            daily_sales_anom['STD7'] = daily_sales_anom['Sales'].rolling(window=window_size).std()
            daily_sales_anom['Upper'] = daily_sales_anom['MA7'] + (2 * daily_sales_anom['STD7'])
            daily_sales_anom['Lower'] = daily_sales_anom['MA7'] - (2 * daily_sales_anom['STD7'])
            
            daily_sales_anom['Anomaly'] = (
                (daily_sales_anom['Sales'] > daily_sales_anom['Upper']) |
                (daily_sales_anom['Sales'] < daily_sales_anom['Lower'])
            )
            
            fig_anomaly = go.Figure()
            
            # Add confidence band
            fig_anomaly.add_trace(go.Scatter(
                x=daily_sales_anom['Order Date'],
                y=daily_sales_anom['Upper'],
                fill=None,
                mode='lines',
                line=dict(color='rgba(102, 126, 234, 0.2)', width=0),
                showlegend=False,
                name='Upper Bound'
            ))
            
            fig_anomaly.add_trace(go.Scatter(
                x=daily_sales_anom['Order Date'],
                y=daily_sales_anom['Lower'],
                fill='tonexty',
                mode='lines',
                line=dict(color='rgba(102, 126, 234, 0.2)', width=0),
                fillcolor='rgba(102, 126, 234, 0.1)',
                showlegend=False,
                name='Lower Bound'
            ))
            
            # Add actual sales
            fig_anomaly.add_trace(go.Scatter(
                x=daily_sales_anom['Order Date'],
                y=daily_sales_anom['Sales'],
                name='Actual Sales',
                line=dict(color='#667eea', width=3),
                mode='lines'
            ))
            
            # Add moving average
            fig_anomaly.add_trace(go.Scatter(
                x=daily_sales_anom['Order Date'],
                y=daily_sales_anom['MA7'],
                name='7-Day Average',
                line=dict(color='#10b981', width=2, dash='dash')
            ))
            
            # Add anomaly points
            anomalies = daily_sales_anom[daily_sales_anom['Anomaly']]
            fig_anomaly.add_trace(go.Scatter(
                x=anomalies['Order Date'],
                y=anomalies['Sales'],
                mode='markers',
                name='Anomalies',
                marker=dict(color='#ef4444', size=12, symbol='x'),
            ))
            
            fig_anomaly.update_layout(
                title='Anomaly Detection with Statistical Boundaries',
                xaxis_title='Date',
                yaxis_title='Sales (₹)',
                template='plotly_white',
                hovermode='x unified',
                height=450,
                font=dict(family='Inter'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_anomaly, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Anomaly Stats")
            
            anomaly_count = anomalies['Anomaly'].sum() if len(anomalies) > 0 else 0
            
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: #ef4444; margin: 0; font-size: 2rem;">{anomaly_count}</h3>
                <p style="color: #6b7280; margin: 0.5rem 0; font-size: 0.9rem;">Anomalies Detected</p>
            </div>
            """, unsafe_allow_html=True)
            
            if len(anomalies) > 0:
                st.markdown("<br>", unsafe_allow_html=True)
                
                latest_anomaly = anomalies.iloc[-1]
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #667eea; margin: 0;">Latest Anomaly</h4>
                    <p style="font-size: 1.1rem; font-weight: 600; margin: 0.5rem 0;">
                        {latest_anomaly['Order Date'].strftime('%d %b %Y')}
                    </p>
                    <p style="color: #6b7280; margin: 0; font-size: 0.85rem;">
                        Sales: {format_inr(latest_anomaly['Sales'])}<br>
                        Expected: {format_inr(latest_anomaly['MA7'])}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # AI Insights Section
        st.markdown("---")
        st.markdown("#### 🤖 AI-Generated Business Insights")
        
        insights_col1, insights_col2, insights_col3 = st.columns(3)
        
        # Check if filtered data is available
        if len(filtered_df) > 0:
            with insights_col1:
                # Best performing category
                cat_sales = filtered_df.groupby('Category')['Sales'].sum()
                if len(cat_sales) > 0:
                    best_cat = cat_sales.idxmax()
                    best_cat_sales = cat_sales.max()
                    
                    st.markdown(f"""
                    <div class="insight-card-modern">
                        <div class="insight-icon">🏆</div>
                        <div class="insight-title">TOP CATEGORY</div>
                        <div class="insight-value">{best_cat}</div>
                        <div class="insight-subtitle">{format_inr(best_cat_sales)} in sales</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No category data available")
            
            with insights_col2:
                # Discount optimization
                if len(filtered_df) > 0 and filtered_df['Discount'].sum() > 0:
                    avg_discount = filtered_df['Discount'].mean() * 100
                    discount_sales = filtered_df.groupby('Discount')['Sales'].sum()
                    if len(discount_sales) > 0:
                        optimal_discount = discount_sales.idxmax() * 100
                        
                        st.markdown(f"""
                        <div class="insight-card-modern">
                            <div class="insight-icon">💰</div>
                            <div class="insight-title">DISCOUNT SWEET SPOT</div>
                            <div class="insight-value">{optimal_discount:.1f}%</div>
                            <div class="insight-subtitle">Current avg: {avg_discount:.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("No discount data available")
                else:
                    st.info("No discount data available")
            
            with insights_col3:
                # Best region
                region_sales = filtered_df.groupby('Region')['Sales'].sum()
                if len(region_sales) > 0:
                    best_region = region_sales.idxmax()
                    best_region_sales = region_sales.max()
                    
                    st.markdown(f"""
                    <div class="insight-card-modern">
                        <div class="insight-icon">🌍</div>
                        <div class="insight-title">LEADING REGION</div>
                        <div class="insight-value">{best_region}</div>
                        <div class="insight-subtitle">{format_inr(best_region_sales)} in sales</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No region data available")
        else:
            # Show message when no data is available
            st.warning("📊 No data available for the selected filters. Please adjust your date range, categories, or regions.")
    
    # Modern Footer
    st.markdown("<div style='margin: 3rem 0 1rem 0; height: 1px; background: rgba(99, 102, 241, 0.2);'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 2rem; 
                background: rgba(15, 23, 42, 0.6); 
                backdrop-filter: blur(20px);
                border-radius: 16px; 
                border: 1px solid rgba(99, 102, 241, 0.2);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);'>
        <p style='margin: 0; font-size: 0.875rem; color: #cbd5e1; line-height: 1.8;'>
            <strong style='background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%);
                          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                          background-clip: text; font-size: 1rem;'>
                Ecommerce Sales Prediction and Analysis
            </strong><br>
            <span style='color: #94a3b8;'>Powered by XGBoost ML • Real-time Analytics • AI Insights</span><br>
            <span style='color: #64748b; font-size: 0.8rem;'>Built with Streamlit • FastAPI • Python</span><br>
            <span style='color: #475569; font-size: 0.75rem;'>© 2025 E-commerce Analytics Platform. All predictions are AI-generated estimates.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()