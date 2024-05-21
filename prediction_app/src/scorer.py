import pandas as pd
import pickle 
import json
import os
from sklearn.calibration import CalibratedClassifierCV # type: ignore
import seaborn as sns
import matplotlib.pyplot as plt 

# Make prediction
def make_pred(df, path_to_file):

    print('Importing pretrained model...')
    # Import model

    model = pickle.load(open('model/model_cat.sav', 'rb'))

    # Define optimal threshold
    threshold = 0.31

    # Make submission dataframe
    submission = pd.DataFrame({
        'client_id':  pd.read_csv(path_to_file)['client_id'],
        'preds': (model.predict_proba(df)[:, 1] > threshold) * 1
    })
    print('Prediction complete!')

    # Return proba for positive class
    return submission

def get_top5():
    model = pickle.load(open('model/model_cat.sav', 'rb'))

    dat = dict(zip(model.calibrated_classifiers_[0].estimator.feature_names_, model.calibrated_classifiers_[0].estimator.feature_importances_))

    sorted_data = sorted(dat.items(), key=lambda item: item[1], reverse=True)

    # Преобразование обратно в словарь (необязательно)
    sorted_dict = dict(sorted_data)

    top_5_items = list(sorted_dict.items())[:5]
    top_5_dict = dict(top_5_items)

    top_5_json = json.dumps(top_5_dict, indent=4, ensure_ascii=False)

    return top_5_json

def save_plot(df, path_to_file):
    model = pickle.load(open('model/model_cat.sav', 'rb'))

    # Define optimal threshold
    threshold = 0.31

    # Make submission dataframe
    submission = pd.DataFrame({
        'client_id':  pd.read_csv(path_to_file)['client_id'],
        'preds': (model.predict_proba(df)[:, 1] > threshold) * 1
    })
    print('Plot saved!')

    sns.histplot(submission['preds'])
    plt.title(f'Class 0 = {submission[submission["preds"]==0].shape[0]}\nClass 1 = {submission[submission["preds"]==1].shape[0]}')
    image_path = os.path.join('output_image', 'image.png')
    plt.savefig(image_path)
    plt.close()