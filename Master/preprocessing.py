import pandas as pd
import string
import sys
if sys.argv[1]=="labelled_data_train.csv":
    var="train"
else:
    var="test"
df = pd.read_csv(sys.argv[1])
f = open('./other_text_files/verbs4.txt')
verbs = []
for i in f.readlines():
    verbs.append(i.strip().lower())
remove_list = []
for i in range(len(df)):
    for j in (df.loc[i][0].split()):
        if(j in verbs):
            remove_list.append(i)
            continue
dd = df.drop(df.index[remove_list])
del df

dd = dd.reset_index(drop=True)

print "Removing verbs"
#dd.to_csv("allverbsremoved.csv", sep=',', index=False)

stopwords = []
remove_list = []
f = open('./other_text_files/stopwords.txt')
for i in f.readlines():
    stopwords.append(i.strip().lower())

for i in range(len(dd)):
    for j in (dd.loc[i][0].split()):
        if(j.lower() in stopwords):
            remove_list.append(i)
            continue
de = dd.drop(dd.index[remove_list])
del dd
de = de.reset_index(drop=True)

print "Removing stopwords"
#de.to_csv("allstopwordsremoved.csv", sep=',', index=False)

digits = ['1','2','3','4','5', '6','7','8','9','0']
special = ['~','!','@','#','$','%','^','&','*','(',')',':']

remove_list = []

for i in range(len(de)):
    for j in (de.loc[i][0].split()):
        if (True in list(k in j.lower() for k in digits)):
            remove_list.append(i)
            continue
        elif (True in list(k in j.lower() for k in special)):
            remove_list.append(i)
            continue
        elif (',' in j):
            remove_list.append(i)
            continue
dg = de.drop(de.index[remove_list])
del de
dg = dg.reset_index(drop=True)
print "Removing digits and special char"
#dg.to_csv("listjunkremoved.csv", sep=',', index=False)

remove_list = []
for i in range(len(dg)):
    if(len(dg.loc[i][0])<3):
        remove_list.append(i)
dh = dg.drop(dg.index[remove_list])
del dg
dh = dh.reset_index(drop=True)

#what is this?
#print "Writing 2 length words removed data to file"
#dh.to_csv("listlengthcropped.csv", sep=',', index=False)
remove_list = []

for i in range(len(dh)):
    for j in (dh.loc[i][0].split()):
        if (j[0] in string.ascii_lowercase):
            if not (i in remove_list):
                remove_list.append(i)
        if j[0]=='\'':
            if not (i in remove_list):
                remove_list.append(i)
            
di = dh.drop(dh.index[remove_list])
del dh
di = di.reset_index(drop=True)

print "Removing lowercase"
di.to_csv("preprocessed_data_"+var+".csv", sep=',', index=False)
