import nltk
# nltk.download('wordnet')
# nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
stpwrds = set(stopwords.words('english'))

def process(query):
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
  string = string.split()
  temp = []
  for word in string:
    if word in stpwrds:
      continue
    temp.append(lemmatizer.lemmatize(word.lower()))
  string = temp
  return string
