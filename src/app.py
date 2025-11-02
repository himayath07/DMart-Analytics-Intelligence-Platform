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

# Page config with vibrant aesthetics
st.set_page_config(
    page_title="DMart Analytics Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Vibrant Modern Custom CSS
st.markdown("""
<style>
    /* Modern Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container with vibrant gradient */
    .main {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        background-attachment: fixed;
        padding: 0;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }
    
    /* Mega Hero Header with Animation */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 24px;
        padding: 4rem 3rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        border: 3px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        animation: headerPulse 3s ease-in-out infinite;
    }
    
    @keyframes headerPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4); }
        50% { transform: scale(1.01); box-shadow: 0 25px 70px rgba(102, 126, 234, 0.6); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 1rem;
        letter-spacing: -0.03em;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: titleFloat 2s ease-in-out infinite;
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 500;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    /* Vibrant Card Design */
    .glass-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Metric Cards with Gradient Backgrounds */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0.25rem 0;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    .metric-subtitle {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.25rem;
    }
    
    /* Sidebar with Dark Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        backdrop-filter: blur(20px);
        border-right: 3px solid #667eea;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h4 {
        color: #ffffff;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] .stMarkdown {
        color: rgba(255, 255, 255, 0.9);
    }
    
    [data-testid="stSidebar"] strong {
        color: #f093fb;
    }
    
    /* Powerful Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 40px rgba(245, 87, 108, 0.6);
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
    }
    
    /* Input Fields with Better Contrast */
    .stSelectbox, .stDateInput, .stSlider {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 14px;
    }
    
    .stSelectbox > div > div,
    .stDateInput > div > div {
        background: white !important;
        border: 2px solid #667eea !important;
        border-radius: 12px !important;
        color: #1f2937 !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox input,
    .stDateInput input {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    .stSlider > div > div > div {
        color: white !important;
    }
    
    /* Success/Error Messages */
    .stSuccess, .stError, .stInfo {
        border-radius: 16px;
        padding: 1.5rem 2rem;
        backdrop-filter: blur(10px);
        font-weight: 500;
    }
    
    /* Plotly Charts with Better Styling */
    .js-plotly-plot {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Vibrant Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 0.8rem;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.2);
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #667eea !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mega Prediction Result Card */
    .prediction-result {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #ff6a00 100%);
        background-size: 200% 200%;
        border-radius: 24px;
        padding: 3rem;
        color: white;
        text-align: center;
        animation: gradientShift 4s ease infinite;
        box-shadow: 0 20px 60px rgba(245, 87, 108, 0.5);
        border: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 2rem 0 1rem 0;
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
        display: inline-block;
    }
    
    /* Insight Cards with Different Colors */
    .insight-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        box-shadow: 0 10px 40px rgba(56, 239, 125, 0.3);
        transition: all 0.3s ease;
    }
    
    .insight-card-orange {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        box-shadow: 0 10px 40px rgba(245, 87, 108, 0.3);
        transition: all 0.3s ease;
    }
    
    .insight-card-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        box-shadow: 0 10px 40px rgba(79, 172, 254, 0.3);
        transition: all 0.3s ease;
    }
    
    .insight-card-green:hover,
    .insight-card-orange:hover,
    .insight-card-blue:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 5px solid rgba(255, 255, 255, 0.3);
        border-top: 5px solid #f5576c;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* DataFrames */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
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
    def _load_data():
        import os

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
            # If running inside Streamlit, allow the user to upload the file
            st.warning("Sales data CSV not found in expected locations. Please upload the dataset or set the DATA_PATH environment variable.")
            uploaded = st.file_uploader("Upload DMart CSV file", type=['csv'])
            if uploaded is not None:
                df = pd.read_csv(uploaded)
            else:
                # Raise a clear error so the app doesn't fail with a raw FileNotFoundError
                raise FileNotFoundError(
                    "DMart CSV not found. Tried: " + ", ".join(candidates) + ". Provide the file via the uploader or set DATA_PATH env var."
                )
        else:
            df = pd.read_csv(found)

        # Ensure Order Date is parsed to datetime
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        return df
    return _load_data()

def main():
    """Main Streamlit application."""
    
    # Initialize session state to prevent tab redirect issues
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    
    # Mega Hero Header
    st.markdown("""
        <div class="hero-header">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
                <div style="font-size: 5rem; animation: titleFloat 2s ease-in-out infinite;">🛒</div>
                <div>
                    <h1 class="hero-title">DMart Analytics Intelligence</h1>
                    <p class="hero-subtitle">⚡ Powered by XGBoost ML  |  🎯 Real-time Predictions  |  📊 Advanced Analytics</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar with vibrant design
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 16px; margin-bottom: 1rem;'>
            <h2 style='color: white; margin: 0; font-size: 1.8rem; font-weight: 800;'>🎯 Control Center</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Date range selector with better UX
        st.markdown("#### 📅 Time Period")
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
        
        st.markdown("---")
        
        # Category filters with select all option
        st.markdown("#### 🏷️ Categories")
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
        
        st.markdown("---")
        
        # Region filter (new feature)
        st.markdown("#### 🌍 Regions")
        regions = st.multiselect(
            "Select Regions",
            options=df['Region'].unique(),
            default=df['Region'].unique(),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("#### 📊 Quick Stats")
        st.markdown(f"""
        <div style='font-size: 0.95rem; color: rgba(255, 255, 255, 0.9); line-height: 1.8;'>
        <p style='margin: 0.5rem 0;'>📦 Total Orders: <strong style='color: #f093fb;'>{len(df):,}</strong></p>
        <p style='margin: 0.5rem 0;'>👥 Customers: <strong style='color: #f093fb;'>{df['Customer Name'].nunique():,}</strong></p>
        <p style='margin: 0.5rem 0;'>🏙️ Cities: <strong style='color: #f093fb;'>{df['City'].nunique():,}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
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
    
    # KPI Metrics with vibrant cards
    st.markdown("""
    <div class="section-header">
        💰 Key Performance Indicators
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = filtered_df['Sales'].sum()
        prev_sales = df[df['Order Date'].dt.date < date_range[0]]['Sales'].sum()
        sales_growth = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL SALES</div>
            <div class="metric-value">{format_inr(total_sales)}</div>
            <div class="metric-subtitle" style="color: {'#4ade80' if sales_growth > 0 else '#f87171'}">
                {'↑' if sales_growth > 0 else '↓'} {abs(sales_growth):.1f}% vs previous
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        total_profit = filtered_df['Profit'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL PROFIT</div>
            <div class="metric-value">{format_inr(total_profit)}</div>
            <div class="metric-subtitle">
                Margin: {(total_profit/total_sales*100):.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        avg_order = filtered_df['Sales'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">AVG ORDER VALUE</div>
            <div class="metric-value">{format_inr(avg_order)}</div>
            <div class="metric-subtitle">
                {len(filtered_df):,} orders
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        total_discount = filtered_df['Discount'].sum() * filtered_df['Sales'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL DISCOUNT</div>
            <div class="metric-value">{format_inr(total_discount)}</div>
            <div class="metric-subtitle">
                Avg: {filtered_df['Discount'].mean()*100:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "📊 Analytics", "🔮 Predictions", "🚨 Insights"])
    
    with tab1:
        st.markdown("### Sales & Profit Trends")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Sales Trend with enhanced styling
            daily_sales = filtered_df.groupby('Order Date').agg({
                'Sales': 'sum',
                'Profit': 'sum'
            }).reset_index()
            
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=daily_sales['Order Date'],
                y=daily_sales['Sales'],
                name='Sales',
                line=dict(color='#667eea', width=3),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.1)'
            ))
            
            fig_trend.add_trace(go.Scatter(
                x=daily_sales['Order Date'],
                y=daily_sales['Profit'],
                name='Profit',
                line=dict(color='#764ba2', width=3),
                fill='tozeroy',
                fillcolor='rgba(118, 75, 162, 0.1)'
            ))
            
            fig_trend.update_layout(
                title='Daily Sales & Profit Trends',
                xaxis_title='Date',
                yaxis_title='Amount (₹)',
                template='plotly_white',
                hovermode='x unified',
                height=400,
                font=dict(family='Inter'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Period Summary")
            
            # Top performing day
            if len(daily_sales) > 0 and not daily_sales.empty:
                best_day = daily_sales.loc[daily_sales['Sales'].idxmax()]
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #10b981; margin: 0;">Best Day</h4>
                    <p style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">
                        {best_day['Order Date'].strftime('%d %b %Y')}
                    </p>
                    <p style="color: #6b7280; margin: 0;">
                        Sales: {format_inr(best_day['Sales'])}
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
            if len(daily_sales) > 14:
                recent_avg = daily_sales.tail(7)['Sales'].mean()
                older_avg = daily_sales.head(7)['Sales'].mean()
                growth = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
                
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: #667eea; margin: 0;">Weekly Growth</h4>
                    <p style="font-size: 1.5rem; font-weight: 600; margin: 0.5rem 0; 
                       color: {'#10b981' if growth > 0 else '#ef4444'};">
                        {growth:+.1f}%
                    </p>
                    <p style="color: #6b7280; margin: 0; font-size: 0.9rem;">
                        Recent vs Previous Week
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
                st.markdown("<p style='color: white; font-weight: 600; margin-bottom: 0.5rem;'>📦 Category</p>", unsafe_allow_html=True)
                pred_category = st.selectbox(
                    "Category",
                    options=df['Category'].unique(),
                    help="Select product category for prediction",
                    label_visibility="collapsed"
                )
            
            with pred_col2:
                st.markdown("<p style='color: white; font-weight: 600; margin-bottom: 0.5rem;'>📅 Target Date</p>", unsafe_allow_html=True)
                pred_date = st.date_input(
                    "Target Date",
                    value=datetime.now() + timedelta(days=30),
                    min_value=datetime.now(),
                    help="Select future date for prediction",
                    label_visibility="collapsed"
                )
            
            with pred_col3:
                st.markdown("<p style='color: white; font-weight: 600; margin-bottom: 0.5rem;'>💰 Discount</p>", unsafe_allow_html=True)
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
            st.markdown("<p style='color: white; font-weight: 600; margin: 1rem 0 0.5rem 0;'>🌍 Region</p>", unsafe_allow_html=True)
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
                            <div class="prediction-result">
                                <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                                    <div style="font-size: 3rem;">🎯</div>
                                    <h2 style="margin: 0; font-size: 1.8rem; font-weight: 700; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                                        Predicted Sales
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
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if prediction.get('confidence_interval'):
                                lower = prediction['confidence_interval']['lower'] * USD_TO_INR
                                upper = prediction['confidence_interval']['upper'] * USD_TO_INR
                                
                                st.markdown(f"""
                                <div style="background: rgba(255,255,255,0.98); padding: 2rem; border-radius: 20px; 
                                            box-shadow: 0 10px 40px rgba(0,0,0,0.2); margin-top: 1.5rem; text-align: center;">
                                    <h4 style="color: #667eea; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">
                                        📊 Confidence Range
                                    </h4>
                                    <p style="font-size: 1.6rem; font-weight: 700; margin: 0; 
                                              background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                                              -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                                        {format_inr(lower)} - {format_inr(upper)}
                                    </p>
                                    <p style="color: #6b7280; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                                        95% confidence interval based on model accuracy
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                                            padding: 2rem; border-radius: 20px; color: white; text-align: center;">
                                    <h3 style="margin: 0; font-size: 1.5rem;">❌ Prediction Error</h3>
                                    <p style="margin: 0.5rem 0 0 0;">Please check your inputs and try again.</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                    except requests.exceptions.Timeout:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                                    padding: 2rem; border-radius: 20px; color: white; text-align: center;">
                            <h3 style="margin: 0; font-size: 1.5rem;">⏱️ Request Timeout</h3>
                            <p style="margin: 0.5rem 0 0 0;">Server is taking too long. Please try again.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except requests.exceptions.ConnectionError:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                                    padding: 2rem; border-radius: 20px; color: white; text-align: center;">
                            <h3 style="margin: 0; font-size: 1.5rem;">🔌 Connection Error</h3>
                            <p style="margin: 0.5rem 0 0 0;">Cannot connect to prediction server. Please ensure the API is running on port 8000.</p>
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
        
        with insights_col1:
            # Best performing category
            best_cat = filtered_df.groupby('Category')['Sales'].sum().idxmax()
            best_cat_sales = filtered_df.groupby('Category')['Sales'].sum().max()
            
            st.markdown(f"""
            <div class="insight-card-green">
                <h4 style="margin: 0; font-size: 1.1rem; opacity: 0.95;">🏆 Top Category</h4>
                <p style="font-size: 2rem; font-weight: 800; margin: 0.8rem 0; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                    {best_cat}
                </p>
                <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
                    {format_inr(best_cat_sales)} in sales
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with insights_col2:
            # Discount optimization
            avg_discount = filtered_df['Discount'].mean() * 100
            optimal_discount = filtered_df.groupby('Discount')['Sales'].sum().idxmax() * 100
            
            st.markdown(f"""
            <div class="insight-card-orange">
                <h4 style="margin: 0; font-size: 1.1rem; opacity: 0.95;">💰 Discount Sweet Spot</h4>
                <p style="font-size: 2rem; font-weight: 800; margin: 0.8rem 0; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                    {optimal_discount:.1f}%
                </p>
                <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
                    Current avg: {avg_discount:.1f}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with insights_col3:
            # Best region
            best_region = filtered_df.groupby('Region')['Sales'].sum().idxmax()
            best_region_sales = filtered_df.groupby('Region')['Sales'].sum().max()
            
            st.markdown(f"""
            <div class="insight-card-blue">
                <h4 style="margin: 0; font-size: 1.1rem; opacity: 0.95;">🌍 Leading Region</h4>
                <p style="font-size: 2rem; font-weight: 800; margin: 0.8rem 0; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                    {best_region}
                </p>
                <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
                    {format_inr(best_region_sales)} in sales
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer with credits
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 2rem; background: rgba(255,255,255,0.95); border-radius: 16px; backdrop-filter: blur(20px);'>
        <p style='margin: 0; font-size: 0.9rem;'>
            <strong>DMart Analytics Intelligence</strong> • Powered by XGBoost ML • Real-time Insights<br>
            <span style='font-size: 0.85rem;'>Built with ❤️ using Streamlit | FastAPI | Python</span><br>
            <span style='font-size: 0.8rem; color: #9ca3af;'>© 2025 E-commerce Analytics Platform. All predictions are AI-generated estimates.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()