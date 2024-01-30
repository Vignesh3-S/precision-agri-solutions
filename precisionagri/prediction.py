import numpy as np
import pandas as pd
import six
import sys
sys.modules['sklearn.externals.six'] = six
import joblib
from itertools import chain
import warnings
from agriproject import settings
def cropprediction(input_list):
    warnings.simplefilter('ignore')
    data = pd.read_csv(settings.BASE_DIR / 'ml/Indian_Crop_Dataset.csv')
    target_list = list(data['label'])
    h = [*set(target_list)]
    h.sort()
    model = joblib.load(open(settings.BASE_DIR / 'ml/predictionmodel.sav','rb'))
    std = joblib.load(open(settings.BASE_DIR / 'ml/standard.sav','rb'))
    a = list(input_list)
    a_array = np.asarray(a)
    a_reshape = a_array.reshape(1,-1)
    a_std = std.transform(a_reshape)
    temp = []
    for i in model:
        temp.append(i.predict(a_std))
        b = list(chain.from_iterable(temp))
    return(h[max(b)])
