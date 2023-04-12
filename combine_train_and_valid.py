import pandas as pd
train_path = './training_entities_subtask2.tsv'
train_df = pd.read_csv(train_path, sep='\t',encoding='utf-8-sig')

with open('./training_and_validation_entities_subtask2.tsv', 'w') as f:
  f.write('\t'.join(['filename','mark','label','off0','off1','span','code']))
  for i,row in train_df.iterrows():
    f.write(f"\n{row['filename']}\t{row['mark']}\t{row['label']}\t{row['off0']}\t{row['off1']}\t{row['span']}\t{row['code']}")


valid_path = './validation_entities_subtask2.tsv'
valid_df = pd.read_csv(valid_path, sep='\t',encoding='utf-8-sig')
with open('./training_and_validation_entities_subtask2.tsv', 'a') as f:
  for i,row in valid_df.iterrows():
    f.write(f"\n{row['filename']}\t{row['mark']}\t{row['label']}\t{row['off0']}\t{row['off1']}\t{row['span']}\t{row['NCBITax']}")