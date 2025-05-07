from abc import ABC, abstractmethod

from interview_result.entity.interview_result import InterviewResult
from interview_result.entity.interview_result_qas import InterviewResultQAS
from interview_result.repository.interview_result_repository import InterviewResultRepository


class InterviewResultRepositoryImpl(InterviewResultRepository):
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

    def registerInterviewResult(self, account):
        InterviewResult.objects.create(account=account)
        interviewResult = InterviewResult.objects.all()
        return interviewResult.last()


    def registerInterviewResultQAS(self, interviewResult, scoreResultList):
        for scoreResult in scoreResultList:
            print(scoreResult)
            question, answer, intent, feedback = scoreResult
            if len(answer) <= 30:
                feedback = '10점<s>답변의 길이가 너무 짧습니다. 질문과 관련한 당신의 구체적인 사례를 언급하여 답변한다면 좋은 점수를 받을 수 있습니다.'
                if any(keyword in answer for keyword in ['모르', '못했', '몰라', '죄송', '모름', '못하']):
                    feedback = '0점<s>답변의 길이가 너무 짧으며, 질문의 의도와 맞지 않습니다. 어려운 질문이라도 최대한 답변할 수 있는 내용을 작성하는 것이 좋습니다.'

            InterviewResultQAS.objects.create(question=question, answer=answer, intent=intent,
                                              feedback=feedback, interview_result=interviewResult)

    def getLastInterviewResult(self,account):
        result = InterviewResult.objects.filter(account=account).order_by('-id').first()
        print(f"▶ getLastInterviewResultByAccount() → {result}")
        return result

    def getLastInterviewResultQASList(self, interviewResult):
        query = InterviewResultQAS.objects.filter(interview_result=interviewResult)
        print(f"▶ QAS count: {query.count()}")  # 0이면 인터뷰에 QAS가 없음

        interviewResultQASList = query.order_by('id').values_list('question', 'answer', 'intent', 'feedback')
        print(f"▶ QAS values_list: {list(interviewResultQASList)}")  # 튜플 리스트로 출력

        return interviewResultQASList

    def saveInterviewResult(self, accountId: int, summary: str, questions: list[str], answers: list[str]):
        try:
            # 1. 면접 결과 저장
            interviewResult = InterviewResult.objects.create(
                account_id=accountId,
                summary=summary
            )

            # 2. 질문/답변 저장 반복
            for q, a in zip(questions, answers):
                intent = "기본"
                feedback = "피드백 없음"

                # 자동 피드백 로직
                if len(a) <= 30:
                    feedback = '10점<s>답변이 짧습니다. 사례 중심으로 구체적으로 설명해보세요.'
                    if any(word in a for word in ['모르', '몰라', '모름', '못했', '죄송']):
                        feedback = '0점<s>질문에 대한 충분한 답변이 없습니다. 최대한 노력해보세요.'

                InterviewResultQAS.objects.create(
                    interview_result=interviewResult,
                    question=q,
                    answer=a,
                    intent=intent,
                    feedback=feedback
                )

            print("✅ 면접 결과 및 QAS 저장 완료")
            return interviewResult

        except Exception as e:
            print(f"❌ 면접 결과 저장 중 오류 발생: {e}")
            raise