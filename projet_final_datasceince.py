# -*- coding: utf-8 -*-
"""Projet Final Datasceince

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p6c1ciaPOuKfdU4TtpIBuH82iKPy8J8W

# Import
"""

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import sklearn
import statistics 
#url_nathan = "/content/sample_data/spambase.data"
data = pd.read_csv("spambase.data")
#data = pd.read_csv("/content/sample_data/spambase.data")
type(data)

"""Nous avons commencé par regarder la forme du dataset et des exemples de données """

print(data.shape)
data.head()

"""Ensuite, nous avons regardé le type de chaque colonne afin de les crosschecker avec la documentation fournie"""

data.info()

"""Ici nous pouvons voir un début d'analyse de chaque colonne dans le but de mieux situer les valeurs possibles """

data.describe()

"""Pour des soucis de compréhension nous avons renommé toute les colonnes vérifiant comme nous avons pu que les colonnes soient dans le même ordre que dans la documentation en regardant le type des capital_run_length_longest, capital_run_length_total et la target étant les seuls integer et capital_run_length_longest < capital_run_length_total"""

data.rename(columns={ '0':'word_freq_make'	,'0.64':'word_freq_address' ,'0.64.1':'word_freq_all' ,'0.1':'word_freq_3d' ,'0.32':'word_freq_our' 	,'0.2':'word_freq_over'	,'0.3':'word_freq_remove' 	,'0.4':'word_freq_internet' ,	'0.5':'word_freq_order', 	'0.6':'word_freq_mail' 	,'0.7':'word_freq_receive' ,	'0.64.2':'word_freq_will' 	,'0.8':'word_freq_people' 	,'0.9':'word_freq_report' 	,'0.10':'word_freq_addresses' ,'0.32.1':'word_freq_free' 	,'0.11':'word_freq_business' ,'1.29':'word_freq_email' 	,'1.93':'word_freq_you' ,'0.12':'word_freq_credit' ,	'0.96':'word_freq_your' ,'0.13':'word_freq_font' 	,'0.14':'word_freq_000'	,'0.15':'word_freq_money' 	,'0.16':'word_freq_hp'	,'0.17':'word_freq_hpl' ,'0.18':'word_freq_george' ,'0.19':'word_freq_650','0.20':'word_freq_lab' 	,'0.21':'word_freq_labs' 	,'0.22':'word_freq_telnet'	,'0.23':'word_freq_857' 	,'0.24':'word_freq_data' ,	'0.25':'word_freq_415' 	,'0.26':'word_freq_85' 	,'0.27':'word_freq_technology'	,'0.28':'word_freq_1999','0.29':'word_freq_parts','0.30' : 'word_freq_pm' ,	'0.31':'word_freq_direct' 	,'0.32.2':'word_freq_cs' , 	'0.33':'word_freq_meeting' 	,'0.34':'word_freq_original' , 	'0.35' : 'word_freq_project',	'0.36' : 'word_freq_re','1': 'Target', '3.756' : 'capital_run_length_average', '61':'capital_run_length_longest' , '278': 'capital_run_length_total', '0.44': 'char_freq_#' , '0.43':'char_freq_$', '0.778' : 'char_freq_!' , '0.42' : 'char_freq_[', '0.41':'char_freq_(', '0.40' : 'char_freq_;', '0.39': 'word_freq_conference', '0.38' :'word_freq_table', '0.37': 'word_freq_edu'  }, inplace=True)
data.describe()

"""Verifions qu'il n'y a pas de valeur nulle ou non disponible ce qui serait succeptible de fausser les modèles et les différentes visualisations"""

data.isnull().sum()

data.isna().sum()

"""Il y a 2788 mails qui ne sont pas des spams et 1812 qui le sont dans le dataset

Nous voyons aussi qu'il y a une vraie difference au niveau des moyennes de toutes les colonnes contrairement aux quartiles qui nous donne aucune information étant donné que la majeur partie des valeurs est 0 en tout cas pour la majorité des colonnes.
"""

data[data['Target']== 1].describe()

data[data['Target']== 0].describe()

"""En comparant les moyennes nous pouvons facilement remarquer que certaine colonnes fluctuent extremement selon si c'est un spam ou non. 

Notamment la fréquence des mots 3d, remove, 000 qui sont respectivement 185,29 et 34 fois plus fréquent dans des mails de spams.

Ainsi que la fréquence des caractères '$', '!', '#' qui sont respectivement environt 15, 5 et 4 fois plus fréquent dans des mails de spams 

"""

