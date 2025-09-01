#!/usr/bin/env python3
"""
MLPayGrade Hugging Face Deployment Helper
This script helps prepare and upload your model to Hugging Face Spaces
"""

import os
import shutil
import subprocess
import sys

def check_files():
    """Check if all required files are present"""
    required_files = [
        'app.py',
        'requirements.txt',
        'best_model.pkl',
        'scaler.pkl',
        'feature_names.json',
        'deployment_functions.pkl',
        'shap_explainer.pkl',
        'shap_importance.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files are present!")
    return True

def create_deployment_folder():
    """Create a clean deployment folder"""
    deploy_folder = "hf_deployment"
    
    if os.path.exists(deploy_folder):
        shutil.rmtree(deploy_folder)
    
    os.makedirs(deploy_folder)
    
    # Copy all required files
    files_to_copy = [
        'app.py',
        'requirements.txt',
        'best_model.pkl',
        'scaler.pkl',
        'feature_names.json',
        'deployment_functions.pkl',
        'shap_explainer.pkl',
        'shap_importance.json'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, deploy_folder)
            print(f"📁 Copied: {file}")
    
    return deploy_folder

def main():
    print("🚀 MLPayGrade Hugging Face Deployment Helper")
    print("=" * 50)
    
    # Check files
    if not check_files():
        print("\n❌ Please ensure all required files are present before deployment.")
        return
    
    # Create deployment folder
    deploy_folder = create_deployment_folder()
    
    print(f"\n✅ Deployment folder created: {deploy_folder}")
    print("\n📋 Next Steps:")
    print("1. Go to https://huggingface.co/spaces")
    print("2. Click 'Create new Space'")
    print("3. Choose 'Gradio' as SDK")
    print("4. Set Space name (e.g., 'MLPayGrade-Salary-Predictor')")
    print("5. Choose visibility (Public or Private)")
    print("6. Upload all files from the 'hf_deployment' folder")
    print("7. Wait for automatic deployment")
    
    print(f"\n📁 Files ready in: {os.path.abspath(deploy_folder)}")
    print("\n🎯 Your app will be available at:")
    print("   https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME")
    
    # Open deployment folder
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", deploy_folder])
        elif sys.platform == "win32":  # Windows
            subprocess.run(["explorer", deploy_folder])
        else:  # Linux
            subprocess.run(["xdg-open", deploy_folder])
        print(f"\n📂 Opened deployment folder: {deploy_folder}")
    except:
        print(f"\n📂 Deployment folder location: {os.path.abspath(deploy_folder)}")

if __name__ == "__main__":
    main()

