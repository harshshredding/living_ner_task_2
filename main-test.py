from fuzzy_match import get_ncbi_fuzz
from exact_match import get_ncbi_exact
from fuzzy_match_bigger_vocab import get_ncbi_fuzz_bigger
import pandas as pd
import sys
import time

pred_path = '/home/claclab/harsh/living-ner-submission/claclab-submission-living-ner/task1/0_task1_pred.tsv'
pred_df = pd.read_csv(pred_path, sep='\t',encoding='utf-8-sig')
query_list_1 = []
query_list_2 = []
with open('/home/claclab/harsh/living-ner-submission/claclab-submission-living-ner/task1/test', 'w') as f:
  f.write('\t'.join(['filename','mark','label','off0','off1','span','NCBITax']))
  for i,row in pred_df.iterrows():
    
    query = row['span']
    if row['label'] == 'HUMAN':
      ncbi_code = '9606'
    else:
      ncbi_code = get_ncbi_exact(query)
      if row['filename'] == '32602267_ES':
        print("query",query,"code",ncbi_code)
        query_list_1.append(query=='SARS‐CoV‐2')
        query_list_2.append(query=='SARS-CoV-2')
    f.write(f"\n{row['filename']}\t{row['mark']}\t{row['label']}\t{row['off0']}\t{row['off1']}\t{row['span']}\t{ncbi_code}")

print(query_list_1)
print(query_list_2)
# pred_path = '/home/claclab/harsh/living-ner-submission/1/task2/task2_pred_exact.tsv'
# pred_df = pd.read_csv(pred_path, sep='\t',encoding='utf-8-sig')

# with open('/home/claclab/harsh/living-ner-submission/1/task2/task2_pred_leven.tsv', 'w') as f:
#   f.write('\t'.join(['filename','mark','label','off0','off1','span','NCBITax']))
#   for i,row in pred_df.iterrows():
#     ncbi_code = row['NCBITax']
#     if ncbi_code == 'OTHER_CODE':
#       query = row['span']
#       ncbi_code = get_ncbi_fuzz(query, 85)
#     f.write(f"\n{row['filename']}\t{row['mark']}\t{row['label']}\t{row['off0']}\t{row['off1']}\t{row['span']}\t{ncbi_code}")