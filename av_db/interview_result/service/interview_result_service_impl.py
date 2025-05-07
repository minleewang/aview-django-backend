from account.repository.account_repository_impl import AccountRepositoryImpl
from interview_result.repository.interview_result_repository_impl import InterviewResultRepositoryImpl
from interview_result.service.interview_result_service import InterviewResultService
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from utility.http_client import HttpClient

import json
class InterviewResultServiceImpl(InterviewResultService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__interviewResultRepository = InterviewResultRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance


    def saveInterviewResult(self, accountId, userToken, summary, questions, answers):
        return  self.__interviewResultRepository.saveInteviewResult(accountId, userToken, summary, questions, answers)

    def getInterviewResult(self, accountId):
        account = self.__accountRepository.findById(accountId)
        print(f"▶ account: {account}")
        interviewResult = self.__interviewResultRepository.getLastInterviewResult(account)
        print(f"▶ interviewResult: {interviewResult}")

        if not interviewResult:
            print("❗️해당 계정의 인터뷰 결과가 없습니다.")
            return []
        interviewResultList = self.__interviewResultRepository.getLastInterviewResultQASList(interviewResult)
        print(f"▶ interviewResultList(raw): {interviewResultList}")
        return interviewResultList

    def getFullQAList(self, interviewId: int) -> tuple[list[str], list[str]]:
        redis = RedisCacheServiceImpl.getInstance()  # 이미 싱글톤 객체로 사용 중

        key = f"interview:{interviewId}:qas"
        raw = redis.getValueByKey(key)

        if not raw:
            raise Exception("Redis에서 Q/A 데이터를 찾을 수 없습니다")

        try:
            qa_list = json.loads(raw)
            questions = [qa["question"] for qa in qa_list]
            answers = [qa["answer"] for qa in qa_list]
            return questions, answers
        except Exception as e:
            print(f"❌ Q/A 복원 실패: {e}")
            raise



