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

    def motif(self, patt):
        """Search all peptides of the regular expression 'patt'
        """
        ret = []
        for key, seq in self.peptides.items():
            for m in patt.finditer(seq):
                ret.append(key)
        return ret
