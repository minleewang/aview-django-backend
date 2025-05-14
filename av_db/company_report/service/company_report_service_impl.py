from company_report.repository.company_report_repository_impl import CompanyReportRepositoryImpl
from company_report.service.company_report_service import CompanyReportService
from crawl.repository.crawl_repository_impl import CrawlRepositoryImpl  # 기존 crawl 모듈 재사용

import pandas as pd


class CompanyReportServiceImpl(CompanyReportService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__repository = CompanyReportRepositoryImpl.getInstance()
            cls.__instance.__crawler = CrawlRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCompanyReports(self):
        for source in ["당근", "토스", "원티드", "사람인", "잡플래닛", "잡코리아", "구글-원티드"]:
            try:
                crawled_data = self.__crawler.crawl(source)
                cleaned_data = self.__cleanData(crawled_data)
                self.__repository.createMany(cleaned_data)
            except Exception as e:
                print(f"[Service] Error for {source}: {e}")
        return True

    def getCompanyReports(self):
        return self.__repository.findAll()

    def __cleanData(self, raw_data: list[dict]) -> list[dict]:
        # 필요한 경우 이곳에 데이터 필터링 / 전처리 추가
        for row in raw_data:
            if 'posted_at' in row and isinstance(row['posted_at'], str):
                try:
                    row['posted_at'] = pd.to_datetime(row['posted_at'])
                except Exception as e:
                    print(f"[Service] 날짜 파싱 실패: {row['posted_at']}, 에러: {e}")
                    row['posted_at'] = None
        return raw_data
