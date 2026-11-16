import pickle
le = pickle.load(open('fertilizer.pkl','rb'))
print('Fertilizer classes (index -> name):')
for i,c in enumerate(le.classes_):
    print(i, c)