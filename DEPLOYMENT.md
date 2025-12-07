# Streamlit Cloud Deployment Guide

## 🚀 Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Step-by-Step Deployment

#### 1. Push to GitHub
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Prepare for Streamlit Cloud deployment"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/himayath07/DMart-Analytics-Intelligence-Platform.git

# Push to GitHub
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Fill in the details:
   - **Repository:** `himayath07/DMart-Analytics-Intelligence-Platform`
   - **Branch:** `main`
   - **Main file path:** `src/app.py`
4. Click **"Deploy"**

#### 3. Configure Secrets (Optional)

If you want to enable API predictions, add this to Streamlit Cloud secrets:

1. Go to your app settings
2. Click on **"Secrets"**
3. Add:
```toml
API_URL = "https://your-fastapi-backend.com"
```

### 📦 Files Created for Deployment

- `.streamlit/config.toml` - Streamlit configuration
- `packages.txt` - System-level dependencies
- `DEPLOYMENT.md` - This guide

### 🎯 Deployment Modes

**Standalone Mode (Default)**
- No API backend required
- Uses historical average-based predictions
- Perfect for Streamlit Cloud free tier
- All analytics features work

**API Mode (Optional)**
- Requires FastAPI backend deployed separately
- Set `API_URL` in Streamlit secrets
- Uses XGBoost ML model for predictions
- Deploy backend to: Railway, Render, Heroku, or AWS

### 🔧 Configuration

The app automatically detects deployment mode:
- **No `API_URL`** → Standalone mode (simple predictions)
- **With `API_URL`** → API mode (ML predictions)

### 📊 What Works in Standalone Mode

✅ All analytics dashboards
✅ Interactive visualizations
✅ Category metrics
✅ Regional analysis
✅ Anomaly detection
✅ Historical trends
✅ Basic predictions (average-based)

### 🚨 Troubleshooting

**Issue: App won't start**
- Check `requirements.txt` has all dependencies
- Verify `src/app.py` path is correct
- Check Streamlit Cloud logs

**Issue: Data not loading**
- Ensure CSV file is in `data/` folder
- Check file is committed to GitHub
- Use file uploader if CSV is large (>100MB)

**Issue: Predictions not working**
- In standalone mode, predictions use historical averages
- For ML predictions, deploy FastAPI backend separately

### 🌐 Access Your App

Once deployed, your app will be available at:
```
https://[your-app-name].streamlit.app
```

### 📝 Post-Deployment

1. Share the URL with stakeholders
2. Monitor usage in Streamlit Cloud dashboard
3. Check logs for any errors
4. Update code via git push (auto-deploys)

### 💡 Tips for Best Performance

- Keep CSV file under 100MB for faster loading
- Use `.streamlit/config.toml` for consistent styling
- Enable caching for data loading (already implemented)
- Consider using Streamlit secrets for API keys

### 🔐 Security Notes

- Don't commit `.env` files (already in `.gitignore`)
- Use Streamlit secrets for sensitive data
- Keep API keys out of source code
- Review `.gitignore` before pushing

---

**Need Help?**
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Community Forum](https://discuss.streamlit.io)
