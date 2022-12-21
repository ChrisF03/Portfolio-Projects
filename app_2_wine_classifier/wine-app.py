import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

st. set_page_config(layout="wide")
#
image = Image.open('app_2_wine_classifier/Vinho_Verde_Logo.jpg')
st.image(image)

st.title('Wine Quality Classification')

st.markdown("""
Vinho Verde refers to Portuguese wine that originated in the historic Minho province in the far north of the country. The name means "green wine," but translates as "young wine", with wine being released three to six months after the grapes are harvested. They may be red, white, or rosé, and they are usually consumed soon after bottling.

This app allows user to predict Vinho Verde wine quality and type (white or red) based on physicochemical qualities!

A Support Vector Classifier is used to predict the wine type while a K-Neighbors Classifier is used to predict the wine quality. 

* **Python libraries:** Streamlit, Pandas, NumPy, Sklearn, Matplotlib, Seaborn, Pillow
* **Data source:** [UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/wine+quality)
""")
#########################################################
###### Reading Data into Pandas Dataframes #########
red = pd.read_csv('winequality-red.csv')
red.insert(loc = 0,
          column = 'type',
          value = 'Red')

white = pd.read_csv('winequality-white.csv')
white.insert(loc = 0,
          column = 'type',
          value = 'White')

types = [red, white]
wine = pd.concat(types)
wine.reset_index(drop = True, inplace = True)
######## the wine dataset above^ will be used for visualizations ###########
st.write('---')
###########################################################################
# we will copy the wine dataset into the wine2 variable below for our predictive models
wine2 = wine.copy()
##############################################################################
###### encoding quality column
group_names=['Low','Medium','High']
bin = pd.cut(wine2['quality'], 3, labels=group_names)
wine2['quality'] = bin

quality = {"Low" : 0,"Medium": 1,"High" : 2}
wine2["quality"] =  wine2["quality"].map(quality)

###### encoding the type column
type_ = {"Red" : 0, "White": 1}
wine2["type"] =  wine2["type"].map(type_)
############################################################################3
X = wine2.drop(['type','quality'],axis=1)
Y = wine2['quality']
# ^This split will be used for predicting wine quality (low, average, high)
X2 = wine2.drop(['type','quality'],axis=1)
Y2 = wine2['type']
# ^This split will be used for predicting wine type (red, white)
st.sidebar.header('Specify Input Parameters')

def user_input_features():
    fixed_acidity = st.sidebar.slider('Fixed Acidity',X['fixed acidity'].min(),X['fixed acidity'].max(),float(X['fixed acidity'].mean()))
    volatile_acidity = st.sidebar.slider('Volatile Acidity',X['volatile acidity'].min(),X['volatile acidity'].max(),float(X['volatile acidity'].mean()))
    citric_acid = st.sidebar.slider('Citric Acid',X['citric acid'].min(),X['citric acid'].max(),float(X['citric acid'].mean()))
    residual_sugar = st.sidebar.slider('Residual Sugar',X['residual sugar'].min(),X['residual sugar'].max(),float(X['residual sugar'].mean()))
    chlorides = st.sidebar.slider('Chlorides',X['chlorides'].min(),X['chlorides'].max(),float(X['chlorides'].mean()))
    free_sulfur_dioxide = st.sidebar.slider('Free Sulfur Dioxide',X['free sulfur dioxide'].min(),X['free sulfur dioxide'].max(),float(X['free sulfur dioxide'].mean()))
    total_sulfur_dioxide = st.sidebar.slider('Total Sulfur Dioxide',X['total sulfur dioxide'].min(),X['total sulfur dioxide'].max(),float(X['total sulfur dioxide'].mean()))
    density = st.sidebar.slider('Density',X['density'].min(),X['density'].max(),float(X['density'].mean()))
    pH = st.sidebar.slider('pH',X['pH'].min(),X['pH'].max(),float(X['pH'].mean()))
    sulphates = st.sidebar.slider('Sulphates',X['sulphates'].min(),X['sulphates'].max(),float(X['sulphates'].mean()))
    alcohol = st.sidebar.slider('Alcohol',X['alcohol'].min(),X['alcohol'].max(),float(X['alcohol'].mean()))
    data = {'fixed acidity' : fixed_acidity,
            'volatile acidity' : volatile_acidity,
            'citric acid' : citric_acid,
            'residual sugar' : residual_sugar,
            'chlorides' : chlorides,
            'free sulfur dioxide' : free_sulfur_dioxide,
            'total sulfur dioxide' : total_sulfur_dioxide,
            'density' : density,
            'pH' : pH,
            'sulphates' : sulphates,
            'alcohol' : alcohol}
    features = pd.DataFrame(data,index=[0])
    return features

df = user_input_features()

