from filters.contains_keywords import ContainsKeywordsFilter
from scraper import EmailScraper


if __name__ == "__main__":
    filter = ContainsKeywordsFilter(["web", "django", "angular"])
    scraper = EmailScraper(headless=True, keywords="angular", filters=[filter])
    scraper.extract_data()
    scraper.quit()