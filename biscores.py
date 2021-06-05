from preprocess import process
import nltk
import json
# nltk.download('wordnet')
# nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import heapq

lemmatizer = WordNetLemmatizer()
stpwrds = set(stopwords.words('english'))

biwords = json.load(open("data/biwords.json"))

def scoring_biword(query, k):
  string = query
  scores = dict()
  for i in range(len(string)-1):
    word1 = string[i]
    word2 = string[i+1]
    lw1 = lemmatizer.lemmatize(word1.lower())
    lw2 = lemmatizer.lemmatize(word2.lower())
    lw = lw1 + " " + lw2
    if lw in biwords:
      #print("\t",lw)
      for docid in biwords[lw]:
        #print(docid)
        if docid not in scores:
          scores[docid] = 0
        scores[docid] += 1
    else:
      print(lw)
  for docid in scores:
    scores[docid] = scores[docid]/(len(string)-1)
  score_list = []
  for docid in scores:
    score_list.append((-scores[docid],docid))

  heapq.heapify(score_list)
  top_k_scores = dict()
  for i in range(min(k,len(score_list))):
    t = heapq.heappop(score_list)
    top_k_scores[t[1]] = -t[0]

  return top_k_scores