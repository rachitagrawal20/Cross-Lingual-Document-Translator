import json
import re

#computes TF-IDF weights for words in src and trg language documents 
def get_doc_vectors(docA, docB, idf):

  def computeTF(wordDict, bow):
      tfDict = {}
      bowCount = len(bow)
      for word, count in wordDict.items():
          if(count==0):
            tfDict[word] = 0
          else:
            tfDict[word] = 1+math.log10(count)
      return tfDict

  def computeTFIDF(tfBow, idf):
      tfidf = {}
      for word, val in tfBow.items():
          tfidf[word] = val*idf[word]
      return tfidf

  bowA = docA.split()
  bowB = docB.split()
  wordSet = set(bowA).union(set(bowB))
  wordDictA = dict.fromkeys(wordSet, 0) 
  wordDictB = dict.fromkeys(wordSet, 0)

  for word in bowA:
    wordDictA[word]+=1
  for word in bowB:
    wordDictB[word]+=1

  tfBowA = computeTF(wordDictA, bowA)
  tfBowB = computeTF(wordDictB, bowB)
  tfidfBowA = computeTFIDF(tfBowA, idf)
  tfidfBowB = computeTFIDF(tfBowB, idf)

  df = pd.DataFrame([tfidfBowA, tfidfBowB])
  return df.values[0], df.values[1]


#computes IDF values corresonding to all the unique words in every document in corpus
def compute_IDFs(corpus, lang_a, lang_b):

  def compute_IDF(docList):
      idfDict = {}
      word_set = set()
      for sent in docList:
        word_set = word_set.union(set(sent))
      N = len(docList)
      for word in word_set:
          val = 0
          for doc in docList:
            if word in doc:
              val = val+1
          idfDict[word] = math.log10(N / float(val))
      return idfDict

  idfs = {}
  docListA = []
  docListB = []
  for pair in corpus:
    docListA.append(pair[lang_a].split())
    docListB.append(pair[lang_b].split())
  idfs[lang_a] = compute_IDF(docListA)
  idfs[lang_b] = compute_IDF(docListB)
  return idfs

def dump_model(model, filename, idfs = None):
  data = {"model" : model, 
          "idfs" : idfs}
  with open(filename, "w+") as f:
    json.dump(data, f)

def input_json_model(filename):
  json_model = None
  with open(filename, "r") as f:
    json_model = json.load(f)
  return json_model

def show_results(input_json):
  print(input_json["title"])
  print("Corpus Length: " + str(input_json["corpus_size"]) )
  print("Similarity Scores: ")
  print("Cosine Similarity: " + str(input_json["score"]["Cosine"]))
  print("Jaccard Coefficient: " + str(input_json["score"]["Jaccard"]))


def get_corpus(lang_a, infile_a, lang_b, infile_b, sentence_size = None):
    '''
    Load corpus from input file infile_a and infile_b
    '''
    corpus = []
    with open(infile_a, 'r', encoding="utf8") as a, open(infile_b, 'r', encoding="utf8") as b:
            while True:
                try:
                    a_sentence = (next(a)).lower()
                    b_sentence = (next(b)).lower()
                    if(sentence_size is not None and (len(a_sentence) > sentence_size or len(b_sentence) > sentence_size)):
                      continue
                    corpus.append({ 
                        lang_a : a_sentence.rstrip(),
                        lang_b : b_sentence.rstrip()
                        })
                except StopIteration:
                    break
    return corpus

#removes punctuations from the given sentence
def to_normalized_sentence(sentence):
  return re.sub(r"[^\w\d'\s]+",'', sentence)

#preprocess corpus
def preprocess_corpus(corpus, lang_a, lang_b):
  p_corpus = []
  for pair in corpus:
    a_sen = to_normalized_sentence(pair[lang_a])
    b_sen = to_normalized_sentence(pair[lang_b])
    if(a_sen == '' or b_sen == ''):
      continue
    p_pair = {lang_a : a_sen,
              lang_b : b_sen
              }
    p_corpus.append(p_pair)
  return p_corpus

#generates random sample from the imput corpus
def get_sample(input, size, seed):
  random.seed(seed)
  return random.sample(input, size)