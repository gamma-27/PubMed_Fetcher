PubMed Fetcher
Overview
PubMed Fetcher is a command-line tool that retrieves research papers from PubMed based on a user query. It identifies papers where at least one author is affiliated with a pharmaceutical or biotech company and outputs the results as a CSV file.

Project Organization
Aganitha_DevOps_Internship_Assignment/ │── pubmed_fetcher/ │ ├── init.py # Module initialization │ ├── fetch.py # Fetches and filters PubMed research papers │ ├── helpers.py # Utility functions │── main.py # Command-line interface │── pyproject.toml # Poetry configuration │── README.md # Documentation │── .gitignore # Ignore unnecessary files

yaml
Copy
Edit

---

## Installation
This project uses [Poetry](https://python-poetry.org/) for dependency management.

### Step 1: Install Poetry
If you don’t have Poetry installed, install it using:
```sh
pip install poetry
Step 2: Clone the Repository
sh
Copy
Edit
git clone https://github.com/MeenakshiKVidhyadhar/Aganitha_DevOps_Internship_Assignment.git
cd Aganitha_DevOps_Internship_Assignment
Step 3: Install Dependencies
sh
Copy
Edit
poetry install
Usage
After installing dependencies, you can run the command-line tool.

Basic Usage
sh
Copy
Edit
poetry run get-papers-list "cancer treatment" --email your@email.com
Options
Flag	Description
-h / --help	Show usage instructions.
-d / --debug	Enable debug mode.
-f <filename> / --file <filename>	Save output to a CSV file.
--email <email>	Required: Your email for PubMed API compliance.
Example Usage
sh
Copy
Edit
poetry run get-papers-list "COVID-19 vaccine" --email example@email.com -f results.csv
This will fetch relevant papers and save the output to results.csv.

How It Works
Search for Papers

Queries PubMed using the provided search term.
Retrieves a list of PubMed IDs.
Fetch Paper Details

Extracts title, publication date, authors, affiliations, and email.
Filter Non-Academic Authors

Identifies authors affiliated with pharmaceutical or biotech companies.
Uses heuristics such as domain names (@company.com) and exclusion of academic terms (university, hospital, institute).
Output Results

Displays results in the console or saves them as a CSV file.
Tools & Libraries Used
Tool / Library	Description
PubMed Entrez API	Used to fetch research papers.
Requests	Handles API requests.
Pandas	Processes and saves data in CSV format.
Biopython	Parses PubMed XML responses.
Poetry	Manages dependencies and packaging.
Publishing to TestPyPI
To publish the package to TestPyPI, run:

sh
Copy
Edit
poetry build
poetry publish --repository testpypi
To install the package from TestPyPI:

sh
Copy
Edit
pip install --index-url https://test.pypi.org/simple/ pubmed-fetcher
