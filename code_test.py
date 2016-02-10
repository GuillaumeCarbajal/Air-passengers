import pandas as pd
import os
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import StratifiedKFold

###################################################
## PREPROCESSING

X_encoded = X_df

path = '.'
#path = os.path.dirname(__file__)  # use this in submission
airports = pd.read_csv(os.path.join(path, "external_data.csv"))

affluence_2011=[]
for j in X_encoded['Departure'].unique():
    for i, item in enumerate(airports['IATA Code']):
        if j==item:
            affluence_2011.append((item, int(airports['2011'][i].replace(',',''))))
affluence_2011 = dict(affluence_2011)

affluence_2012=[]
for j in X_encoded['Departure'].unique():
    for i, item in enumerate(airports['IATA Code']):
        if j==item:
            affluence_2012.append((item, int(airports['2012'][i].replace(',',''))))
affluence_2012 = dict(affluence_2012)

affluence_2013=[]
for j in X_encoded['Departure'].unique():
    for i, item in enumerate(airports['IATA Code']):
        if j==item:
            affluence_2013.append((item, int(airports['2013'][i].replace(',',''))))
affluence_2013 = dict(affluence_2013)

X_encoded['Affluence_Dep_2011'] = X_encoded['Departure'].map(affluence_2011)
X_encoded['Affluence_Arr_2011'] = X_encoded['Arrival'].map(affluence_2011)
X_encoded['Affluence_Score_2011'] = X_encoded['Affluence_Arr_2011'] + X_encoded['Affluence_Dep_2011']

X_encoded['Affluence_Dep_2012'] = X_encoded['Departure'].map(affluence_2012)
X_encoded['Affluence_Arr_2012'] = X_encoded['Arrival'].map(affluence_2012)
X_encoded['Affluence_Score_2012'] = X_encoded['Affluence_Arr_2012'] + X_encoded['Affluence_Dep_2012']

X_encoded['Affluence_Dep_2013'] = X_encoded['Departure'].map(affluence_2013)
X_encoded['Affluence_Arr_2013'] = X_encoded['Arrival'].map(affluence_2013)
X_encoded['Affluence_Score_2013'] = X_encoded['Affluence_Arr_2013'] + X_encoded['Affluence_Dep_2013']

X_encoded = X_encoded.drop('Affluence_Dep_2011', axis=1)
X_encoded = X_encoded.drop('Affluence_Arr_2011', axis=1)

X_encoded = X_encoded.drop('Affluence_Dep_2012', axis=1)
X_encoded = X_encoded.drop('Affluence_Arr_2012', axis=1)

X_encoded = X_encoded.drop('Affluence_Dep_2013', axis=1)
X_encoded = X_encoded.drop('Affluence_Arr_2013', axis=1)
      
X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Departure'], prefix='d'))
X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Arrival'], prefix='a'))
X_encoded = X_encoded.drop('Departure', axis=1)
X_encoded = X_encoded.drop('Arrival', axis=1)

X_encoded['DateOfDeparture'] = pd.to_datetime(X_encoded['DateOfDeparture'])
X_encoded['year'] = X_encoded['DateOfDeparture'].dt.year
X_encoded['month'] = X_encoded['DateOfDeparture'].dt.month
X_encoded['day'] = X_encoded['DateOfDeparture'].dt.day
X_encoded['weekday'] = X_encoded['DateOfDeparture'].dt.weekday
X_encoded['week'] = X_encoded['DateOfDeparture'].dt.week
X_encoded['n_days'] = X_encoded['DateOfDeparture'].apply(lambda date: (date - pd.to_datetime("1970-01-01")).days)

X_encoded = X_encoded.join(pd.get_dummies(X_encoded['year'], prefix='y'))
X_encoded = X_encoded.join(pd.get_dummies(X_encoded['month'], prefix='m'))
X_encoded = X_encoded.join(pd.get_dummies(X_encoded['day'], prefix='d'))
X_encoded = X_encoded.join(pd.get_dummies(X_encoded['weekday'], prefix='wd'))
X_encoded = X_encoded.join(pd.get_dummies(X_encoded['week'], prefix='w'))

X_encoded = X_encoded.drop('DateOfDeparture', axis=1)
X_array = X_encoded.values

features = X_encoded.drop(['log_PAX'], axis=1)
X_columns = X_encoded.columns.drop(['log_PAX'])
X = features.values
y = X_encoded['log_PAX'].values

###################################
## TRAINING AND TESTING

loss='ls'
learning_rate=0.4
n_estimators=600
min_samples_split=10
random_state=10
max_features=80

self.clf = GradientBoostingRegressor(loss= loss,
                        learning_rate= learning_rate,
                        n_estimators= n_estimators,
                        min_samples_split= min_samples_split,
                        random_state= random_state)



X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=10)
skf = StratifiedKFold(y_train, n_folds=5, shuffle = True, random_state=41)

reg = LinearRegression()

scores = cross_val_score(reg, X_train, y_train, cv=skf, scoring='mean_squared_error')
print("log RMSE: {:.4f} +/-{:.4f}".format(
    np.mean(np.sqrt(-scores)), np.std(np.sqrt(-scores))))