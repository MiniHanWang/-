import importlib,sys
importlib.reload(sys)
from snownlp import SnowNLP
import pandas
import os
def read_dir(path_read):
    files=os.listdir(path_read)
    print(files)
    return files
def read_csv(files,path):
    score_=[]
    for file in files:
        data=pandas.read_csv(path+file,header=None)
        data_pd=pandas.DataFrame(data)
        for i in data.iloc[:,3]:
            s=SnowNLP(str(i))
            score=s.sentiments
            score_.append(score)
    return score_

def save(score,path):
            pandas.DataFrame(score).to_excel(path)
            print(path,"success saved!")
if __name__=="__name__":
    cities = ["保定", "北京", "沧州", "承德", "邯郸", "衡水", "廊坊", "秦皇岛", "石家庄", "唐山", "天津", "邢台", "张家口"]
    path = "E:/projects/jiajia/papaer1-游记/"
    for i in cities:
        files = read_dir(path + str(i))
        score = read_csv(files, path + str(i) + "/")
        save_path = "E:/projects/jiajia/papaer1-游记/" + str(i) + ".xlsx"
        save(score, save_path)
