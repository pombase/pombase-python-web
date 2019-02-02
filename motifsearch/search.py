import re

class Search:
    def __init__(self, data_path):
        self.data_path = data_path
        self.peptides = {}
        self.read_data()

    def read_data(self):
        with open(self.data_path, "r") as f:
            lines = f.read().splitlines()

        seq = ''
        gene_name = ''

        for line in lines:
            if line[0] == '>':
                if gene_name != '':
                    seq = re.sub(r"\*$", "", seq)
                    self.peptides.update({gene_name: seq})
                gene_name = re.sub(r':pep$', '', line[1:])
                seq = ''
            else:
                seq += line

        if gene_name != '':
            seq = re.sub(r"\*$", "", seq)
            self.peptides.update({gene_name: seq})

    def motif(self, search_text, max_genes = 20, context = 25):
        """Search all peptides of the regular expression 'search_text'
returning an array like:
    [
         {
             'gene_id': "some_id",
             'matches': [
                 {
                     'start': 100,
                     'end': 110,
                     'match': 'CADR',
                     'before': 'ACDCWDAEIQCSYGWIECVG',
                     'after': 'SAYDLSVHSKATKTPLVVQE'
                 },
                 {
                    ...
                 }
             ]
             'motif_match_count': 4
         },
         {
           ...
         }
    ]
        """
        patt = re.compile(search_text, re.IGNORECASE)

        gene_matches = []

        for key, seq in self.peptides.items():
            pep_res = []
            pep_res_count = 0
            for m in patt.finditer(seq):
                if len(gene_matches) >= max_genes:
                    pep_matches = {
                        'gene_id': key
                    }
                    gene_matches.append(pep_matches)
                    break

                pep_res_count += 1
                if len(pep_res) < 20:
                    before_start = m.start() - context
                    if before_start < 0:
                        before_start = 0
                    hit = {
                        'start': m.start() + 1,
                        'end': m.end(),
                        'match': m.group(),
                        'before': seq[before_start:m.start()],
                        'after': seq[m.end():m.end() + context],
                    }
                    pep_res.append(hit)
                else:
                    break
            if len(pep_res) > 0:
                pep_matches = {
                    'gene_id': key,
                    'matches': pep_res,
                    'match_count': pep_res_count
                }
                gene_matches.append(pep_matches)
        return gene_matches
