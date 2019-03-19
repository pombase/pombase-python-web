import re

class Search:
    def __init__(self, data_path):
        self.data_path = data_path
        self.peptides = {}
        self.read_data()
        self.aa_group_code_lookup = {
            "0": "DE",
            "1": "ST",
            "2": "AGILV",
            "3": "FHWY",
            "4": "KRH",
            "5": "DEHKR",
            "6": "AVILMFYW",
            "7": "KRHDENQ",
            "8": "CDEHKNQRST",
            "9": "ACDGNPSTV",
            "B": "AGS",
            "Z": "ACDEGHKNQRST",
        }
        aa_group_codes = "".join(self.aa_group_code_lookup.keys())
        self.aa_group_codes_re = re.compile("([" + aa_group_codes + "])")
        self.char_class_re = re.compile(r"(\[|\])")

    # substitute AA group codes in the argument
    # if the AA code is outside a character class, substitute a char class
    #   eg. 'CZC' -> 'C[AGS]C'
    # if the code is inside a char class, just substitute
    #   eg. '[CZ]C' -> [CAGS]C'
    def substitute_group_codes(self, text):
        # split by "[" and "]"
        search_text_bits = self.char_class_re.split(text)

        processed_text = ''

        def subst_group_codes_helper(txt, in_class):
            for code, aa_letters in self.aa_group_code_lookup.items():
                sub_re = re.compile(code, flags=re.IGNORECASE)
                if in_class:
                    repl_text = aa_letters
                else:
                    repl_text = '[' + aa_letters + ']'

                txt = re.sub(sub_re, repl_text, txt)

            return txt

        in_class = False
        for bit in search_text_bits:
            if bit == '[':
                in_class = True
                processed_text += bit
            else:
                if bit == ']':
                    in_class = False
                    processed_text += bit
                else:
                    processed_text += subst_group_codes_helper(bit, in_class)

        return processed_text

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

    def motif(self, search_text, max_genes = 100, context = 25):
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

        if self.aa_group_codes_re.search(search_text):
            processed_search_text = self.substitute_group_codes(search_text)
        else:
            processed_search_text = search_text

        patt = re.compile(processed_search_text, re.IGNORECASE)

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
