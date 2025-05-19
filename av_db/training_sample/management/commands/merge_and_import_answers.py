from django.core.management.base import BaseCommand
import pandas as pd
import os

from training_sample.utils.merge_answers_data import merge_answer_excels
from training_sample.service.training_sample_service_impl import TrainingSampleServiceImpl

class Command(BaseCommand):
    help = '답변 엑셀 병합 후 training_answers.xlsx로 저장하고 DB에 자동 등록합니다.'

    def handle(self, *args, **kwargs):
        folder_path = "training_sample/data/answers"
        output_file = "training_sample/data/training_answers.xlsx"

        # ✅ 병합
        merge_answer_excels(folder_path, output_file)

        # ✅ 병합된 파일이 실제로 존재하면 등록 수행
        if not os.path.exists(output_file):
            self.stdout.write(self.style.ERROR("❌ 병합된 엑셀 파일이 존재하지 않습니다."))
            return

        try:
            df = pd.read_excel(output_file)
            service = TrainingSampleServiceImpl.getInstance()
            service.import_answers(df)
            self.stdout.write(self.style.SUCCESS(f"✅ 병합 + 등록 완료: {len(df)}개 답변"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"🔥 오류 발생: {e}"))
