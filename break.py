import csv
import sys
import random
import re
from itertools import chain
from io import BytesIO
import numpy as np
import torch
from transformers import AutoTokenizer


#TSVファイルの読み込み
def read_tsv(filename,input_id,output_id):
    ss = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter="\t")

        for row in reader:
            ss.append((row[input_id], row[output_id]))
    return ss


# 乱数シードの設定
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

#トークン化
def get_token(text,MODEL_NAME):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokens = tokenizer.tokenize(text)
    tokens = tokens[1:]
    # tokens = [t for t in text.split(' ') if t]
    return tokens


#ひらがな判定
def is_hiragana(value):
    return re.match(r'^[\u3040-\u309F]+$', value) is not None


#欠落
def skip(s:str, ratio,MODEL_NAME):
    token = get_token(s,MODEL_NAME)
    token_idx = [idx for idx in range(len(token))] 
    buffer = []

    for index in token_idx:
        if is_hiragana(token[index]) == True:
            if random.random() < ratio:       # 欠落率
            #buffer.append(token[index]) #4割はトークンをappendしない
                pass
            else:#6割はトークンをappendする
                buffer.append(token[index])
        else:
            buffer.append(token[index])
    buffer = "".join(buffer)
    return buffer


def main():

    ss=read_tsv(sys.argv[1],0,1)
    
    set_seed(42)

    MODEL_NAME = 'google/mt5-small'
    
    wtitefile = 'kyoudai_goji_40.tsv'

    with open(wtitefile,'w') as f2:
        for line in ss:
            sentence = line[0]
            new_sentence = skip(sentence, 0.40,MODEL_NAME)
            f2.write(new_sentence+'\t'+line[1]+'\n')

main()
