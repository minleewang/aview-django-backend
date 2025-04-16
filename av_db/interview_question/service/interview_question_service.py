from abc import ABC, abstractmethod
from interview_question.entity.interview_question import InterviewQuestion

# 질문 관련 비즈니스 로직 인터페이스
class InterviewQuestionService(ABC):

    @abstractmethod
    def saveQuestions(self, interview_id: int, question_list: list) -> list:
        # 질문 리스트 저장 (중복 방지 포함)
        pass

    @abstractmethod
    def getQuestions(self, interview_id: int) -> list:
        # 특정 인터뷰의 질문 목록 조회
        pass