from django.core.paginator import Paginator
from account.repository.account_repository_impl import AccountRepositoryImpl
from interview.entity.interview import Interview
from interview.entity.interview_status import InterviewStatus
from interview.repository.interview_repository_impl import InterviewRepositoryImpl
from interview.service.interview_service import InterviewService


class InterviewServiceImpl(InterviewService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__interviewRepository = InterviewRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createInterview(self, accountId, jobCategory, experienceLevel):
        foundAccount = self.__accountRepository.findById(accountId)

        if not foundAccount:
            raise Exception("해당 accountId에 해당하는 account를 찾을 수 없습니다.")

        newInterview = Interview(
            account=foundAccount,
            status=InterviewStatus.IN_PROGRESS.value,
            topic=jobCategory.value if hasattr(jobCategory, 'value') else jobCategory,
            experience_level=experienceLevel.value if hasattr(experienceLevel, 'value') else experienceLevel
        )
        print(f"newInterview: {newInterview}")

        savedInterview = self.__interviewRepository.save(newInterview)
        return savedInterview

    def listInterview(self, accountId, page, pageSize):
        try:
            account = self.__accountRepository.findById(accountId)
            if not account:
                raise ValueError(f"Account with ID {accountId} not found.")

            paginatedInterviewList = self.__interviewRepository.findInterviewByAccount(account, page, pageSize)

            total_items = paginatedInterviewList.paginator.count

            interviewDataList = [
                {
                    "id": interview.id,
                    "topic": interview.topic,  # Updated field
                    "yearsOfExperience": interview.yearsOfExperience,  # Updated field
                    "created_at": interview.created_at,  # Included created_at field
                }
                for interview in paginatedInterviewList
            ]

            return interviewDataList, total_items

        except Exception as e:
            print(f"Unexpected error in listInterview: {e}")
            raise

    def removeInterview(self, accountId, interviewId):
        try:
            interview = self.__interviewRepository.findById(interviewId)
            if interview is None or str(interview.account.id) != str(accountId):
                return {
                    "error": "해당 인터뷰를 찾을 수 없거나 소유자가 일치하지 않습니다.",
                    "success": False
                }

            result = self.__interviewRepository.deleteById(interviewId)
            if result:
                return {
                    "success": True,
                    "message": "인터뷰가 삭제되었습니다."
                }

        except Exception as e:
            print(f"Error in InterviewService.removeInterview: {e}")
            return {
                "error": "서버 내부 오류",
                "success": False
            }
