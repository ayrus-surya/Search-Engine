from preprocess import process
from biscores import scoring_biword
from Parametric_indexing import metadata_indexer
from tf_idf_indexer import scoring_list_tf_idf
from spell import spellcheck
from datetime import datetime
import pandas as pd
import json


mappings = json.load(open('data/mappings.json'))

def query_parser(query_vec, metadata, top_k):
    ranked_list_biword = scoring_biword(query_vec,top_k)

    ranked_list_metadata = metadata_indexer.getdocs(metadata['month'],metadata['year'],metadata['station'],metadata['show'])

    ranked_list_tf_idf = scoring_list_tf_idf(query_vec, top_k)

    final_ranked_list = combine(ranked_list_biword, ranked_list_metadata, ranked_list_tf_idf, top_k)
    
    return final_ranked_list


def combine(ranked_list_biword, ranked_list_metadata, ranked_list_tf_idf, top_k):
    tf_idf_weight = 0.5
    biword_weight = 0.3
    metadata_weight = 0.7
    final_ranked_dict = dict()
    for doc in ranked_list_biword:
        final_ranked_dict[doc] = biword_weight*ranked_list_biword[doc]
    for doc in ranked_list_tf_idf:
        if final_ranked_dict.get(doc) == None:
            final_ranked_dict[doc] = 0
        final_ranked_dict[doc] += tf_idf_weight*ranked_list_tf_idf[doc]
    for doc in ranked_list_metadata:
        if final_ranked_dict.get(doc) == None:
            final_ranked_dict[doc] = 0
        final_ranked_dict[doc] += metadata_weight*ranked_list_metadata[doc]
    top_k_docs = list(sorted(final_ranked_dict.keys(), key = lambda x: final_ranked_dict[x], reverse = True))
    final_ranked_list = []
    for i in range(min(len(top_k_docs), top_k)):
        final_ranked_list.append((top_k_docs[i], final_ranked_dict[top_k_docs[i]]))   
    return final_ranked_list


def ranking(postin_list,query):
    json_list = list()
    for i in postin_list:
        json_list.append(fetch_document(i[0])['URL'])
    json.dump(json_list,open("out/" + query + '.json','w'))
    
def main(query,metadata):   
    spelling_dict = spellcheck(query)
    if(len(spelling_dict) != 0):
        print("Spelling Error!! Did You mean :-")
        print(spelling_dict)
        exit()

    p_query = process(query)
    res = query_parser(p_query,metadata,100)
    # ranking(res,query)
    return read_data(res)


def read_data(posting_list):
    res = list()
    for docid,score in posting_list:
        d = dict(fetch_document(docid))
        d['Score'] = score
        res.append(d)
    return res

def fetch_document(doc_row_id):
    docid,rowid = doc_row_id.split("_")
    rowid = int(rowid)
    df = pd.read_csv('data/TelevisionNews/' + mappings[docid])
    return df.iloc[rowid - 1]


if __name__ == '__main__':
    metadata = {'month':'','year':'','station':'','show':''}

    query = input('Enter Query - ')
    metadata['month'] = input('Enter Month - ')
    metadata['year'] = input('Enter Year - ')
    metadata['station'] = input('Enter station - ')
    metadata['show'] = input('Enter show name - ')

    start = datetime.now()
    res = main(query,metadata)
    print("Time Taken-",datetime.now()-start)
    print(json.dumps(res, indent=4, sort_keys=True))

