import streamlit as st
import pandas as pd
import numpy as np
import shap
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

st.set_page_config(page_title='Insurance Cost Estimator', page_icon=':hospital:',layout="wide")

image = Image.open("insurance_cover.png")
st.image(image, use_column_width=True)

st.title('Medical Insurance Regression')

st.markdown('''
Americans spend significantly more on healthcare compared to other nations and such spending is expected to continue growing. That trend will increase the nation’s growing debt even further. This application will provide Americans with a tool to help them predict medical insurance costs.

The dataset used to train the ML model for this app was inspired by the book *Machine Learning with R* by Brett Lantz. The data contains medical information and costs billed by health insurance companies. It contains 1338 rows of data and the following columns: age, gender, BMI, children, smoker, region and insurance charges.

* **Python libraries:** Streamlit, Pandas, NumPy, Sklearn, Matplotlib, Seaborn, Pillow, Shap
* **Data source:** [Kaggle](https://www.kaggle.com/datasets/mirichoi0218/insurance)
''')

st.write('---')
#############################################################################
# Uploading our Dataset
dataset = pd.read_csv('InsuranceDataset.csv')
#############################################################################
# Creating our sidebar menu and displaying user inputs
st.sidebar.header('Specify Input Parameters')

def user_input_features():
    age = st.sidebar.slider('Age', float(dataset['age'].min()),float(dataset['age'].max()),step=1.00)
    sex = st.sidebar.radio('Sex',dataset.sex.unique())
    bmi = st.sidebar.slider('BMI (Body Mass Index)',dataset['bmi'].min(),dataset['bmi'].max(),float(dataset['bmi'].mean()),step=0.01)
    children = st.sidebar.slider('Children',float(dataset['children'].min()),float(dataset['children'].max()),step=1.00)
    smoker = st.sidebar.radio('Smoker',(dataset.smoker.unique()))
    region = st.sidebar.selectbox('Region',(dataset.region.unique()))
    data = {'age' : age,
            'sex' : sex,
            'bmi' : bmi,
            'children' : children,
            'smoker' : smoker,
            'region' : region}
    features = pd.DataFrame(data,index=[0])
    return features

df = user_input_features()

st.header('Specified Parameters')
st.write(df)
st.write('---')
#####################################################################
# Data preprocessing for model
X = dataset.drop(['charges'],axis=1)
Y = dataset['charges']
# Encoding categorical features using dummy variables
sex = {'female' : 0,'male': 1}
X['sex'] =  X['sex'].map(sex)
df['sex'] = df['sex'].map(sex)

smoker = {'no' : 0, 'yes': 1}
X['smoker'] = X['smoker'].map(smoker)
df['smoker'] = df['smoker'].map(smoker)

region = {'northeast' : 0, 'northwest': 1, 'southeast' : 2, 'southwest' : 3}
X['region'] =  X['region'].map(region)
df['region'] = df['region'].map(region)
# label_encoder = preprocessing.LabelEncoder()
# encoded_X = X.apply(label_encoder.fit_transform)
#
scaler = preprocessing.StandardScaler()
standard_df = scaler.fit_transform(X)
X = pd.DataFrame(standard_df, columns=X.columns)
#
# encoded_df = df.apply(label_encoder.fit_transform)
# standard_params = scaler.fit_transform(encoded_df)
# encoded_df = pd.DataFrame(standard_params,columns=df.columns)
# encoded_df
######################################################################
# Building our model
rfr = RandomForestRegressor(criterion="absolute_error",max_features='log2',n_estimators=150,n_jobs=1,random_state=4)
#
rfr.fit(X,Y)
# encoded_df = df.apply(label_encoder.fit_transform)
cost_prediction = rfr.predict(df)
cost_predict = pd.DataFrame(cost_prediction, columns=['Cost (USD)'])
#
st.write('**Prediction based on your inputs** : ')
st.dataframe(cost_predict)
st.write('---')

st.set_option('deprecation.showPyplotGlobalUse', False)

explainer = shap.TreeExplainer(rfr)
shap_values = explainer.shap_values(X)

st.header('Feature Importance')
plt.title('Feature importance based on SHAP values')
shap.summary_plot(shap_values, X)
st.pyplot()

plt.title('Feature importance based on SHAP values (Bar)')
shap.summary_plot(shap_values, X, plot_type="bar")
st.pyplot()
