import glob
import pandas


def words(data):
    lineStream = iter(data)
    for line in lineStream:
        for word in line.split():
            yield word

def get_all_list():
    list=[]
    filename_list=[]
    n_gram=[]
    start=[]
    end=[]

    for filename in glob.iglob('./cleanfiles/*.txt'):
         with open(filename, 'r') as myself:
             index=0
             for word in words(myself):
                 list.append(word)
                 filename_list.append(filename)
                 n_gram.append(1)
                 start.append(index)
                 end.append(index)
                 index+=1
    i=0
    n=len(list)-1

    while(i<n):
        list.append(list[i]+ " " +list[i+1])
        filename_list.append(filename_list[i])
        n_gram.append(2)
        start.append(start[i])
        end.append(start[i]+1)
        i=i+1

    i=0
    while(i<n-1):
        list.append(list[i]+ " " +list[i+1]+" " +list[i+2])
        filename_list.append(filename_list[i])
        n_gram.append(3)
        start.append(start[i])
        end.append(start[i]+2)
        i=i+1
    return list,filename_list,n_gram,start,end


def print_to_csv():
    list=[]
    filename_list=[]
    n_gram=[]
    start=[]
    end=[]
    list,filename_list,n_gram,start,end=get_all_list()
    df = pandas.DataFrame(data={"All-Words": list, "filename": filename_list,"n-gram": n_gram, "start": start, "end":end})
    df.to_csv("list.csv", sep=',',index=False)

if __name__ == '__main__':
    print_to_csv()