st.header('Specified Parameters')
with st.expander('CLICK HERE FOR PARAMETER DESCRIPTIONS') :
    st.write('''**Fixed acidity:** Fixed acids include tartaric, malic, citric, and succinic acids which are found in grapes (except succinic). Wines with higher acidity feel lighter-bodied because they come across as “spritzy”. Reducing acids significantly might lead to wines tasting flat. If you prefer a wine that is richer and rounder, you enjoy slightly less acidity.


**Volatile acidity:** These acids are to be distilled out from the wine before completing the production process. It is primarily constituted of acetic acid though other acids like lactic, formic and butyric acids might also be present. Excess of volatile acids are undesirable and lead to unpleasant flavour.


**Citric acid:** This is one of the fixed acids which gives a wine its freshness. Usually most of it is consumed during the fermentation process and sometimes it is added separately to give the wine more freshness.


**Residual sugar:** This typically refers to the natural sugar from grapes which remains after the fermentation process stops, or is stopped.


**Chlorides:** Chloride concentration in the wine is influenced by terroir and its highest levels are found in wines coming from countries where irrigation is carried out using salty water or in areas with brackish terrains.


**Free sulfur dioxide:** This is the part of the sulphur dioxide that when added to a wine is said to be free after the remaining part binds. Winemakers will always try to get the highest proportion of free sulphur to bind. They are also known as sulfites and too much of it is undesirable and gives a pungent odour.


**Total sulfur dioxide:** This is the sum total of the bound and the free sulfur dioxide. This is mainly added to kill harmful bacteria and preserve quality and freshness. There are usually legal limits for sulfur levels in wines and excess of it can even kill good yeast and give out undesirable odour.


**Density:** This can be represented as a comparison of the weight of a specific volume of wine to an equivalent volume of water. It is generally used as a measure of the conversion of sugar to alcohol.


**pH:** Also known as the potential of hydrogen, this is a numeric scale to specify the acidity or basicity the wine. Fixed acidity contributes the most towards the pH of wines. You might know, solutions with a pH less than 7 are acidic, while solutions with a pH greater than 7 are basic. With a pH of 7, pure water is neutral. Most wines have a pH between 2.9 and 3.9 and are therefore acidic.


**Sulphates:** These are mineral salts containing sulfur. Sulphates are to wine as gluten is to food. They are a regular part of the winemaking around the world and are considered essential. They are connected to the fermentation process and affects the wine aroma and flavour.


**Alcohol:** It's usually measured in % vol or alcohol by volume (ABV).
    ''')
st.write(df)
st.write('---')
########################### QUALITY PREDICTION ###############################
scaler = preprocessing.MinMaxScaler()
minmax_df = scaler.fit_transform(X)
X = pd.DataFrame(minmax_df, columns=X.columns)

model =  KNeighborsClassifier(algorithm='auto',n_neighbors=42,p=1,weights='distance')
model.fit(X,Y)  #n_neighbors=18

prediction = model.predict(df)
predict = pd.DataFrame(prediction, columns=['Rating'])

keys = {'Low': [0], 'Average': [1], 'High':[2]}
key = pd.DataFrame.from_dict(keys,orient='index',columns=['Rating'])
########################### TYPE PREDICTION ###############################
scaler = preprocessing.MinMaxScaler()
minmax_df = scaler.fit_transform(X2)
X2 = pd.DataFrame(minmax_df, columns=X2.columns)

model2 = SVC(probability=True)
model2.fit(X2,Y2)

quality_prediction = model2.predict(df)
qual_predict = pd.DataFrame(quality_prediction, columns=['Type'])

type_keys = {'Red': [0], 'White': [1]}
type_key = pd.DataFrame.from_dict(type_keys,orient='index',columns=['Type'])
############################################################################
st.header('Predictions')
st.write('Predictions are based on ' + str(wine.shape[0]) + ' wine samples')
c1 , c2 = st.columns(2)
with c1 :
    st.header('Type')
    st.write('**Prediction based on your inputs** : ')
    st.dataframe(qual_predict)

    st.write('**Prediction probability for each value (%)** : ')
    prediction_proba2 = model2.predict_proba(df)
    proba2 = pd.DataFrame(prediction_proba2*100,columns=['Red','White'])
    st.dataframe(proba2)

    st.write('**Corresponding Labels**')
    st.dataframe(type_key)
with c2 :
    st.header('Quality')
    st.write('**Prediction based on your inputs** : ')
    st.dataframe(predict)

    st.write('**Prediction probability for each value (%)** : ')
    prediction_proba = model.predict_proba(df)
    proba = pd.DataFrame(prediction_proba*100,columns=['Low','Average','High'])
    st.dataframe(proba)

    st.write('**Corresponding Labels**')
    st.dataframe(key)
st.write('---')
############################# Dataset EDA #################################.
st.set_option('deprecation.showPyplotGlobalUse', False)
st.header('Dataset Analysis')
c1, c2, c3 = st.columns(3)
with c1 :
    corr = red.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, cmap='coolwarm', annot=False, mask=mask, vmax=1, square=True)
        ax.set_title('Red Wine Correlations')
        st.pyplot()
    f, ax = plt.subplots(figsize=(7, 5))
    ax = sns.countplot(data=wine, x='type')
    ax.bar_label(ax.containers[0])
    st.pyplot()
with c2 :
    corr = white.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, cmap='coolwarm', annot=False, mask=mask, vmax=1, square=True)
        ax.set_title('White Wine Correlations')
        st.pyplot()
    f, ax = plt.subplots(figsize=(7, 5))
    ax = sns.boxplot(data=wine, x="quality", y='type')
    st.pyplot()
with c3 :
    corr = wine.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, cmap='coolwarm', annot=False, mask=mask, vmax=1, square=True)
        ax.set_title('Overall Wine Correlations')
        st.pyplot()
    f, ax = plt.subplots(figsize=(7,5))
    ax = sns.countplot(x = 'type', hue = 'quality', data = wine2)
    mylabels = ['Low','Average','High']
    ax.legend(labels=mylabels)
    for container in ax.containers:
        ax.bar_label(container)
    st.pyplot()
