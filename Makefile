# Makefile

# Variables
PACKAGES_INSTALL = api data_source_plugin-packages simple_visualizer block-visualizer
PACKAGES_UNINSTALL = sok-api sok-data-source-packages simple_visualizer block_visualizer

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

# Clean install
.PHONY: clean-install
clean-install: uninstall install