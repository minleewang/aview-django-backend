from django.db import models

class InterviewTechStack(models.Model):
    """
    인터뷰에서 사용 가능한 기술스택 항목 정의 모델
    ID는 고정값으로 수동 지정 (API와 연동을 위함)
    """
    id = models.PositiveIntegerField(primary_key=True)  # 고정된 ID로 저장 (예: Node.js = 17)
    name = models.CharField(max_length=50, unique=True)  # 기술스택 이름
    description = models.TextField(blank=True, null=True)  # 선택 설명

    class Meta:
        db_table = "interview_tech_stack"
        app_label = "interview"
        verbose_name = "인터뷰 기술스택"
        verbose_name_plural = "인터뷰 기술스택 목록"

    def __str__(self):
        return self.name
