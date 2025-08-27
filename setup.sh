#!/bin/bash

# SOK Project Setup Script
# This script sets up the complete development environment

set -e  # Exit on any error

echo "🚀 Starting SOK project setup..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📋 Installing requirements from requirements.txt..."
pip install -r requirements.txt

# Install local packages in development mode
echo "🔧 Installing local packages..."
pip install -e ./api
pip install -e ./core
pip install -e ./data_source_plugin-movies
pip install -e ./data_source_plugin-packages
pip install -e ./block-visualizer
pip install -e ./simple_visualizer

# Navigate to Django project directory
cd graph_explorer

# Run Django migrations
echo "🗃️  Running Django migrations..."
python manage.py migrate

# Start Django development server
echo "🌐 Starting Django development server..."
echo "Server will be available at http://127.0.0.1:8000/"
python manage.py runserver
