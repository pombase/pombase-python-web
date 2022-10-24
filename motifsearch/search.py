import regex

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
        self.aa_group_codes_re = regex.compile("([" + aa_group_codes + "])")
        self.brackets_re = regex.compile(r"(\[|\]|\{|\})")

    # substitute AA group codes in the argument
    # if the AA code is outside a character class, substitute a char class
    #   eg. 'CZC' -> 'C[AGS]C'
    # if the code is inside a char class, just substitute
    #   eg. '[CZ]C' -> [CAGS]C'
    def substitute_group_codes(self, text):
        # split by "[" and "]"
        search_text_bits = self.brackets_re.split(text)

        processed_text = ''

        def subst_group_codes_helper(txt, in_class):
            for code, aa_letters in self.aa_group_code_lookup.items():
                sub_re = regex.compile(code, flags=regex.IGNORECASE)
                if in_class:
                    repl_text = aa_letters
                else:
                    repl_text = '[' + aa_letters + ']'

                txt = regex.sub(sub_re, repl_text, txt)

            return txt

        in_class = False
        in_curlies = False

        def open_class():
            nonlocal in_class
            in_class = True

        def close_class():
            nonlocal in_class
            in_class = False

        def open_curly():
            nonlocal in_curlies
            in_curlies = True

        def close_curly():
            nonlocal in_curlies
            in_curlies = False

        table = {
            '[': open_class,
            ']': close_class,
            '{': open_curly,
            '}': close_curly,
        }

        for bit in search_text_bits:
            if bit in table:
                table[bit]()
                processed_text += bit
            else:
                if in_curlies:
                    processed_text += bit
                else:
                    processed_text += subst_group_codes_helper(bit, in_class)

        return processed_text

    def read_data(self):
        with open(self.data_path, "r") as f:
            lines = f.read().splitlines()

        seq = ''
        peptide_id = ''

        for line in lines:
            if line[0] == '>':
                if peptide_id != '':
                    seq = regex.sub(r"\*$", "", seq)
                    self.peptides.update({peptide_id: seq})
                peptide_id = regex.sub(r':pep.*$', '', line[1:])
                seq = ''
            else:
                seq += line

        if peptide_id != '':
            seq = regex.sub(r"\*$", "", seq)
            self.peptides.update({peptide_id: seq})

    def motif(self, scope, search_text, max_genes = 500, context = 25):
        """Search all peptides of the regular expression 'search_text'
returning an array like:
    [
         {
             'peptide_id': "some_id",
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

        patt = regex.compile(processed_search_text, regex.IGNORECASE)

        peptide_matches = []

        def add_match(peptide_id, peptide_matches, seq):
            pep_res = []
            pep_res_count = 0
            for m in patt.finditer(seq, timeout=2):
                if len(peptide_matches) >= max_genes:
                    pep_matches = {
                        'peptide_id': peptide_id
                    }
                    peptide_matches.append(pep_matches)
                    break

                pep_res_count += 1
                if len(pep_res) < 20 or scope != 'all':
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
                    'peptide_id': peptide_id,
                    'matches': pep_res,
                    'match_count': pep_res_count
                }
                peptide_matches.append(pep_matches)

        if scope == 'all':
            for peptide_id, seq in self.peptides.items():
                add_match(peptide_id, peptide_matches, seq)
        else:
            # look up just one ID
            if scope in self.peptides:
                add_match(scope, peptide_matches, self.peptides[scope])

        return peptide_matches