for column in data.columns :
  if(column != 'Target'):
    print(column + ' : ' + str(data[data['Target']== 1][column].mean() / data[data['Target']== 0][column].mean()))

"""De la meme manière nous remarquons que les fréquences des mots 'cs', 'george', 'lab', '857', 'meeting' sont respectivement 1305, 815, 237, 149, 88 fois plus élevées en moyenne.



"""

#word_freq_cs : 1305.1209469153519
#word_freq_george : 815.8935754147157
#word_freq_lab : 237.889468690702
#word_freq_857 : 149.0202539760066
#word_freq_meeting : 88.68073102720136
for column in data.columns :
  if(column != 'Target'):
    print(column + ' : ' + str(data[data['Target']== 0][column].mean() / data[data['Target']== 1][column].mean()))

"""# Data Visualisation"""

spam = len(data[ data['Target'] == 0 ])

non_spam = len(data[data['Target'] == 1])

print('Nombre de spams: ', spam)
print('Nombre de non spams: ', non_spam)

prop = [spam, non_spam]
plt.title('Proportion de spams et non spams dans le dataset')
#sn.barplot(prop, [spam/(spam+non_spam), non_spam/(spam+non_spam)])
plt.pie(prop, labels = ['spam: 60%', 'non spam: 40%'])

"""Dans un premier temps nous avons voulu afficher les différentes corrélations qui existent entre les attributs de notre data frame. Ainsi nous avons tracé une matrice de corrélation sur l’ensemble des 58 attributs que composent notre data frame cependant le grand nombre d’attributs rends le lecture, la compréhension et l’interprétation compliquée. En revanche tracer cette grande matrice de corrélation nous a permis  de voir grossièrement quels étaient les attributs les plus corrélés."""

from matplotlib.pyplot import figure
plt.figure(figsize=(50, 50)) 

corrMatrix = data.corr()
sn.heatmap(corrMatrix, annot=True)

"""Dans un second temps, fort de notre traçage de la grande matrice de corrélation nous avons tracé une deuxième matrice qui cette fois ci contient seulement 16 attributs. Nous observons ainsi des corrélations fortes entre les différents attributs."""

#hp à direct
data_corr = data.iloc[:,24:40]
#data_corr.drop(data_corr.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56]], axis=1) 
data_corr
plt.figure(figsize=(15, 15)) 

corrMatrix_2 = data_corr.corr()
sn.heatmap(corrMatrix_2, annot=True)

"""Afin de connaître mieux la constitution type d’un mail spam et non spam, nous avons affiché les fréquence moyenne d’apparition des mots contenus respectivement dans un mail spam et non spam."""

data_D_0 = data[data['Target']== 0].describe()
data_D_0 = data_D_0.T
data_D_0.drop('capital_run_length_total', inplace = True)
data_D_0.drop('capital_run_length_longest', inplace = True)
data_D_0.drop('capital_run_length_average', inplace = True)

plt.figure(figsize=(20, 5)) 
plt.title('Moyenne de frequence des mots dans les emails non spam')
sn.barplot(data_D_0.index, data_D_0['mean'])
plt.xticks(rotation= 90)

"""Nous observons que les mots qui apparaissent le plus dans un mail non spam sont « you », « george », « hp », « will »"""

data_D_1 = data[data['Target']== 1].describe()
data_D_1 = data_D_1.T
data_D_1.drop('capital_run_length_total', inplace = True)
data_D_1.drop('capital_run_length_longest', inplace = True)
data_D_1.drop('capital_run_length_average', inplace = True)

plt.figure(figsize=(20, 5)) 
plt.title('Moyenne de frequence des mots dans les emails spams')
sn.barplot(data_D_0.index, data_D_1['mean'])
plt.xticks(rotation= 90)

"""Nous observons que les mots qui apparaissent le plus dans un mail spam sont « you », « your », « will », « our »

Nous voyons ici de manière logique que les mots qui apparaissent en moyenne le plus sont des mots courants ou des mots propres à l’utilisateur comme sont prénom.

Nous avons donc choisi d'afficher les mots qui apparaissaient le plus en moyenne dans les spams moins ceux dans les non spams. Cela nous permet d'afficher les mots en moyennes qui apparaissent exlusivement dans les spams
"""

plt.figure(figsize=(20, 5)) 

sn.barplot(data_D_0.index, data_D_1['mean']-data_D_0['mean'])

plt.xticks(rotation= 90)

"""Ainsi nous observons que les hors mis les mots "you" et "your" le mots "free" et le caractère "!" apparaissent particulièrement dans les mails spams"""

plt.figure(figsize=(20, 5)) 

sn.barplot(data_D_0.index, data_D_0['mean']-data_D_1['mean'])

