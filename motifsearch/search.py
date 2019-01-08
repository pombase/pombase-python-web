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
                    self.peptides.update({gene_name: seq})
                gene_name = re.sub(r':pep$', '', line[1:])
                seq = ''
            else:
                seq += line

        if gene_name != '':
            self.peptides.update({gene_name: seq})

    def motif(self, search_text, match_count = 20, context = 25):
        """Search all peptides of the regular expression 'patt'
        """
        patt = re.compile(search_text, re.IGNORECASE)
        ret = []
        for key, seq in self.peptides.items():
            if len(ret) < 20:
                pep_res = []
                for m in patt.finditer(seq):
                    if len(pep_res) < match_count:
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
                        'peptide_id': key,
                        'matches': pep_res,
                    }
                    ret.append(pep_matches)
            else:
                break
        return ret
