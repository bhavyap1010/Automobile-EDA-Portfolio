#!/bin/bash

# Automobile EDA Portfolio - Quick Setup Script
# This script sets up the environment and demonstrates the hybrid approach

echo "🚗 Automobile Market Intelligence - Setup & Demo"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not found."
    echo "Please install pip and try again."
    exit 1
fi

echo "✅ pip found"

# Install requirements
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "Please check requirements.txt and try manually:"
    echo "pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "🎯 Setup Complete! Here's how to use your hybrid portfolio:"
echo ""
echo "FOR BUSINESS STAKEHOLDERS:"
echo "========================="
echo "1. 📄 Executive Summary:"
echo "   open Executive_Summary.md"
echo ""
echo "2. 📊 Business Dashboard:"
echo "   jupyter notebook Business_Dashboard.ipynb"
echo ""
echo "3. 🌐 Interactive Dashboard:"
echo "   streamlit run dashboard_app.py"
echo ""
echo "FOR TECHNICAL TEAMS:"
echo "==================="
echo "1. 🔬 Technical Deep Dive:"
echo "   jupyter notebook Automobile_EDA_Portfolio.ipynb"
echo ""
echo "2. 📋 Complete Documentation:"
echo "   open README.md"
echo ""
echo "🚀 QUICK DEMO - Choose an option:"
echo "================================="
echo ""

# Interactive menu
PS3="Select demo option (1-4): "
options=("Executive Summary" "Business Dashboard" "Interactive Dashboard" "Technical Analysis" "Exit")

select opt in "${options[@]}"
do
    case $opt in
        "Executive Summary")
            echo "📄 Opening Executive Summary..."
            if command -v code &> /dev/null; then
                code Executive_Summary.md
            elif command -v open &> /dev/null; then
                open Executive_Summary.md
            else
                echo "Please open Executive_Summary.md in your text editor"
            fi
            break
            ;;
        "Business Dashboard")
            echo "📊 Starting Business Dashboard..."
            if command -v jupyter &> /dev/null; then
                jupyter notebook Business_Dashboard.ipynb
            else
                echo "Jupyter not found. Please install: pip install jupyter"
            fi
            break
            ;;
        "Interactive Dashboard")
            echo "🌐 Starting Interactive Dashboard..."
            echo "This will open in your web browser at http://localhost:8501"
            echo ""
            if command -v streamlit &> /dev/null; then
                streamlit run dashboard_app.py
            else
                echo "Streamlit not found. Please install: pip install streamlit"
            fi
            break
            ;;
        "Technical Analysis")
            echo "🔬 Opening Technical Analysis..."
            if command -v jupyter &> /dev/null; then
                jupyter notebook Automobile_EDA_Portfolio.ipynb
            else
                echo "Jupyter not found. Please install: pip install jupyter"
            fi
            break
            ;;
        "Exit")
            echo "Setup complete! Refer to README.md for detailed instructions."
            break
            ;;
        *) echo "Invalid option. Please select 1-5.";;
    esac
done

echo ""
echo "🎉 Portfolio ready! Professional hybrid approach deployed successfully."
echo ""
echo "📚 Next Steps:"
echo "   • Review README.md for complete overview and implementation details"
echo "   • Customize content for your specific use case"
echo "   • Explore the interactive dashboard features"
echo ""
echo "🔗 GitHub: Star and share this repository!"
echo "💼 LinkedIn: Add this project to your portfolio!"
