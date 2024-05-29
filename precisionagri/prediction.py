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
    #print(input_list) [312.0, 1232121.0, 23.0, 123.0, 123.0, 123.0, 312.0]
    warnings.simplefilter('ignore')
    data = pd.read_csv(settings.BASE_DIR / 'ml/Indian_Crop_Dataset.csv')
    target = list(data['label'])
    target_list= list(set(target))
    target_list.sort()
    model = joblib.load(open(settings.BASE_DIR / 'ml/predictionmodel.sav','rb'))
    input_data = np.asarray(input_list)
    #print(input_data) [3.120000e+02 1.232121e+06 2.300000e+01 1.230000e+02 1.230000e+02 1.230000e+02 3.120000e+02]
    input_reshape = input_data.reshape(1,-1)
    #print(input_reshape) [[3.120000e+02 1.232121e+06 2.300000e+01 1.230000e+02 1.230000e+02 1.230000e+02 3.120000e+02]]
    result = model.predict(input_reshape)
    #print(result)
    return(target_list[result[0]])
