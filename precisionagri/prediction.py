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
    target = list(data['label'])
    target_list= list(set(target))
    target_list.sort()
    model = joblib.load(open(settings.BASE_DIR / 'ml/predictionmodel.sav','rb'))
    input_data = np.asarray(input_list)
    input_reshape = input_data.reshape(1,-1)
    result = model.predict(input_reshape)
    return(target_list[result[0]])
