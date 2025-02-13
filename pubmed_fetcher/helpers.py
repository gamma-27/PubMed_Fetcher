"""
Utility Functions for PubMed Fetcher

This module includes helper functions for processing and saving data retrieved from PubMed.

Functions:
- extract_non_academic_authors: Filters authors affiliated with pharmaceutical or biotech companies.
- save_to_csv: Saves the extracted paper information to a CSV file.
"""

import csv
from typing import List, Dict


def extract_non_academic_authors(authors: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Filters authors linked to pharmaceutical or biotech companies.

    Args:
        authors (List[Dict[str, str]]): List of authors with their affiliations.

    Returns:
        List[Dict[str, str]]: List of authors with non-academic affiliations.
    """
    academic_keywords = {"university", "hospital", "institute", "college", "research center"}
    industry_keywords = {"pharma", "biotech", "laboratories", "inc.", "corp.", "ltd."}

    non_academic_authors = []
    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        if any(keyword in affiliation for keyword in industry_keywords) and not any(
            keyword in affiliation for keyword in academic_keywords
        ):
            non_academic_authors.append(author)

    return non_academic_authors


def save_to_csv(data: List[Dict[str, str]], filename: str = "output.csv") -> None:
    """
    Saves paper data to a CSV file.

    Args:
        data (List[Dict[str, str]]): List of dictionaries containing paper details.
        filename (str): Name of the output CSV file.
    """
    if not data:
        print("No data to save.")
        return

    fieldnames = ["PubMedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Results successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")
