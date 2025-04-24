from interview_tech_stack.repository.interview_tech_stack_repository_impl import InterviewTechStackRepositoryImpl
from interview_tech_stack.service.interview_tech_stack_service import InterviewTechStackService

class InterviewTechStackServiceImpl(InterviewTechStackService):

    def __init__(self):
        self.repository = InterviewTechStackRepositoryImpl()

    def get_all_tech_stacks(self):
        return self.repository.find_all()