plt.xticks(rotation= 90)

"""On observe ici que les mots "hp", "hpl" "george et "re" apparaissent en moyenne speicifiquement dans les mails non spams

Nous avons effectué dans un deuxième temps une visualisation pour voir quels était les mots propres aux mails spams et non spams.
Ainsi nous observons que les mots « cs », « george », « lab », « 857 », « meeting » apparaissent respectivement 1305, 815, 237, 149, 88 fois plus dans non spam par rapport au spams
"""

#word_freq_cs : 1305.1209469153519
#word_freq_george : 815.8935754147157
#word_freq_lab : 237.889468690702
#word_freq_857 : 149.0202539760066
#word_freq_meeting : 88.68073102720136
list_1 = []
list_2= []
for column in data.columns :
  if(column != 'Target'):
    list_1.append(data[data['Target']== 0][column].mean() / data[data['Target']== 1][column].mean())
    list_2.append(column)
    #print(column + ' : ' + str(data[data['Target']== 0][column].mean() / data[data['Target']== 1][column].mean()))

plt.figure(figsize=(20, 5)) 
plt.title('Ratio apparition de mot dans les non spams par rapport au spams')
sn.barplot(list_2, list_1)
plt.xticks(rotation= 90)

"""Nous observons par ailleurs que les mots 3d, remove, 000 qui sont respectivement 185,29 et 34 fois plus fréquent dans des mails de spam."""

#word_freq_cs : 1305.1209469153519
#word_freq_george : 815.8935754147157
#word_freq_lab : 237.889468690702
#word_freq_857 : 149.0202539760066
#word_freq_meeting : 88.68073102720136
list_1 = []
list_2= []
for column in data.columns :
  if(column != 'Target'):
    list_1.append(data[data['Target']== 1][column].mean() / data[data['Target']== 0][column].mean())
    list_2.append(column)
    #print(column + ' : ' + str(data[data['Target']== 0][column].mean() / data[data['Target']== 1][column].mean()))

plt.figure(figsize=(20, 5)) 
plt.title('Ratio apparition de mot dans les spams par rapport aux non spams')
sn.barplot(list_2, list_1)
plt.xticks(rotation= 90)

"""# Modèles"""

from sklearn.model_selection import train_test_split
train, test = train_test_split(data, test_size=0.2, random_state = 700192)
np_data = train[['word_freq_make' ,	'word_freq_address', 	'word_freq_all', 	'word_freq_3d', 	'word_freq_our', 	'word_freq_over', 	'word_freq_remove', 	'word_freq_internet', 	'word_freq_order', 	'word_freq_mail', 	'word_freq_receive', 	'word_freq_will', 	'word_freq_people', 	'word_freq_report', 	'word_freq_addresses', 	'word_freq_free', 	'word_freq_business', 	'word_freq_email', 	'word_freq_you' ,	'word_freq_credit', 	'word_freq_your', 	'word_freq_font', 	'word_freq_000', 	'word_freq_money', 	'word_freq_hp', 	'word_freq_hpl', 	'word_freq_george', 	'word_freq_650', 	'word_freq_lab' , 	'word_freq_labs', 	'word_freq_telnet' ,	'word_freq_857' ,	'word_freq_data', 	'word_freq_415' ,	'word_freq_85', 	'word_freq_technology', 	'word_freq_1999', 	'word_freq_parts', 	'word_freq_pm', 	'word_freq_direct', 	'word_freq_cs', 	'word_freq_meeting' ,	'word_freq_original', 	'word_freq_project', 	'word_freq_re',	'word_freq_edu' ,	'word_freq_table' ,	'word_freq_conference', 	'char_freq_;', 	'char_freq_(' ,	'char_freq_[' ,	'char_freq_!' ,	'char_freq_$' ,	'char_freq_#' ,	'capital_run_length_average', 	'capital_run_length_longest', 	'capital_run_length_total']].to_numpy()

np_target = train['Target'].tolist()


