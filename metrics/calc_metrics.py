import json
from queries import Queries
from matplotlib import pyplot as plt


def precision_recall_at_k(retrieved, relevant, k):
    numerator = 0
    for i in range(k):
        if retrieved[i] in relevant:
            numerator += 1
    return (round(numerator / k, 4), round(numerator / len(relevant), 4))


def F1_score_at_k(retrieved, relevant, k):
    p, r = precision_recall_at_k(retrieved, relevant, k)
    return 0 if p == r == 0 else round(2 * p * r / (p + r), 4)


# compute average precision and recall over all queries 
precision = [0] * 1000
recall = [0] * 1000
for query in Queries:
    with open("relevant_results/{}.json".format(query), "r") as openfile1:
        relevant = json.load(openfile1)
    with open("query_results/{}.json".format(query), "r") as openfile2:
        retrieved = json.load(openfile2)

    len_relevant = len(relevant)
    numerator = 0
    for i in range(len(retrieved)):
        if retrieved[i] in relevant:
            numerator += 1
        precision[i] += round(numerator / (i + 1), 4)
        recall[i] += round(numerator / len_relevant, 4)
    for i in range(len(retrieved), 1000):
        recall[i] = recall[i-1]
avg_precision = list(map(lambda p: round(p / len(Queries), 4), precision))
avg_recall = list(map(lambda r: round(r / len(Queries), 4), recall))


# compute mean avereage precision
Map = round(sum(avg_precision) / len(avg_precision), 4)
print("MAP : ", Map)


#compute P@k, R@k and F@k
p = {20: 0, 50: 0, 100: 0, 500: 0, 1000: 0}
r = {20: 0, 50: 0, 100: 0, 500: 0, 1000: 0}
F = {20: 0, 50: 0, 100: 0, 500: 0, 1000: 0}
exclude = {}
for query in Queries:
    with open("relevant_results/{}.json".format(query), "r") as openfile1:
        relevant = json.load(openfile1)
    with open("query_results/{}.json".format(query), "r") as openfile2:
        retrieved = json.load(openfile2)
    len_retrieved = len(retrieved)
    for k in p:
        if len_retrieved >= k :
            pres, rec = precision_recall_at_k(retrieved, relevant, k)
            f = F1_score_at_k(retrieved, relevant, k)
            p[k] += pres
            r[k] += rec
            F[k] += f
        else:
            if k not in exclude:
                exclude[k] = 0
            exclude[k] += 1
for k in p:
    p[k] = round(p[k] / (len(Queries) - exclude[k]), 4)
    r[k] = round(r[k] / (len(Queries) - exclude[k]), 4)
    F[k] = round(F[k] / (len(Queries) - exclude[k]), 4)
print("precision : ", p)
print("recall : ", r)
print("f1 score : ", F)


# plot precision vs recall curve
plt.plot(avg_recall, avg_precision)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision vs Recall Curve")
plt.show()

