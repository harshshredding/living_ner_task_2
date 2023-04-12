import rapidfuzz
import pandas as pd
term_to_ncbi_dict_fuzz = {}

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
    term_to_ncbi_dict_fuzz[term.lower()] = ncbi_code


def get_ncbi_fuzz(query_string,cutoff):
  max_ratio = 0
  max_term = None
  query_string = query_string.lower()
  for term in term_to_ncbi_dict_fuzz:
    ratio = rapidfuzz.fuzz.ratio(query_string,term,score_cutoff=cutoff)
    if ratio > max_ratio:
      max_ratio = ratio
      max_term = term
  if max_ratio == 0:
    return 'OTHER_CODE'
  else:
    return term_to_ncbi_dict_fuzz[max_term]