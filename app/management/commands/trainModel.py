import sys

from django.core.management.base import BaseCommand

sys.path.append('/Users/ikedamorito/Desktop/Gunosy/assignment')
from utils.train import output_model


# モデルを学習させ、保存
class Command(BaseCommand):
    help = "train NaiveBayes model and output it in pickle format"

    def add_arguments(self, parser):
        '''
        alpha: スムージングの係数
        data_path: 処理済みのデータ(pickle)へのパス
        save_path: 学習させたモデルを保存するパス
        '''
        parser.add_argument('alpha', default=1, type=float)
        parser.add_argument('data_path', type=str)
        parser.add_argument('save_path', default='./pkl_objects/model.pkl', type=str)

    def handle(self, *args, **options):
        output_model(options['alpha'], options['data_path'], options['save_path'])
