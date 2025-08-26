import re
from selenium.webdriver.common.by import By
from time import sleep
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.recruter.tn"
class FromRecruterTnMixin:
    def _extract_data(self, pages=10):
        current_page = 1
        while True:
            max_num_pages, search_results_links = self._get_results_links(search_query=self.keywords, page=1)
            print(f"Processing page {current_page} of {max_num_pages}")
            if current_page > max_num_pages:
                break
            for link in search_results_links:
                self.driver.get(link)
                company_name = self.extract_company_name()
                email = self.extract_email()
                position = self.extract_position()
                job_description = self.extract_job_description()
                yield {
                    "company_name": company_name,
                    "email": email,
                    "position": position,
                    "job_link": link,
                    "job_description": job_description
                }
            current_page += 1
            

    def _get_results_links(self, search_query, page):
        url = 'https://www.recruter.tn/jm-ajax/get_listings/'
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ar-TN;q=0.6,ar;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Priority': 'u=1, i',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.recruter.tn/?search_keywords=angular&search_location'
        }
        data = f'lang=&search_keywords={search_query}&search_location=&per_page=10&orderby=date&order=DESC&page={page}&featured=false&filled=false&show_pagination=true&form_data='

        response = requests.post(url, headers=headers, data=data)


        soup = BeautifulSoup(response.json().get('html'), 'html.parser')
        max_num_pages = response.json().get('max_num_pages')
        job_listings = soup.find_all('li', class_='job_listing')
        return max_num_pages,[job.find('a')['href'] for job in job_listings]
    
    def extract_company_name(self):
        try:
            return self.driver.find_element(By.XPATH, "//div[contains(@class, 'company-info')]//h4").text
        except:
            return "N/A"

    def extract_email(self):
        try:
            email_element = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'libuttonR')]")[1]
            email = email_element.text
            return email
        except:
            try:
                job_description_div = self.driver.find_element(By.CLASS_NAME, "job_description")
                links = job_description_div.find_elements(By.TAG_NAME, 'a')
                email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
                first_email_link = next((link for link in links if email_pattern.match(link.text)), "N/A")
                return first_email_link.text if first_email_link != "N/A" else "N/A"
            except:
                return "N/A"
    
    def extract_position(self):
        try:
            return self.driver.find_element(By.XPATH, "//a[@class='google_map_link']").text
        except:
            return "N/A"
    
    def extract_job_description(self):
        try:
            job_description_div = self.driver.find_element(By.CLASS_NAME, "job_description")
            recomm_jobs_div = job_description_div.find_element(By.XPATH, "./div[last()]")
            all_text = job_description_div.text
            job_description_text = all_text.replace(recomm_jobs_div.text, "").strip()
            return job_description_text
        except:
            return "N/A"