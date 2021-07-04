from snownlp_sentiment_analysis import read_dir
from snownlp_sentiment_analysis import save
import pandas
def read_save_excel(files,path):
    for file in files:
        score_ = {}
        score_["neg"] = []
        score_["pos"] = []
        score_["sum"] = []
        score_["score_pos_rate"]=[]
        data = pandas.read_excel(path + file)
        print(file)
        score_neg = 0
        score_pos = 0
        for i in data.iloc[:, 1]:
            if i ==1 :
                score_neg+=1
            else:
                score_pos+=1
        score_pos_rate=score_pos/(score_neg+score_pos)
        score_["neg"].append(score_neg)
        score_["pos"].append(score_pos)
        score_["sum"].append(score_neg+score_pos)
        score_["score_pos_rate"].append(score_pos_rate)
        save_path=path+"结果2/"+ file
        save(score_, save_path)
    return "saved all"
path="E:/projects/jiajia/papaer1-游记/结果/结果1/"
data=read_dir(path)
score=read_save_excel(data,path)

