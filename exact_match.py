import pandas as pd
term_to_ncbi_dict = {}

#Enhance the dictionary with NCBI file data
with open('./names.dmp', 'r') as f:
  for line in f.readlines():
    assert line[-3:] == '\t|\n'
    line = line[:-3]
    splitted_line = line.split('\t|\t')
    ncbi_code = splitted_line[0]
    term = splitted_line[1]
    assert len(splitted_line) == 4
    if term.lower() not in term_to_ncbi_dict:
      term_to_ncbi_dict[term.lower()] = ncbi_code

ncbi_atoms_only = []
# Read UMLS ncbi atoms
with open('./umls_ncbi_atoms.lst','r') as f:
  for line in f.readlines():
    line = line.strip()
    code = line.split('|')[0]
    term = line.split('|')[1]
    ncbi_atoms_only.append((code,term))

for code,term in ncbi_atoms_only:
  term_to_ncbi_dict[term.lower()] = code


# Enhance the dictionary with training data
ncbi_docs = {}
training_path = './training_entities_subtask2.tsv'
df = pd.read_csv(training_path, sep='\t', encoding='utf-8-sig')
for i,row in df.iterrows():
  ncbi_code = row['code']
  text = row['span']
  terms = ncbi_docs.get(ncbi_code,set())
  terms.add(text)
  ncbi_docs[ncbi_code] = terms
for ncbi_code in ncbi_docs:
  for term in ncbi_docs[ncbi_code]:
    term_to_ncbi_dict[term.lower()] = ncbi_code

def get_ncbi_exact(query_string):
  if query_string.lower() in term_to_ncbi_dict:
    return term_to_ncbi_dict[query_string.lower()]
  return 'OTHER_CODE'