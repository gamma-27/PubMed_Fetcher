import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import pandas as pd

# Base URL for accessing PubMed via NCBI's E-utilities
NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

class PubMedFetcher:
    def __init__(self, email: str):
        """Initialize with email for API compliance (required by PubMed)."""
        self.email = email

    def search_papers(self, query: str, max_results: int = 20) -> List[str]:
        """Search PubMed using a query and return a list of PubMed IDs."""
        # Parameters for searching PubMed
        params = {
            "db": "pubmed",          # Database: PubMed
            "term": query,           # Search query
            "retmode": "xml",        # Return data in XML format
            "retmax": max_results,   # Maximum number of results to return
            "email": self.email,     # Email for API compliance
        }
        # Send request to PubMed E-utilities
        response = requests.get(f"{NCBI_BASE_URL}/esearch.fcgi", params=params)
        response.raise_for_status()  # Check if request was successful

        # Parse the XML response and extract PubMed IDs
        root = ET.fromstring(response.text)
        return [id_elem.text for id_elem in root.findall(".//Id")]

    def fetch_paper_details(self, pubmed_ids: List[str]) -> List[Dict]:
        """Fetch detailed information for papers using their PubMed IDs."""
        if not pubmed_ids:
            return []  # Return empty list if no PubMed IDs are given

        # Parameters for fetching detailed paper data
        params = {
            "db": "pubmed",
            "id": ",".join(pubmed_ids),  # List of PubMed IDs separated by commas
            "retmode": "xml",            # Return data in XML format
            "email": self.email,         # Email for API compliance
        }
        # Send request to fetch paper details
        response = requests.get(f"{NCBI_BASE_URL}/efetch.fcgi", params=params)
        response.raise_for_status()  # Check if request was successful

        # Parse the XML response to extract paper details
        root = ET.fromstring(response.text)
        papers = []

        # Loop through each article and extract relevant data
        for article in root.findall(".//PubmedArticle"):
            pubmed_id = article.find(".//PMID").text  # PubMed ID
            title = article.find(".//ArticleTitle").text or "N/A"  # Article title
            pub_date = article.find(".//PubDate/Year")
            pub_date = pub_date.text if pub_date is not None else "Unknown"  # Publication year

            # Extract authors, companies, and email
            authors, companies, email = self.extract_authors(article)

            # Store paper details in a dictionary for easy saving to CSV
            papers.append({
                "PubMed ID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-Academic Author(s)": ", ".join(authors) if authors else "N/A",
                "Company Affiliation(s)": ", ".join(companies) if companies else "N/A",
                "Corresponding Author Email": email or "N/A",
            })

        return papers

    def extract_authors(self, article) -> (List[str], List[str], Optional[str]):
        """Extract authors' names, company affiliations, and corresponding author email."""
        authors = []  # List to store non-academic authors
        companies = []  # List to store company affiliations
        email = None  # Initialize email as None

        # Loop through each author in the article
        for author in article.findall(".//Author"):
            name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()  # Author's name
            affiliation = author.findtext(".//AffiliationInfo/Affiliation", "")  # Author's affiliation

            # If the affiliation is non-academic, add the author and company to respective lists
            if self.is_non_academic(affiliation):
                authors.append(name)
                companies.append(affiliation)

            # Get email if available
            if author.find(".//ElectronicAddress") is not None:
                email = author.find(".//ElectronicAddress").text

        return authors, companies, email

    @staticmethod
    def is_non_academic(affiliation: str) -> bool:
        """Check if an author's affiliation is non-academic (e.g., pharmaceutical, biotech)."""
        # Keywords for academic institutions
        academic_keywords = ["university", "college", "institute", "hospital", "school"]
        # Check if affiliation contains non-academic keywords and doesn't contain academic ones
        return any(word in affiliation.lower() for word in ["pharma", "biotech", "corp", "inc"]) and \
               not any(word in affiliation.lower() for word in academic_keywords)

def save_to_csv(papers: List[Dict], filename: str):
    """Save the fetched papers to a CSV file."""
    # Convert the list of paper dictionaries into a pandas DataFrame
    df = pd.DataFrame(papers)
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
