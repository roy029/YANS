import csv
import sys
import random
import re
from itertools import chain
from io import BytesIO
import numpy as np
from transformers import AutoTokenizer


# 乱数シードの設定
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)


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

    for to in token:
        if is_hiragana(to) == True:
            if random.random() < ratio:
                token.remove(to)
    new_token = "".join(token)
    return new_token


def main():

    # ss=read_tsv(sys.argv[1],0,1)   
    set_seed(42)
    count=0
    MODEL_NAME = 'google/mt5-small'
    wtitefile = 'kyoudai_goji_40.tsv'

    with open(sys.argv[1], 'r') as f:
        with open(wtitefile,'w') as f2:
            #data = csv.reader(f)
            data = csv.reader(f, delimiter="\t")
            #print('data=',data)
            for line in data:
                #print('line=',line)
                sentence = line[0]
                new_sentence = skip(sentence, 0.40,MODEL_NAME)
                f2.write(new_sentence+'\t'+line[1]+'\n')
                count+=1
                print(count)

main()
