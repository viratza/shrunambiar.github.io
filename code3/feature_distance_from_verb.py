import pandas as pd

df = pd.read_csv('lowercase cropped.csv')
df.insert(len(df.columns), "PRE_DIST_VERB", 100)
df.insert(len(df.columns), "POST_DIST_VERB",100)
df.insert(len(df.columns), "PRE_DIST_STOPWORD",100)
df.insert(len(df.columns), "POST_DIST_STOPWORD",100)
df.insert(len(df.columns), "PrecedingTitle", False)
df.insert(len(df.columns), "Apostrophe", False)
df.insert(len(df.columns), "PRE_DIST_FROM_THE", False)
df.insert(len(df.columns), "PRE_DIST_FROM_POSITION", 100)
f = open('./other_text_files/verbs4.txt')
g = open('./other_text_files/stopwords.txt')

def checkPrecedingPrefix(instance):
    l = instance.split(" ")
    # n = len(l)

    prefixes = ['Mr.', 'Mrs.', 'Dr.', 'Ms.', 'Sir.', 'Jr.', 'Sr.', 'Lord', 'Prince', 'Princess']

    # Positions=['Leader','Secretary','Prime Minister','Officer','Archbishop','Major','Chancellor','Minister','MEP', 'Officer','Spokesperson', 'Sheriff', 'Reporter', 'Sergent', 'General','Queen','Lieutenant','Colonel','Commander','Captain','Private','Specialist','Staff','Master','Brigadier','Airman','Seaman','Minister','Admiral','Deputy','MP', 'President', 'Vice president','Governor', 'Chair','Director','Controller','Inspector','Assistant','Priest','Professor','Principal','Lady','Viceroy','Vicar']


    if l[0] in prefixes or (l[0] + ".") in prefixes:
        return True
    return False

def checkSucceedingApostrophe(instance):
    l = instance.split(" ")
    # n = len(l)

    val = l[-1]

    if val[-1] == "\'" or val[-2:] == "\'s":
        return True

    return False

#------------------------------


verbs = f.read().split()
stopwords = g.read().split()

for j in range(len(df)):
    file = open(df.loc[j]['filename'])
    ls = file.read().split()
    start = df.loc[j]['start']
    end = df.loc[j]['end']
    instance = df.loc[j]["All-Words"]

    if start>5:
        prestring = ls[start-5:start]
    else:
        prestring = ls[0:start]
    if end< len(ls)-5:
        postring = ls[end+1:end + 5]
    else:
        postring = ls[end+1:len(ls)-1]

    if start>1:
        preword = ls[start-1:start]
    else:
        preword = ls[0:start]



    for i in postring:
        if i in verbs:
            df.at[j,"POST_DIST_VERB"]=postring.index(i)
            break


    if preword=="the" or preword=="The":
        df.at[j,"PRE_DIST_FROM_THE"]= True
        break

    for k in prestring:
        if k in verbs:
            df.at[j,"PRE_DIST_VERB"]=len(prestring)- prestring.index(k)

    for i in postring:
        if i in stopwords:
            df.at[j, "POST_DIST_STOPWORD"] = postring.index(i)
            break
    for k in prestring:
        if k in stopwords:
            df.at[j,"PRE_DIST_STOPWORD"]=len(prestring)- prestring.index(k)

    for k in prestring:
        Positions=['Leader','Secretary','Prime Minister','Officer','Archbishop','Major','Chancellor','Minister','MEP', 'Officer','Spokesperson', 'Sheriff', 'Reporter', 'Sergent', 'General','Queen','Lieutenant','Colonel','Commander','Captain','Private','Specialist','Staff','Master','Brigadier','Airman','Seaman','Minister','Admiral','Deputy','MP', 'President', 'Vice president','Governor', 'Chair','Director','Controller','Inspector','Assistant','Priest','Professor','Principal','Lady','Viceroy','Vicar']

        if k in Positions:
            df.at[j,"PRE_DIST_FROM_POSITION"]=len(prestring)- prestring.index(k)
            break


    prefix = checkPrecedingPrefix(instance)
    df.at[j, "PrecedingTitle"] = prefix
    apostrophe = checkSucceedingApostrophe(instance)
    df.at[j, "Apostrophe"] = apostrophe

print "Writing feature DIST_VERB to file"

df.to_csv("distance to verb.csv", sep=',', index=False)