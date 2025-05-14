from abc import ABC, abstractmethod

class CrawlRepository(ABC):

    @abstractmethod
    def crawl(self, source: str) -> list[dict]:
        pass
