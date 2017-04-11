import sys

from django.core.management.base import BaseCommand

sys.path.append('/Users/ikedamorito/Desktop/Gunosy/assignment')
from utils.download import get_newsdata


# ニュース記事の取得と解析
class Command(BaseCommand):
    help = "scrape news data and tokenize"

    def add_arguments(self, parser):
        '''
        maxp: Gunosyニュースの各カテゴリページの最大取得ページ数
        save_path: 取得・解析した記事の保存のパス
        dict_path: 使用したいシステム辞書のパス(デフォルトはipadic)
        stopword: SlothLibによるストップワードを使うかどうか
        '''
        parser.add_argument('maxp', type=int)
        parser.add_argument('save_path', type=str)
        parser.add_argument('dict_path', type=str)
        parser.add_argument('stopword', type=bool)

    def handle(self, *args, **options):
        get_newsdata(options['maxp'], options['save_path'], options['dict_path'], options['stopword'])
