from driver import Driver
from mixins.from_recruter_tn import FromRecruterTnMixin
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class EmailScraper(Driver, FromRecruterTnMixin):
    def __init__(self, headless=False, keywords="angular", filters=None):
        self.keywords = keywords
        self.filters = filters or []
        super().__init__(headless=headless, keywords=keywords)

    
    def extract_data(self, pages, output_file):
        self._empty_file(output_file)
        for data in self._extract_data(pages=pages):
            valid = True
            for filter in self.filters:
                if not filter.check(data["job_description"]):
                    valid = False
                    logger.info(f"Filtered out job due to filter {filter.__class__.__name__}")
                    break
            if not valid:
                continue
            data.pop("job_description")
            self.append_to_file(output_file, data)
            logger.info(f"stored email: {data['email']}")

    # append to csv file
    def append_to_file(self, filename, data):
        import csv
        import os
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        
    def _empty_file(self, filename):
        import os
        if os.path.isfile(filename):
            os.remove(filename)