import pandas as pd
import json
import os

class ParametricIndex():
    def __init__(self,):
        self.corpus = dict()
        self.month = dict()
        self.year = dict()
        self.station = dict()
        self.show = dict()

    def loadpostinglist(self,file_name):
        data = json.load(open(file_name))
        try:
            self.corpus = data['corpus']
            self.month = data['month']
            self.year = data['year']
            self.station = data['station']
            self.show = data['show']
            # print("Load Success !!")
        except:
            print("Load Failed Build Posting lists Again !!!")


    def buildPostingLists(self,dataset_path = "/home/keshavk/Desktop/AIR/Project/TelevisionNews/",map_file="/home/keshavk/Desktop/AIR/Project/docs.json"):
        mapping = json.load(open(map_file))

        for dno in range(1,1 + len(mapping)):
            try:
                df = pd.read_csv(dataset_path + mapping[str(dno)])
            except:
                print("Unable to readfile",mapping[str(dno)])
                continue
                

            for rno in df.index:
                docrow_id = str(dno) + "_" + str(rno)   
                self.corpus[docrow_id] = 0

                date = df['MatchDateTime'][rno].split()[0]
                m,_,y = map(int,date.split("/"))
                station = df['Station'][rno]
                try:
                    sname = df['Show'][rno].split()
                except AttributeError:
                    sname = []
                    
                self.month[m] = self.month.get(m,[]) 
                self.year[y] = self.year.get(y,[])
                self.station[station] = self.station.get(station,[])

                self.month[m].append(docrow_id)
                self.year[y].append(docrow_id)
                self.station[station].append(docrow_id)

                for name in sname:
                    self.show[name] = self.show.get(name,dict())
                    self.show[name][docrow_id] = 1/len(sname)   
            
            data = {'corpus':self.corpus,'month':self.month,'year' : self.year, 'station' : self.station , 'show': self.show}
            json.dump(data,open('data/ParametricIndex_data.json','w'))




    def getdocs(self,q_month = '', q_year = '', q_station = '', q_show = ''):
        
        res_doc = dict()

        if(q_month != ''):
            try:
                for doc in self.month[q_month]:
                    res_doc[doc] = res_doc.get(doc,0) + 1
            except KeyError:
                pass

        if(q_year != ''):
            try:
                for doc in self.year[q_year]:
                    res_doc[doc] = res_doc.get(doc,0) + 1
            except KeyError:
                pass
                
        if(q_station != ''):
            try:
                for doc in self.station[q_station]:
                    res_doc[doc] = res_doc.get(doc,0) + 1
            except KeyError:
                pass

        if(q_show != ''):
            try:    
                for name in q_show.split():
                    for doc in self.show[name]:
                        res_doc[doc] = res_doc.get(doc,0) + self.show[name][doc]
            except KeyError:
                pass

        return res_doc    

metadata_indexer = ParametricIndex()
metadata_indexer.loadpostinglist('data/ParametricIndex_data.json')
