from fuzzy_match import get_ncbi_fuzz
from exact_match import get_ncbi_exact
from fuzzy_match_bigger_vocab import get_ncbi_fuzz_bigger
import pandas as pd
import sys
import time

pred_path = '/home/claclab/validation_predictions4.tsv'
pred_df = pd.read_csv(pred_path, sep='\t',encoding='utf-8-sig')

with open('/home/claclab/validation_predictions4_exact.tsv', 'w') as f:
  f.write('\t'.join(['filename','mark','label','off0','off1','span','NCBITax']))
  for i,row in pred_df.iterrows():

    query = row['span']
    if row['label'] == 'HUMAN':
      ncbi_code = '9606'
    else:
      ncbi_code = get_ncbi_exact(query)
    f.write(f"\n{row['filename']}\t{row['mark']}\t{row['label']}\t{row['off0']}\t{row['off1']}\t{row['span']}\t{ncbi_code}")

pred_path = '/home/claclab/validation_predictions4_exact.tsv'
pred_df = pd.read_csv(pred_path, sep='\t',encoding='utf-8-sig')

with open('/home/claclab/validation_predictions4_leven.tsv', 'w') as f:
  f.write('\t'.join(['filename','mark','label','off0','off1','span','NCBITax']))
  for i,row in pred_df.iterrows():
    ncbi_code = row['NCBITax']
    if ncbi_code == 'OTHER_CODE':
      query = row['span']
      ncbi_code = get_ncbi_fuzz(query, 85)
    f.write(f"\n{row['filename']}\t{row['mark']}\t{row['label']}\t{row['off0']}\t{row['off1']}\t{row['span']}\t{ncbi_code}")


# pred_path = './validation_predictions_norm_redone_fuzzed.tsv'
# pred_df = pd.read_csv(pred_path, sep='\t',encoding='utf-8-sig')
# with open('./validation_predictions_norm_redone_fuzzed_bigger.tsv', 'w') as f:
#   f.write('\t'.join(['filename','mark','label','off0','off1','span','NCBITax']))
#   for i,row in pred_df.iterrows():
#     ncbi_code = row['NCBITax']
#     if ncbi_code == 'OTHER_CODE':
#       query = row['span']
#       ncbi_code = get_ncbi_fuzz_bigger(query, 91)
#     f.write(f"\n{row['filename']}\t{row['mark']}\t{row['label']}\t{row['off0']}\t{row['off1']}\t{row['span']}\t{ncbi_code}")
