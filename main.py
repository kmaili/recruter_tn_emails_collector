from filters.contains_keywords import ContainsKeywordsFilter
from scraper import EmailScraper

import argparse

parser = argparse.ArgumentParser(description="Exemple de params")
parser.add_argument("--query", type=str, help="specify the search query")
parser.add_argument("--pages", type=int, help="number of pages to scrape")
parser.add_argument("--output", type=str, help="output file name")


if __name__ == "__main__":
    args = parser.parse_args()
    if not args.query:
        print("Please provide a search query using --query")
        exit(1)
    if not args.output:
        print("Please provide an output file name using --output")
        exit(1)
    query = args.query
    output_file = args.output
    pages = args.pages if args.pages else 10
    # filter = ContainsKeywordsFilter(["web", "django", "angular"])
    # scraper = EmailScraper(headless=True, keywords=query, filters=[filter])


    scraper = EmailScraper(headless=True, keywords=query)
    scraper.extract_data(pages=pages, output_file=output_file+".csv")
    scraper.quit()