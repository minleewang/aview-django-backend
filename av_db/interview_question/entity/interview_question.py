from django.db import models
from interview.entity.interview import Interview

# 면접 질문 도메인 모델 정의
class InterviewQuestion(models.Model):
    id = models.AutoField(primary_key=True)  # 고유 ID
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="questions")  # 어떤 인터뷰에 속한 질문인지
    question_text = models.TextField()  # 질문 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 일시

    class Meta:
        db_table = 'interview_question'
        app_label = 'interview'

    def __str__(self):
        return f"InterviewQuestion(id={self.id}, interview={self.interview.id}, question_text={self.question_text})"