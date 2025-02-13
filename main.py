"""
Command-Line Interface for PubMed Fetcher

This script enables users to retrieve research papers from PubMed using a specific query,
filtering for papers that have non-academic authors (specifically from pharmaceutical or biotech companies),
and saving the results in a CSV format.

Usage:
    poetry run get-papers-list "your search query" --email your@email.com -f results.csv

Options:
    -h, --help       Display help information and exit.
    -d, --debug      Activate debug mode for detailed logging.
    -f, --file       Define the filename to save the results as a CSV.
    --email          Required: Your email address for compliance with PubMed API policies.

Author: Meenakshi K Vidhyadhar
Email: kvidhyadharmeenakshi27@gmail.com
Repository License: MIT License
"""

import argparse
import sys
from pubmed_fetcher.fetch import PubMedFetcher, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Retrieve research papers with non-academic authors from PubMed.")
    parser.add_argument("query", type=str, help="Search term for querying PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("-f", "--file", type=str, help="Filename for saving output as CSV.")
    parser.add_argument("--email", type=str, required=True, help="Your email for PubMed API compliance.")

    args = parser.parse_args()

    fetcher = PubMedFetcher(email=args.email)
    
    if args.debug:
        print(f"Searching for papers with the query: {args.query}")

    pubmed_ids = fetcher.search_papers(args.query)

    if args.debug:
        print(f"Total papers found: {len(pubmed_ids)}.")

    papers = fetcher.fetch_paper_details(pubmed_ids)

    if papers:
        if args.file:
            save_to_csv(papers, args.file)
            print(f"Results have been saved to {args.file}")
        else:
            for paper in papers:
                print(paper)
    else:
        print("No relevant papers were found.")

if __name__ == "__main__":
    main()
