"""
PubMed Fetcher Module

This package provides functionality to fetch research papers from PubMed
based on a user query, and filter results based on non-academic (pharmaceutical/biotech)
author affiliations.

Modules:
- fetch: Handles fetching and filtering PubMed research papers.
- utils: Contains utility functions for processing and saving data.

Author: Meenakshi Vidhyadhar
License: MIT
"""

# Importing the necessary classes and functions from other modules
from .fetch import PubMedFetcher  # Class to fetch and filter PubMed papers
from .helpers import save_to_csv  # Function to save data to CSV

# Defining what will be available when this module is imported
__all__ = ["PubMedFetcher", "save_to_csv"]

# Defining the version of the package
__version__ = "0.1.0"