np_test_data = test[['word_freq_make' ,	'word_freq_address', 	'word_freq_all', 	'word_freq_3d', 	'word_freq_our', 	'word_freq_over', 	'word_freq_remove', 	'word_freq_internet', 	'word_freq_order', 	'word_freq_mail', 	'word_freq_receive', 	'word_freq_will', 	'word_freq_people', 	'word_freq_report', 	'word_freq_addresses', 	'word_freq_free', 	'word_freq_business', 	'word_freq_email', 	'word_freq_you' ,	'word_freq_credit', 	'word_freq_your', 	'word_freq_font', 	'word_freq_000', 	'word_freq_money', 	'word_freq_hp', 	'word_freq_hpl', 	'word_freq_george', 	'word_freq_650', 	'word_freq_lab' , 	'word_freq_labs', 	'word_freq_telnet' ,	'word_freq_857' ,	'word_freq_data', 	'word_freq_415' ,	'word_freq_85', 	'word_freq_technology', 	'word_freq_1999', 	'word_freq_parts', 	'word_freq_pm', 	'word_freq_direct', 	'word_freq_cs', 	'word_freq_meeting' ,	'word_freq_original', 	'word_freq_project', 	'word_freq_re',	'word_freq_edu' ,	'word_freq_table' ,	'word_freq_conference', 	'char_freq_;', 	'char_freq_(' ,	'char_freq_[' ,	'char_freq_!' ,	'char_freq_$' ,	'char_freq_#' ,	'capital_run_length_average', 	'capital_run_length_longest', 	'capital_run_length_total']].to_numpy()


np_test_target = test['Target'].tolist()

"""##KNeighborsClassifier
Nous avons premièrement testé un modele de classification des voisins les plus proches sur l'ensemble de nos attributs ce qui nous a rendu un model avec une précision de 80%
"""

from sklearn import neighbors
knn = neighbors.KNeighborsClassifier()
knn.fit(np_data, np_target)
# Predict and print the result


#result=knn.predict([data.iloc[94].tolist()[:-1]])

c = 0
for i in range(0, len(np_test_data)):
  if(knn.predict([np_test_data[i]]) == np_test_target[i]):
    c += 1

print(c/len(np_test_data) *100)

"""## Clustering
Notre second model de classification à été un système de clustering basé sur un algorithme nommé k-means. 
Il consiste à diviser les éléments en un nombre de groupe fixé (en l'occurence deux spams ou non-spams).
Il n'a qu'une précision de 65%
"""

from sklearn import cluster
k=2
k_means = cluster.KMeans(k)
k_means.fit(np_data)

c = 0
for i in range(0, len(np_test_data)):
  if(k_means.predict([np_test_data[i]]) == np_test_target[i]):
    c += 1

print(c/len(np_test_data) *100)

"""# Regression Linéaire
Finalement, nous avons opté pour une regression linéaire qui sans amélioration nous obtenait une précision de 93%. 
Une precision aussi élevée sans 'feature engineering' s'explique par le fait que les données que nous utilisons ont déja été choisi par précaution.
En effet, la donnée brut, à savoir les mails n'était pas à disposition dans ce cas donc les données que nous avons ont déja subit du feature engineering.

"""

from sklearn import svm

clf_base = svm.LinearSVC(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, loss='squared_hinge', max_iter=10000,
          multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
          verbose=0)



clf_base.fit(np_data, np_target)

c = 0
for i in range(0, len(np_test_data)):
  if(clf_base.predict([np_test_data[i]]) == np_test_target[i]):
    c += 1

print(c/len(np_test_data))

"""# Amélioration des modèles

# Normalisation des données
Notre seconde tentative d'amélioration des performances de nos modeles aura été de normaliser les données.
"""

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(np_data)
scaled_data = scaler.transform(np_data)
scaled_test_data = scaler.transform(np_test_data)

print(scaled_data)

"""## Regression Lineaire
Une fois les données normalisées le modele de régression linéaire ne change presque pas de précision 
"""

clf.fit(scaled_data, np_target)

c = 0
for i in range(0, len(scaled_test_data)):
  if(clf.predict([scaled_test_data[i]]) == np_test_target[i]):
    c += 1

print(c/len(np_test_data) )

"""##Clustering
Le clustering descend jusqu'à 38%.

C'est clairement pas le bon model pour ce dataset. Le clustering est plus utiles lors de classification avec une target ayant plus de valeur possible.
"""

from sklearn import cluster
k=2
k_means = cluster.KMeans(k)
k_means.fit(scaled_data)

c = 0
for i in range(0, len(scaled_test_data)):
  if(k_means.predict([scaled_test_data[i]]) == np_test_target[i]):
    c += 1

print(c/len(np_test_data))

"""##KNeighborsClassifier 
Le modele KNeighbors lui est encore une fois plus performant apres la normalisation des données. La normalisation des données nous à donné une précision de 91%.


"""

from sklearn import neighbors
knn = neighbors.KNeighborsClassifier()
knn.fit(scaled_data, np_target)
# Predict and print the result
c = 0
for i in range(0, len(scaled_test_data)):
  if(knn.predict([scaled_test_data[i]]) == np_test_target[i]):
    c += 1

print(c/len(np_test_data) )

