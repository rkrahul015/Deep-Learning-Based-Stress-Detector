import pickle

def prediction(URL):
    model = pickle.load(open('./svm_stem.sav', 'rb'))
    result = model.predict([URL])
    print(result)
    return result[0]