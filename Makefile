# Makefile

# Variables
PACKAGES_INSTALL = api data_source_plugin-packages data_source_plugin-movies simple_visualizer block-visualizer core
PACKAGES_UNINSTALL = sok-api sok-data-source-packages simple_visualizer block_visualizer sok-core sok-data-source-movies

# Default target
.PHONY: all
all: help

# Help target
.PHONY: help
help:
	@echo "Makefile for managing plugins"
	@echo "Usage:"
	@echo "  make setup - Run setup script based on OS (Linux/Mac: setup.sh, Windows: setup.bat)"
	@echo "  make setup-linux - Run Linux/Mac setup script"
	@echo "  make setup-windows - Run Windows setup script"
	@echo "  make install - Install all packages"
	@echo "  make uninstall - Uninstall all packages"

# Setup targets - detect OS and run appropriate setup script
.PHONY: setup
setup:
	@echo "🚀 Detecting operating system and running setup..."
ifeq ($(OS),Windows_NT)
	@echo "🪟 Windows detected - running setup.bat"
	@cmd /c setup.bat
else
	@echo "🐧 Linux/Mac detected - running setup.sh"
	@chmod +x setup.sh
	@./setup.sh
endif

# Linux/Mac setup target
.PHONY: setup-linux
setup-linux:
	@echo "🐧 Running Linux/Mac setup script..."
	@chmod +x setup.sh
	@./setup.sh

# Windows setup target
.PHONY: setup-windows
setup-windows:
	@echo "🪟 Running Windows setup script..."
	@cmd /c setup.bat

# Install target
.PHONY: install
install:
	@for package in $(PACKAGES_INSTALL); do \
		echo "Installing $$package"; \
		pip install ./$$package; \
	done

# Uninstall target
.PHONY: uninstall
uninstall:
	@echo "Uninstalling packages"
	@for package in $(PACKAGES_UNINSTALL); do \
		echo "Uninstalling $$package"; \
		pip uninstall -y $$package; \
	done

# Clean install
.PHONY: clean-install
clean-install: uninstall install

# Run migrations
.PHONY: migrate
migrate:
	@echo "Running migrations"
	python graph_explorer/manage.py migrate
	@echo "Migrations completed"

# Run server
.PHONY: runserver
runserver:
	@echo "Starting development server"
	python graph_explorer/manage.py runserver 8000

# clean install and run
.PHONY: reset
reset: clean-install runserver
