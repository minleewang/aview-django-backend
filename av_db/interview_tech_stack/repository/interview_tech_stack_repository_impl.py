from interview_tech_stack.entity.interview_tech_stack import InterviewTechStack
from interview_tech_stack.repository.interview_tech_stack_repository import InterviewTechStackRepository

class InterviewTechStackRepositoryImpl(InterviewTechStackRepository):

    def find_all(self):
        return InterviewTechStack.objects.all().order_by("id")
