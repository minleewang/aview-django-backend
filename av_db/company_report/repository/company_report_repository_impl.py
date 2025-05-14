from company_report.entity.company_report import CompanyReport
from company_report.repository.company_report_repository import CompanyReportRepository

import pandas as pd


class CompanyReportRepositoryImpl(CompanyReportRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createMany(self, reportDataList):
        reportObjects = []
        for data in reportDataList:
            report = CompanyReport(**data)
            report.save()
            reportObjects.append(report)
        return reportObjects

    def findAll(self) -> pd.DataFrame:
        reportList = CompanyReport.objects.all().values()
        return pd.DataFrame(reportList)
