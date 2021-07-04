from snownlp_sentiment_analysis import read_dir
from snownlp_sentiment_analysis import save
import pandas
def read_excel(files,path):
    score_ = []
    for file in files:
        data = pandas.read_excel(path +"/"+ file, header=None)
        print(file)
        for i in data.iloc[:, 1]:
            score=0
            if i < 0.5:
                score_.append(score)
            else:
                score=1
                score_.append(score)
        save_path = path + "结果1/" + file
        save(score_, save_path)
    return "saved all"
path="E:/projects/jiajia/papaer1-游记/结果/"
data=read_dir(path)
score=read_excel(data,path)

