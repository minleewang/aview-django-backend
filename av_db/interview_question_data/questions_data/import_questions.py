import pandas as pd
import os
from django.core.management.base import BaseCommand
from interview_question_data.entity.interview_data import InterviewData


class Command(BaseCommand):
    help = '엑셀 파일에서 av_db로 면접 질문 데이터 가져오기'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.abspath(__file__))   # 현재 파일 기준 디렉터리
        file_path = os.path.join(base_dir, '../../../merged_interview_questions.xlsx')
        file_path = os.path.abspath(file_path)   # 파일 정규화

        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            InterviewData.objects.create(
                id=row.get('id', ''),
                category=row.get('category', ''),
                companyName=row.get('companyName', ''),
                question=row.get('question', ''),
                source=row.get('source', '')
            )

        self.stdout.write(self.style.SUCCESS('엑셀 데이터가 av_db에 성공적으로 저장되었습니다.'))