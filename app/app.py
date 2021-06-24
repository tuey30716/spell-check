# Import library
from flask import Flask,request, jsonify
from pythainlp import word_tokenize
from pythainlp.corpus.common import thai_words
from pythainlp.util import dict_trie
import deepcut
import pandas as pd
import re
from docx import Document
import json
from pythainlp.spell import NorvigSpellChecker

app = Flask(__name__)


#create_custom_dict 
#by create dict from csv file that contain word to work in tokenize function
#  @param: dict_csv=.csv file name
#  @return:dict with word from .csv file

def create_custom_dict(dict_csv):
  dict_df=pd.read_csv(dict_csv,header=None)

  newdict = []
  newdict.extend(dict_df[0].tolist())

  dict=[word for line in newdict for word in line.split("/")]
  newdict = []
  for i in dict:
      bracket_check=re.sub(r'\([ก-๏\s]+\)',"",i)
      newdict.append(bracket_check.strip())

  custom_dict = set(thai_words())
  for i in newdict:
      custom_dict.add(i)
  return dict_trie(dict_source=custom_dict)


#append_word_to_dict 
#insert new word into .csv file
#  @param: dict_csv=.csv file name, 
#          new_word=word to insert in .csv file(string type)
#  @return: .csv file with new word
def append_word_to_dict(dict_file,new_word):
  dict_df=pd.read_csv(dict_file,header=None)
  if dict_df[0].str.contains(new_word).any():
    return "dict already have this word"
  else:
    new_word_df=pd.DataFrame([new_word])
    dict_df=dict_df.append(new_word_df,ignore_index=True)
    dict_df.to_csv(dict_file, index = False,header=None)
    return "success append word to dict"


#spell_correcting 
#insert new word into .csv file
#  @param: get_text=text to check spell 
#          custom_dict= word dict variable
#  @return: json object of tokenize word and answer 
def spell_correcting(get_text,custom_dict):
  symbol=[' ','”','“','...','‘','’','!','?','ๆ',',','%','-','+']
  tokennize=[]
  tokennize=word_tokenize(get_text, engine="newmm", custom_dict=custom_dict)

  checked_arr=[]
  checker = NorvigSpellChecker(custom_dict=custom_dict)
  for k in tokennize:
    # print(repr(k))
    if '\n' in k:
        k=k.replace('\n','')
    if k in symbol or k.isnumeric():
      # print(True) 
      checked_arr.append(True)
    else:    
        correct=checker.spell(k)
        if len(correct)==1:
            # print(k==correct[0])
            checked_arr.append(k==correct[0])
        else:
            # print(k)
            checked_arr.append(False)

  word_list = pd.DataFrame(
    {'tokennize': tokennize,
    'checked_arr': checked_arr
  })
  # return 0
  return word_list.to_json(orient='records',force_ascii=False, indent=4) 



@app.route('/')
def index():
  return "Hello, World!"


@app.route('/append-dict', methods=['POST'])
def append_dict():
  if request.method == 'POST':
    query_parameters = request.json
    append_word = query_parameters.get('word')
    return jsonify(message=append_word_to_dict('dict_words.csv',append_word))



@app.route('/spell-check', methods=['POST'])
def spell_check():
    if request.method == 'POST':
        query_parameters = request.json
        data = query_parameters.get('text')

        if not (data):
            return page_not_found(404)
        
        return spell_correcting(data,create_custom_dict('dict_words.csv'))
    return page_not_found(404)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(message="can not find resource",
                    status="404")
if __name__ == '__main__':
  app.run("0.0.0.0", port=80, debug=True)
