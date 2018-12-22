import os
import re

from django.test import TestCase
from motifsearch.search import Search

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = CURRENT_DIR + '/test_data'

print(CURRENT_DIR)

class SearchTest(TestCase):
    def test_all_results(self):
        search = Search(DATA_DIR + '/test_pep.fasta')
        self.assertEqual(len(search.motif(re.compile('^M'))), 5)
