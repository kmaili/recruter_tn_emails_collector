from driver import Driver
from mixins.from_recruter_tn import FromRecruterTnMixin


class EmailScraper(Driver, FromRecruterTnMixin):
    def __init__(self, headless=False, keywords="angular", filters=None):
        self.keywords = keywords
        self.filters = filters or []
        super().__init__(headless=headless, keywords=keywords)

    
    def extract_data(self, pages=10):
        self._empty_file("results.csv")
        for data in self._extract_data(pages=pages):
            valid = True
            for filter in self.filters:
                if not filter.check(data["job_description"]):
                    valid = False
                    break
            if not valid:
                continue
            data.pop("job_description")
            self.append_to_file("results.csv", data)

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