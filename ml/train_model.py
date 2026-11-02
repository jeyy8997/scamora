"""Melatih TF-IDF karakter (2-4) + Regresi Logistik, evaluasi di data uji realistis terpisah, ekspor ml/model.json."""
import re, json, pandas as pd, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
SLANG={"dapet":"dapat","norek":"nomor rekening","tf":"transfer","trf":"transfer","dlu":"dulu","udah":"sudah","udh":"sudah","gak":"tidak","ga":"tidak","ngga":"tidak","nggak":"tidak","yg":"yang","dr":"dari","utk":"untuk","jd":"jadi","skrg":"sekarang","krn":"karena","dgn":"dengan","depo":"deposit","hub":"hubungi","sblm":"sebelum","dpt":"dapat","km":"kamu","bgt":"banget","jgn":"jangan","kepilih":"terpilih","ngeklaim":"klaim","no":"nomor"}
def norm(x):
    x=x.lower()
    x=re.sub(r"https?://\S+|bit\.ly/\S+|wa\.me/\S+|t\.me/\S+"," tautan ",x)
    x=re.sub(r"(\d)-(?=\d)",r"\1",x)
    x=re.sub(r"(\d)\s?rb\b",r"\1 ribu",x);x=re.sub(r"(\d)\s?jt\b",r"\1 juta",x)
    x=re.sub(r"\b\d{8,}\b"," nomorpanjang ",x)
    x=re.sub(r"[^a-z0-9 ]"," ",x)
    x=re.sub(r"\b[a-z]+\b",lambda m:SLANG.get(m.group(0),m.group(0)),x)
    return re.sub(r"\s+"," ",x).strip()
if __name__=="__main__":
    tr=pd.read_csv('data/dataset_awasin_v3.csv');te=pd.read_csv('data/test_realistic.csv')
    vec=TfidfVectorizer(analyzer='char_wb',ngram_range=(2,4),sublinear_tf=True,min_df=2,max_features=2500)
    X=vec.fit_transform(tr.teks.map(norm));clf=LogisticRegression(C=10,max_iter=3000).fit(X,tr.label)
    pred=clf.predict(vec.transform(te.teks.map(norm)))
    print(classification_report(te.label,pred,zero_division=0));print(confusion_matrix(te.label,pred,labels=clf.classes_),clf.classes_)
    bs=(te.label!='aman');bp=(pred!='aman');print("Biner scam vs aman: akurasi",(bs==bp).mean(),"| recall scam",(bp[bs]).mean(),"| false alarm aman",(bp[~bs]).mean())
    json.dump({"classes":list(clf.classes_),"vocab":vec.vocabulary_,"idf":[round(float(v),3) for v in vec.idf_],"coef":[[round(float(v),3) for v in r] for r in clf.coef_],"b":[round(float(v),3) for v in clf.intercept_],"slang":SLANG},open('ml/model.json','w'),separators=(',',':'),default=int)
