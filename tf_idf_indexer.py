import heapq
import pickle 
import json
from BTrees.OOBTree import OOBTree
import heapq
from math import sqrt
from collections import OrderedDict

btree_index = pickle.load(open('data/Btree.pickle','rb'))
 
def generate_query_weights(query_vec):
    query_weights = {}
    norm_term = 0
    for term in set(query_vec):
        idf = btree_index[term][0]
        query_weights[term] = idf
        norm_term += idf*idf
    norm_term = sqrt(norm_term)
    for term in query_weights:
        query_weights[term] = query_weights[term]/norm_term
    return query_weights

def normalize_scores(cosine_scores, doc_weights):
    cosine_scores_normalized_heap = [] 
    for doc in cosine_scores:
        norm_term = 0
        for score in doc_weights[doc]:
            norm_term += score*score 
        norm_term = sqrt(norm_term)
        cosine_scores[doc] = cosine_scores[doc]/norm_term
        heapq.heappush(cosine_scores_normalized_heap, (-cosine_scores[doc], doc))
    return cosine_scores_normalized_heap

def get_top_k_cosine_scores(cosine_scores_normalised, top_k):
    top_k_docs = OrderedDict()
    for i in range(min(top_k, len(cosine_scores_normalised))):
        score_doc_pair = heapq.heappop(cosine_scores_normalised)
        top_k_docs[score_doc_pair[1]] = -1*score_doc_pair[0]
    return top_k_docs

def scoring_list_tf_idf(query_vec, top_k):
    query_weights = generate_query_weights(query_vec)
    doc_weights = dict()
    cosine_scores = dict()
    for term in set(query_vec):
        posting_list = btree_index[term][1]
        for i in range(min(top_k*5, len(posting_list))):
            if(doc_weights.get(posting_list[i][0]) == None):
                doc_weights[posting_list[i][0]] = []
            doc_weights[posting_list[i][0]].append(posting_list[i][1])
            cosine_scores[posting_list[i][0]] = query_weights[term]*posting_list[i][1]
    cosine_scores_normalized = normalize_scores(cosine_scores, doc_weights)
    top_k_docs = get_top_k_cosine_scores(cosine_scores_normalized, top_k)
    return top_k_docs 
