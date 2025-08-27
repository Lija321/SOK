@echo off
REM SOK Project Setup Script for Windows
REM This script sets up the complete development environment

echo 🚀 Starting SOK project setup...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    exit /b 1
)

REM Install requirements
echo 📋 Installing requirements from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    exit /b 1
)

REM Install local packages in development mode
echo 🔧 Installing local packages...
pip install -e ./api
if %errorlevel% neq 0 (
    echo ❌ Failed to install api package
    exit /b 1
)

pip install -e ./core
if %errorlevel% neq 0 (
    echo ❌ Failed to install core package
    exit /b 1
)

pip install -e ./data_source_plugin-movies
if %errorlevel% neq 0 (
    echo ❌ Failed to install data_source_plugin-movies package
    exit /b 1
)

pip install -e ./data_source_plugin-packages
if %errorlevel% neq 0 (
    echo ❌ Failed to install data_source_plugin-packges package
    exit /b 1
)

pip install -e ./block-visualizer
if %errorlevel% neq 0 (
    echo ❌ Failed to install block-visualizer package
    exit /b 1
)

pip install -e ./simple_visualizer
if %errorlevel% neq 0 (
    echo ❌ Failed to install simple_visualizer package
    exit /b 1
)

REM Navigate to Django project directory
echo 🗂️  Navigating to Django project...
cd graph_explorer
if %errorlevel% neq 0 (
    echo ❌ Failed to navigate to graph_explorer directory
    exit /b 1
)

REM Run Django migrations
echo 🗃️  Running Django migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ Failed to run Django migrations
    exit /b 1
)

REM Start Django development server
echo 🌐 Starting Django development server...
echo Server will be available at http://127.0.0.1:8000/
python manage.py runserver
