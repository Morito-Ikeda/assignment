import sys

from django.core.management.base import BaseCommand

sys.path.append('/Users/ikedamorito/Desktop/Gunosy/assignment')
from utils.train import output_model

class Command(BaseCommand):
    help = "train NaiveBayes model and output it in pickle format"

    def add_arguments(self, parser):
        parser.add_argument('alpha', type=int)
        parser.add_argument('data_path', type=str)
        parser.add_argument('save_path', type=str)

    def handle(self, *args, **options):
        output_model(options['alpha'], options['data_path'], options['save_path'])
