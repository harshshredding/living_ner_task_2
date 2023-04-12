import rapidfuzz
import pandas as pd
term_to_ncbi_dict_fuzz_bigger = {}

with open('./names.dmp', 'r') as f:
  for line in f.readlines():
    assert line[-3:] == '\t|\n'
    line = line[:-3]
    splitted_line = line.split('\t|\t')
    ncbi_code = splitted_line[0]
    term = splitted_line[1]
    assert len(splitted_line) == 4
    if term.lower() not in term_to_ncbi_dict_fuzz_bigger:
      term_to_ncbi_dict_fuzz_bigger[term] = ncbi_code

ncbi_atoms_only = []
# Read UMLS ncbi atoms
with open('./umls_ncbi_atoms.lst','r') as f:
  for line in f.readlines():
    line = line.strip()
    code = line.split('|')[0]
    term = line.split('|')[1]
    ncbi_atoms_only.append((code,term))

for code,term in ncbi_atoms_only:
  if term not in term_to_ncbi_dict_fuzz_bigger:
    term_to_ncbi_dict_fuzz_bigger[term] = code

ncbi_all_terms = list(term_to_ncbi_dict_fuzz_bigger.keys())

def get_ncbi_fuzz_bigger(query_string,cutoff):
  max_ratio = 0
  max_term = None
  query_string = query_string
  closest_term = rapidfuzz.process.extractOne(query_string,ncbi_all_terms,score_cutoff=cutoff)
  print(closest_term)
  if closest_term is None:
    return 'OTHER_CODE'
  else:
    return term_to_ncbi_dict_fuzz_bigger[closest_term[0]]