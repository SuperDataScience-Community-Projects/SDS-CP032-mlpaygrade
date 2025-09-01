# MLPayGrade Advanced Salary Predictor - Hugging Face Spaces Deployment

## 🚀 Quick Deploy to Hugging Face Spaces

This repository contains everything needed to deploy your MLPayGrade salary prediction model on Hugging Face Spaces.

## 📁 Files Structure

```
Deployment Files/
├── app.py                 # Main Gradio app for Hugging Face
├── requirements.txt       # Python dependencies
├── best_model.pkl        # Trained LightGBM model
├── scaler.pkl            # Feature scaler
├── feature_names.json    # Feature names list
├── deployment_functions.pkl  # Feature engineering functions
├── shap_explainer.pkl   # SHAP explainer
└── shap_importance.json # Feature importance rankings
```

## 🎯 Model Information

- **Algorithm**: LightGBM Regressor
- **Features**: 85 Clean Features (No Data Leakage)
- **Performance**: R² = 0.2848, MAE = $44,323.68, RMSE = $64,868.74
- **Data**: 2024 ML/AI Job Market Data
- **Validation**: Honest Performance (Corrected for Data Leakage)

## 🚀 Deployment Steps

### 1. Create Hugging Face Account
- Go to [huggingface.co](https://huggingface.co)
- Sign up for a free account

### 2. Create New Space
- Click "New Space" button
- Choose "Gradio" as the SDK
- Set visibility (Public or Private)
- Choose a license

### 3. Upload Files
- Upload all files from the `Deployment Files/` folder
- Make sure `app.py` is in the root directory
- Upload model files (`*.pkl`, `*.json`)

### 4. Automatic Deployment
- Hugging Face will automatically install dependencies from `requirements.txt`
- The app will be available at: `https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME`

## 🔧 Features

### Job Configuration
- **Job Title**: Data Scientist, ML Engineer, AI Engineer, Data Engineer, Data Analyst
- **Experience Level**: Entry, Mid, Senior, Executive
- **Company Size**: Small (<50), Medium (50-250), Large (>250)
- **Employment Type**: Full-time, Part-time, Contract, Freelance
- **Location**: US, CA, GB, AU, DE, FR, etc.
- **Remote Work**: On-site, Hybrid, Remote

### Model Outputs
- **Predicted Salary**: Annual salary in USD
- **Detailed Explanation**: Feature breakdown and model information
- **What-If Analysis**: Interactive parameter exploration

## 📊 Model Performance

| Metric | Value | Status |
|--------|-------|--------|
| R² Score | 0.2848 | ✅ Honest |
| MAE | $44,323.68 | ✅ Realistic |
| RMSE | $64,868.74 | ✅ Appropriate |
| Data Leakage | None | ✅ Clean |

## 🎯 Key Advantages

1. **No Data Leakage**: All features are legitimate and domain-driven
2. **Honest Performance**: Realistic R² score reflects true predictive power
3. **Clean Architecture**: Proper train-test separation
4. **Domain Knowledge**: Features based on industry understanding
5. **Interactive UI**: User-friendly Gradio interface

## 🔍 Technical Details

### Feature Engineering
- **Ordinal Encodings**: Experience level, company size, employment type
- **Interaction Features**: Experience × Size, Experience × Remote, Size × Remote
- **Geographic Features**: Country-based location encoding
- **Complexity Features**: Job title word count, location diversity

### Model Architecture
- **Algorithm**: LightGBM (Gradient Boosting)
- **Preprocessing**: RobustScaler for feature scaling
- **Validation**: Proper train-test split (no data leakage)
- **Explainability**: SHAP analysis ready

## 🌐 Access Your Deployed App

Once deployed, your app will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/MLPayGrade-Salary-Predictor
```

## 📈 Usage Examples

### Example 1: Senior Data Scientist
- Job Title: "Data Scientist"
- Experience: Senior Level
- Company Size: Large
- Location: US
- Remote: Hybrid
- **Predicted**: ~$180,000

### Example 2: Entry ML Engineer
- Job Title: "ML Engineer"
- Experience: Entry Level
- Company Size: Medium
- Location: CA
- Remote: On-site
- **Predicted**: ~$95,000

## 🎉 Benefits of Hugging Face Deployment

1. **Reliability**: Always available, no local setup needed
2. **Scalability**: Handles multiple users simultaneously
3. **Sharing**: Easy to share with stakeholders
4. **Updates**: Simple to update and redeploy
5. **Professional**: Looks professional for presentations

## 🔧 Troubleshooting

### Common Issues
1. **Model Loading Error**: Ensure all `.pkl` files are uploaded
2. **Dependency Issues**: Check `requirements.txt` compatibility
3. **Memory Limits**: Free tier has 16GB RAM limit
4. **File Size**: Ensure model files are under space limits

### Solutions
1. **Verify Files**: Check all required files are present
2. **Update Dependencies**: Use compatible package versions
3. **Optimize Model**: Reduce model size if needed
4. **Check Logs**: Use Hugging Face logs for debugging

## 📞 Support

For deployment issues:
1. Check Hugging Face documentation
2. Review error logs in your Space
3. Verify all files are properly uploaded
4. Ensure dependencies are compatible

---

**MLPayGrade Advanced Track** - Built with excellence and honesty! 🎯
