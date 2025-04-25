from django.db import models
from account.entity.account import Account
from interview.entity.academic_background import AcademicBackground
from interview.entity.experience_level import ExperienceLevel
from interview.entity.interview_status import InterviewStatus
from interview.entity.interview_topic import InterviewTopic
from interview.entity.project_experience import ProjectExperience
from interview_tech_stack.entity.interview_tech_stack import InterviewTechStack

class Interview(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="interviews")
    topic = models.CharField(
        max_length=50,
        choices=InterviewTopic.choices
    )
    experience_level = models.IntegerField(
        choices=ExperienceLevel.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=InterviewStatus.choices,
        default=InterviewStatus.IN_PROGRESS,
    )
    project_experience  = models.IntegerField(
        choices=ProjectExperience.choices,
    )
    academic_background = models.IntegerField(
        choices=AcademicBackground.choices,
        default=AcademicBackground.NON_MAJOR  # 기본값: 비전공자
    )
    interview_tech_stack = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interview'
        app_label = 'interview'

    def __str__(self):
        return (
            f"Interview(id={self.id}, account={self.account}, topic={self.topic}, "
            f"experience_level={self.experience_level}, status={self.status}, "
            f"project_experience={self.project_experience}, "
            f"academic_background={self.academic_background}, "
            f"interview_tech_stack={self.interview_tech_stack})"
        )

    def getId(self):
        return self.id

    def getAccount(self):
        return self.account

    def getTopic(self):
        return self.topic

    def getExperienceLevel(self):
        return ExperienceLevel(self.experience_level)

    def getStatus(self):
        return self.status

    def getProjectExperience(self):
        return ProjectExperience(self.project_experience)

    def getAcademicBackground(self):
        return AcademicBackground(self.academic_background)

    def getInterviewTechStack(self):
        return InterviewTechStack(self.interview_tech_stack)