"""#Subset de features 

Dans l'optique d'améliorer la précision de nos modeles nous avons fait appel à la méthode classique des moindres carrés (modèle de régression) pour déterminer dans quelle mesure chaque colonne impactait les chances d'un mail d'être du spams ou non en ce concentrant sur ce qu'on appelle les p-value.
"""

from sklearn import datasets, linear_model
from sklearn.linear_model import LinearRegression
from scipy import stats

X = data[['word_freq_make' ,	'word_freq_address', 	'word_freq_all', 	'word_freq_3d', 	'word_freq_our', 	'word_freq_over', 	'word_freq_remove', 	'word_freq_internet', 	'word_freq_order', 	'word_freq_mail', 	'word_freq_receive', 	'word_freq_will', 	'word_freq_people', 	'word_freq_report', 	'word_freq_addresses', 	'word_freq_free', 	'word_freq_business', 	'word_freq_email', 	'word_freq_you' ,	'word_freq_credit', 	'word_freq_your', 	'word_freq_font', 	'word_freq_000', 	'word_freq_money', 	'word_freq_hp', 	'word_freq_hpl', 	'word_freq_george', 	'word_freq_650', 	'word_freq_lab' , 	'word_freq_labs', 	'word_freq_telnet' ,	'word_freq_857' ,	'word_freq_data', 	'word_freq_415' ,	'word_freq_85', 	'word_freq_technology', 	'word_freq_1999', 	'word_freq_parts', 	'word_freq_pm', 	'word_freq_direct', 	'word_freq_cs', 	'word_freq_meeting' ,	'word_freq_original', 	'word_freq_project', 	'word_freq_re',	'word_freq_edu' ,	'word_freq_table' ,	'word_freq_conference', 	'char_freq_;', 	'char_freq_(' ,	'char_freq_[' ,	'char_freq_!' ,	'char_freq_$' ,	'char_freq_#' ,	'capital_run_length_average', 	'capital_run_length_longest', 	'capital_run_length_total']].to_numpy()

y = data['Target'].tolist()

X2 = sm.add_constant(X)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())

"""Nous avons relevé les colonnes avec les p-value les plus elevés afin de les retirer du dataset."""

data
count = 1
liste = []
for i in data:
  if(count not in [ 10, 11, 13, 14, 15, 28, 29, 31, 32, 34, 35 , 36 , 37, 38, 39, 40,41, 50, 51, 54, 55, 56 , 58]):
    liste.append(i)
  
  count +=1

print(liste)

np_data = train[liste].to_numpy()
np_test_data = test[liste].to_numpy()

"""
##KNeighborsClassifier 
Nous avons remarqué qu'en excluant les colonnes qui selon notre étude de corrélation précédente n'avais que très peu d'impact sur nos prédictions, la classification KNN s'est améliorée en passant à environ 81% de précision au lieu de 78%.
"""

from sklearn import neighbors
knn = neighbors.KNeighborsClassifier()
knn.fit(np_data, np_target)
# Predict and print the result
c = 0
for i in range(0, len(np_test_data)):
  if(knn.predict([np_test_data[i]]) == np_test_target[i]):
    c += 1

print(c/len(np_test_data) * 100)

"""# Clustering
A priori enlever les colonnes en questions n'a pas vraiment aidé ce modèle qui est passé à 66.09% soit une legere progression mais qui reste négligeable. 
"""

from sklearn import cluster
k=2
k_means = cluster.KMeans(k)
k_means.fit(np_data)

c = 0
for i in range(0, len(np_test_data)):
  if(k_means.predict([np_test_data[i]]) == np_test_target[i]):
    c += 1

print(c/len(np_test_data) * 100)

"""#Linear Regression

En revanche la regression linéaire semble arrivé à une précision de 92.93%, ce qui est théoriquement impossible. Cela doit être dû au fait que le dataset à été consu sur-mesure en analysant la présence de mot stratégique étant donné qu'on n'analyse que les mails d'une seule personne.
"""

from sklearn import svm

clf = svm.LinearSVC(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, loss='squared_hinge', max_iter=10000,
          multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
          verbose=0)

clf.fit(np_data, np_target)

c = 0
for i in range(0, len(np_test_data)):
  if(clf.predict([np_test_data[i]]) == np_test_target[i]):
    c += 1

print(c/len(np_test_data)* 100)

"""Etant donné que la regression linéaire sans modification du dataset est le modele le plus precis nous l'avons exporter grâce au module pickle pour l'intégré dans notre api."""

import pickle
pickle.dump(clf_base, open('final_prediction.pickle', 'wb'))