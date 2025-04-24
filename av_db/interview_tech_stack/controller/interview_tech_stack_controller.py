from rest_framework import viewsets
from rest_framework.response import Response
from interview_tech_stack.service.interview_tech_stack_service_impl import InterviewTechStackServiceImpl
from interview_tech_stack.serializer.interview_tech_stack_serializer import InterviewTechStackSerializer

class InterviewTechStackController(viewsets.ViewSet):
    service = InterviewTechStackServiceImpl()

    def requestListInterviewTechStack(self, request):
        stacks = self.service.get_all_tech_stacks()
        serializer = InterviewTechStackSerializer(stacks, many=True)
        return Response(serializer.data)
