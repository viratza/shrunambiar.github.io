import os

# os.system('time python ./data/test/extractor2.py')
os.system('python tagcheck4.py ./data/test/listtest.csv')
os.system('python preprocessing.py')
os.system('python feature_distance_from_verb.py test')