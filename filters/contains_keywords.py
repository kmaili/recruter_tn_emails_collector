
from abc import abstractmethod
from abc import ABC
import logging
logger = logging.getLogger(__name__)
class Filter(ABC):

    @abstractmethod
    def check(self, text):
        pass

class ContainsKeywordsFilter(Filter):

    def __init__(self, keywords):
        self.keywords = [keyword.lower() for keyword in keywords]

    def check(self, text):
        text_lower = text.lower()
        return any(keyword.strip() in text_lower for keyword in self.keywords)
