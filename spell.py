import json
len_term = json.load(open('data/len_term.json'))
def editDistDP(str1, str2, wi=2, wd=2, wr=1): 
  m = len(str1)
  n = len(str2)
  dp = [[0 for x in range(n + 1)] for x in range(m + 1)] 
  for i in range(m + 1): 
    for j in range(n + 1):
      if i == 0: 
        dp[i][j] = j  
      elif j == 0: 
        dp[i][j] = i  
      elif str1[i-1] == str2[j-1]: 
        dp[i][j] = dp[i-1][j-1]  
      else: 
        dp[i][j] = min(wi+dp[i][j-1],	 # Insert 
                           wd+dp[i-1][j],	 # Delete 
                           wr+dp[i-1][j-1]) # Replace 
  return dp[m][n]

def spellsuggest(misspell):
  edit_terms = dict()
  if len(misspell)>1:
    for i in range(len(misspell)-1,len(misspell)+2):
      if str(i) in len_term:
        for term in len_term[str(i)]:
          val = editDistDP(misspell, term) 
          if str(val) not in edit_terms:
            edit_terms[str(val)] = set()
          edit_terms[str(val)].add(term)
  if "1" in edit_terms:
    # if "2" in edit_terms:
    #   return list(edit_terms["1"]) + list(edit_terms["2"]) 
    return list(edit_terms["1"])
  elif "2" in edit_terms:
    return list(edit_terms["2"])
  elif "3" in edit_terms:
    return list(edit_terms["3"])
  else:
    return ["no suggestion!"]

def spellcheck(query):
  query = query.lower()
  string = query.replace(',',' ')
  string = string.replace('.', ' ')
  string = string.replace('?', ' ')
  string = string.replace('!', ' ')
  string = string.replace('(', ' ')
  string = string.replace(')', ' ')
  string = string.replace('[', ' ')
  string = string.replace(']', ' ')
  string = string.replace(':', ' ')
  string = string.replace(';', ' ')
  string = string.replace('"', ' ')
  string = string.replace('-', ' ')
  string = string.replace('/', ' ')
  string = string.replace("'", ' ')
  string = string.replace('"', ' ')
  res = dict()
  all_correct = True
  for word in string.split():
    if str(len(word)) in len_term:
      if word in len_term[str(len(word))]:
        continue
      else:
        all_correct = False
        res[word]=spellsuggest(word)
    else:
        all_correct = False
        res[word]=spellsuggest(word)
  if all_correct:
    return dict()
  else:
    return res

# print(spellcheck("angrysdvubuvbuervbbeyrvbueninciwneicnun"))