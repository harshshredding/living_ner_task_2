import rapidfuzz
import pandas as pd
term_to_ncbi_dict_fuzz = {}

# Check whether a string has a digit or not
def has_digit(some_string):
  digits = [char for char in some_string if char.isdigit()]
  return len(digits) > 0

# add training data to the dictionary 
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
  if ' y ' in query_string.lower():
    return 'OTHER_CODE'
  # if has_digit(query_string):
  #   return 'OTHER_CODE'
  max_ratio = 0
  max_term = None
  query_string = query_string.lower()
  for term in term_to_ncbi_dict_fuzz:
    # calculate the normalized indel distance
    ratio = rapidfuzz.fuzz.ratio(query_string,term,score_cutoff=cutoff)
    if ratio > max_ratio:
      max_ratio = ratio
      max_term = term
  if max_ratio == 0:
    return 'OTHER_CODE'
  else:
    code = term_to_ncbi_dict_fuzz[max_term]
    if code == '9606':
      return 'OTHER_CODE'
    else:
      return code

pred_path = './validation_predictions_norm.tsv'
pred_df = pd.read_csv(pred_path, sep='\t',encoding='utf-8-sig')

# Only relabel the ones marked OTHER_CODE
with open('./validation_predictions_norm_fuzzed.tsv', 'w') as f:
  f.write('\t'.join(['filename','mark','label','off0','off1','span','NCBITax']))
  for i,row in pred_df.iterrows():
    ncbi_code = row['NCBITax']
    if ncbi_code == 'OTHER_CODE':
      query = row['span']
      ncbi_code = get_ncbi_fuzz(query, 85)
    f.write(f"\n{row['filename']}\t{row['mark']}\t{row['label']}\t{row['off0']}\t{row['off1']}\t{row['span']}\t{ncbi_code}")