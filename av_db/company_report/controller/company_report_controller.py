from rest_framework import viewsets, status
from django.http import JsonResponse

from company_report.service.company_report_service_impl import CompanyReportServiceImpl


class CompanyReportController(viewsets.ViewSet):
    __service = CompanyReportServiceImpl.getInstance()

    def requestCreateCompanyReports(self, request):
        isSuccess = self.__service.createCompanyReports()
        return JsonResponse({'success': isSuccess})

    def requestCompanyReportList(self, request):
        try:
            reportListDataFrame = self.__service.getCompanyReports()
            print(f"[Controller] companyReportList: {reportListDataFrame}")

            return JsonResponse(reportListDataFrame.to_dict(orient='records'), safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
