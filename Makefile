# Makefile

# Variables
PACKAGES_INSTALL = ./api
PACKAGES_UNINSTALL = sok-api

# Default target
.PHONY: all
all: help

# Help target
.PHONY: help
help:
	@echo "Makefile for managing plugins"
	@echo "Usage:"
	@echo "  make install - Install all packages"
	@echo "  make uninstall - Uninstall all packages"

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