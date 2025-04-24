from rest_framework import serializers
from interview_tech_stack.entity.interview_tech_stack import InterviewTechStack

class InterviewTechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewTechStack
        fields = ["id", "name"]
