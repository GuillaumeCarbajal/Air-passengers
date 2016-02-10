from sklearn.ensemble import GradientBoostingRegressor
from sklearn.base import BaseEstimator
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import Pipeline

class Regressor(BaseEstimator):
    def __init__(self):
        
        loss='ls'
        learning_rate=0.2
        n_estimators=2000
        #min_weight_fraction_leaf=0.0
        max_depth=4
        min_samples_split= 10
        random_state=10
        max_features=100

        self.clf = GradientBoostingRegressor(loss= loss,
                                        learning_rate= learning_rate,
                                        n_estimators= n_estimators,
                                        subsample=1.0,
                                        #max_depth = max_depth,
                                        min_samples_split= min_samples_split,
                                        max_features = max_features,
                                        random_state=random_state)


        loss='ls'
        learning_rate=0.2
        n_estimators=2000
        min_weight_fraction_leaf=0.0
        max_depth=6
        min_samples_split= 10
        random_state=10
        max_features=100

        self.clf2 = GradientBoostingRegressor(loss= loss,
                                        learning_rate= learning_rate,
                                        n_estimators= n_estimators,
                                        subsample=1.0,
                                        max_depth = max_depth,
                                        #min_samples_split= min_samples_split,
                                        max_features = max_features,
                                        random_state=random_state)

        scaler1=StandardScaler()
        scaler = MinMaxScaler(feature_range=(0.0, 1.0))

        svr = SVR(kernel='rbf', C= 4, cache_size= 800, epsilon = 0.045)
        
        self.pipeline = Pipeline([
            ('scaler', scaler1),
            ('svr', svr)])

    def fit(self, X, y):
        self.clf.fit(X, y)
        self.clf2.fit(X,y)
        self.pipeline.fit(X,y)

    def predict(self, X):
        return (self.clf.predict(X)+self.clf2.predict(X)+self.pipeline(X))/3