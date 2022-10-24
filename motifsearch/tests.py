import os

from django.test import TestCase
from motifsearch.search import Search

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = CURRENT_DIR + '/test_data'

class SearchTest(TestCase):
    def setUp(self):
        data_path = DATA_DIR + '/test_pep.fasta'
        self._search = Search(data_path)

    def test_all_results(self):
        result = self._search.motif('all', '^M')
        self.assertEqual(len(result), 5)

    def test_RSLYED(self):
        result = self._search.motif('all', 'RSLYED')
        self.assertEqual(len(result), 1)
        res0 = result[0]
        self.assertEqual(res0['peptide_id'], 'SPAC1002.02.1')
        res0_matches = res0['matches']
        self.assertEqual(len(res0_matches), 1)
        match0 = res0_matches[0]
        self.assertEqual(match0['start'], 12)
        self.assertEqual(match0['end'], 17)
        self.assertEqual(match0['match'], 'RSLYED')
        self.assertEqual(match0['before'], 'MASTFSQSVFA')
        self.assertEqual(match0['after'], 'SAENKVDSSKNTEANFPITLPKVLP')

    def test_FdotL(self):
        result = self._search.motif('all', 'F.L')
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]['matches']), 2)
        self.assertEqual(result[0]['matches'][1]['match'], 'FIL')
        self.assertEqual(result[1]['matches'][0]['match'], 'FNL')

    def test_END_dot_start_EDD(self):
        result = self._search.motif('all', 'END.*EDD')
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]['matches']), 1)
        self.assertEqual(result[0]['matches'][0]['match'], 'ENDLEEDD')

    def test_simple_aa_group(self):
        result = self._search.motif('all', 'ZAHZ')
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]['matches']), 1)
        self.assertEqual(result[0]['matches'][0]['match'], 'QAHQ')

    def test_aa_group_class(self):
        result = self._search.motif('all', '[01].[4]7AHZ')
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]['matches']), 1)
        self.assertEqual(result[0]['matches'][0]['match'], 'TGKQAHQ')

    def test_curlies(self):
        result = self._search.motif('all', 'FD{2,3}')
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]['matches']), 1)
        self.assertEqual(result[0]['matches'][0]['match'], 'FDD')
        self.assertEqual(result[0]['matches'][0]['after'], 'LQLTPLQRKLMGLPEGGSTSGKHLT')
        result = self._search.motif('all', 'F{3}I')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['matches'][0]['match'], 'FFFI')
        self.assertEqual(len(result[0]['matches']), 1)

    def test_one_gene(self):
        result = self._search.motif('SPAC1002.02.1', 'VFARSL')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['peptide_id'], 'SPAC1002.02.1')
        self.assertEqual(len(result[0]['matches']), 1)
        self.assertEqual(result[0]['matches'][0]['end'], 14)
        self.assertEqual(result[0]['matches'][0]['before'], 'MASTFSQS')
