import pandas as pd
import os
import networkx as nx

class FeatureExtractor(object):
    def __init__(self):
        pass

    def fit(self, X_df, y_array):
        pass

    def transform(self, X_df):
        X_encoded = X_df
        path = os.path.dirname(__file__)  # use this in submission
        #path = '.'  # use this in notebook
        #data_weather = pd.read_csv(os.path.join(path, "Submission/external_data.csv"))
        city_airport = pd.read_csv(os.path.join(path, "external_data.csv"))
        
        ######################### 
        # preprocessing functions
        ##################"######
        
        def current_month_dep(data):
            df = data.copy()
            df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
            df['month'] = df['DateOfDeparture'].dt.month.astype(str)
            df['year'] = df['DateOfDeparture'].dt.year.astype(str)
            df['year_month_dep'] = df[['Departure','month','year']].apply(lambda x: '-'.join(x),axis=1)
            n_month_year_dep = dict(df['Departure'].groupby(df['year_month_dep']).count())
            df['n_year_month_dep'] = df['year_month_dep'].map(n_month_year_dep)
            del df['year_month_dep']
            return df
        
        df_6 = current_month_dep(X_df)
        
        def current_month_arr(data):
            df = data.copy()
            df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
            df['month'] = df['DateOfDeparture'].dt.month.astype(str)
            df['year'] = df['DateOfDeparture'].dt.year.astype(str)
            df['year_month_arr'] = df[['Arrival','month','year']].apply(lambda x: '-'.join(x),axis=1)
            n_month_year_arr = dict(df['Arrival'].groupby(df['year_month_arr']).count())
            df['n_year_month_arr'] = df['year_month_arr'].map(n_month_year_arr)
            del df['year_month_arr']
            return df
        
        df_7 = current_month_arr(X_df)
        
        def current_month_city_dep(data):
            df = data.copy()
            df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
            df['month'] = df['DateOfDeparture'].dt.month.astype(str)
            df['year'] = df['DateOfDeparture'].dt.year.astype(str)
            df['city_dep'] = city_dep

            df['year_month_dep'] = df[['city_dep','month','year']].apply(lambda x: '-'.join(x),axis=1)
            n_month_year_dep = dict(df['city_dep'].groupby(df['year_month_dep']).count())
            df['n_year_month_city_dep'] = df['year_month_dep'].map(n_month_year_dep)
            del df['year_month_dep']
            return df

        city_dep=[]
        for j in X_df['Departure']:
            for i, item in enumerate(city_airport['IATA Code']):
                if j==item:
                    city_dep.append(city_airport['AccentCity'][i])     
        
        city_arr=[]
        for j in X_df['Arrival']:
            for i, item in enumerate(city_airport['IATA Code']):
                if j==item:
                    city_arr.append(city_airport['AccentCity'][i])
        
        
        df_11 = current_month_city_dep(X_df)
        
        def current_month_city_arr(data):
            df = data.copy()
            df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
            df['month'] = df['DateOfDeparture'].dt.month.astype(str)
            df['year'] = df['DateOfDeparture'].dt.year.astype(str)
            df['city_arr'] = city_arr

            df['year_month_arr'] = df[['city_arr','month','year']].apply(lambda x: '-'.join(x),axis=1)
            n_month_year_dep = dict(df['city_arr'].groupby(df['year_month_arr']).count())
            df['n_year_month_city_arr'] = df['year_month_arr'].map(n_month_year_dep)
            del df['year_month_arr']
            return df
        
        df_12 = current_month_city_arr(X_df)
        
        def centrality_month_airports(data):    
            df = data.copy()
            df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
            df['month'] = df['DateOfDeparture'].dt.week.astype(str)
            df['year'] = df['DateOfDeparture'].dt.year.astype(str)
            df['year_month'] = df[['month','year']].apply(lambda x: '-'.join(x),axis=1)
            df['year_month_dep'] = df[['Departure','month','year']].apply(lambda x: '-'.join(x),axis=1)
            df['year_month_arr'] = df[['Arrival','month','year']].apply(lambda x: '-'.join(x),axis=1)
            year_month = pd.unique(df['year_month'])
            G = nx.Graph()
            centrality = {}

            for i, item in enumerate(year_month):
                sub_df = df[df['year_month'] == item][['Departure','Arrival']]
                list_dep_arr = zip(sub_df['Departure'], sub_df['Arrival'])
                G.add_edges_from(list_dep_arr)
                #G.number_of_nodes()
                #G.number_of_edges()
                centrality_month = nx.degree_centrality(G)
                centrality_month = pd.DataFrame(centrality_month.items())
                centrality_month['year_month'] = [item] * centrality_month.shape[0]
                centrality_month['airport_year_month'] = centrality_month[centrality_month.columns[[0,2]]].apply(lambda x: '-'.join(x),axis=1)
                centrality_month =dict(zip(centrality_month['airport_year_month'], centrality_month[1]))

                z = centrality.copy()
                z.update(centrality_month)
                centrality = z
            df['centrality_month_dep'] = df['year_month_dep'].map(centrality)
            df['centrality_month_arr'] = df['year_month_arr'].map(centrality)
            return df
        
        df_9 = centrality_month_airports(X_df)
        
        def centrality_month_cities(data):    
            df = data.copy()
            df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
            df['month'] = df['DateOfDeparture'].dt.week.astype(str)
            df['year'] = df['DateOfDeparture'].dt.year.astype(str)
            df['year_month'] = df[['month','year']].apply(lambda x: '-'.join(x),axis=1)
            df['city_dep'] = city_dep
            df['city_arr'] = city_arr

            df['year_month_dep'] = df[['city_dep','month','year']].apply(lambda x: '-'.join(x),axis=1)
            df['year_month_arr'] = df[['city_arr','month','year']].apply(lambda x: '-'.join(x),axis=1)
            year_month = pd.unique(df['year_month'])
            G = nx.Graph()
            centrality = {}

            for i, item in enumerate(year_month):
                sub_df = df[df['year_month'] == item][['city_dep','city_arr']]
                list_dep_arr = zip(sub_df['city_dep'], sub_df['city_arr'])
                G.add_edges_from(list_dep_arr)
                #G.number_of_nodes()
                #G.number_of_edges()
                centrality_month = nx.degree_centrality(G)
                centrality_month = pd.DataFrame(centrality_month.items())
                centrality_month['year_month'] = [item] * centrality_month.shape[0]
                centrality_month['city_year_month'] = centrality_month[centrality_month.columns[[0,2]]].apply(lambda x: '-'.join(x),axis=1)
                centrality_month =dict(zip(centrality_month['city_year_month'], centrality_month[1]))

                z = centrality.copy()
                z.update(centrality_month)
                centrality = z
            df['centrality_city_dep'] = df['year_month_dep'].map(centrality)
            df['centrality_city_arr'] = df['year_month_arr'].map(centrality)
            return df
        
        df_10 = centrality_month_cities(X_df)
        
        def btw_centrality_month_airports(data):    
            df = data.copy()
            df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
            df['month'] = df['DateOfDeparture'].dt.week.astype(str)
            df['year'] = df['DateOfDeparture'].dt.year.astype(str)
            df['year_month'] = df[['month','year']].apply(lambda x: '-'.join(x),axis=1)
            df['year_month_dep'] = df[['Departure','month','year']].apply(lambda x: '-'.join(x),axis=1)
            df['year_month_arr'] = df[['Arrival','month','year']].apply(lambda x: '-'.join(x),axis=1)
            year_month = pd.unique(df['year_month'])
            G = nx.Graph()
            btw_centrality = {}

            for i, item in enumerate(year_month):
                sub_df = df[df['year_month'] == item][['Departure','Arrival']]
                list_dep_arr = zip(sub_df['Departure'], sub_df['Arrival'])
                G.add_edges_from(list_dep_arr)
                #G.number_of_nodes()
                #G.number_of_edges()
                centrality_month = nx.betweenness_centrality(G)
                centrality_month = pd.DataFrame(centrality_month.items())
                centrality_month['year_month'] = [item] * centrality_month.shape[0]
                centrality_month['airport_year_month'] = centrality_month[centrality_month.columns[[0,2]]].apply(lambda x: '-'.join(x),axis=1)
                centrality_month =dict(zip(centrality_month['airport_year_month'], centrality_month[1]))

                z = btw_centrality.copy()
                z.update(centrality_month)
                btw_centrality = z
            df['btw_centrality_month_dep'] = df['year_month_dep'].map(btw_centrality)
            df['btw_centrality_month_arr'] = df['year_month_arr'].map(btw_centrality)
            return df
        
        df_13 = btw_centrality_month_airports(X_df)
        
        def load_centrality_month_airports(data):    
            df = data.copy()
            df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
            df['month'] = df['DateOfDeparture'].dt.week.astype(str)
            df['year'] = df['DateOfDeparture'].dt.year.astype(str)
            df['year_month'] = df[['month','year']].apply(lambda x: '-'.join(x),axis=1)
            df['year_month_dep'] = df[['Departure','month','year']].apply(lambda x: '-'.join(x),axis=1)
            df['year_month_arr'] = df[['Arrival','month','year']].apply(lambda x: '-'.join(x),axis=1)
            year_month = pd.unique(df['year_month'])
            G = nx.Graph()
            load_centrality = {}

            for i, item in enumerate(year_month):
                sub_df = df[df['year_month'] == item][['Departure','Arrival']]
                list_dep_arr = zip(sub_df['Departure'], sub_df['Arrival'])
                G.add_edges_from(list_dep_arr)
                #G.number_of_nodes()
                #G.number_of_edges()
                centrality_month = nx.load_centrality(G)
                centrality_month = pd.DataFrame(centrality_month.items())
                centrality_month['year_month'] = [item] * centrality_month.shape[0]
                centrality_month['airport_year_month'] = centrality_month[centrality_month.columns[[0,2]]].apply(lambda x: '-'.join(x),axis=1)
                centrality_month =dict(zip(centrality_month['airport_year_month'], centrality_month[1]))

                z = load_centrality.copy()
                z.update(centrality_month)
                load_centrality = z
            df['load_centrality_month_dep'] = df['year_month_dep'].map(load_centrality)
            df['load_centrality_month_arr'] = df['year_month_arr'].map(load_centrality)
            return df
        
        df_14 = load_centrality_month_airports(X_df)
        
        def set_connectivity(data):    
            df = data.copy()
            df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
            df['month'] = df['DateOfDeparture'].dt.week.astype(str)
            df['year'] = df['DateOfDeparture'].dt.year.astype(str)
            df['arr_dep'] = df[['Departure','Arrival']].apply(lambda x: '-'.join(x),axis=1)

            G = nx.Graph()
            connectivity = {}

            list_dep_arr = zip(df['Departure'], df['Arrival'])
            G.add_edges_from(list_dep_arr)
            #G.number_of_nodes()
            #G.number_of_edges()
            connectivity = nx.all_pairs_node_connectivity(G)
            for j, jtem in enumerate(connectivity):
                if j==0:
                    a=[jtem]*len(connectivity[jtem])
                    d = pd.DataFrame(connectivity[jtem].items())
                    d = pd.concat([pd.DataFrame(a),d], axis=1)
                    c = d.copy()
                a=[jtem]*len(connectivity[jtem])
                d = pd.DataFrame(connectivity[jtem].items())
                d = pd.concat([pd.DataFrame(a),d], axis=1)
                c = c.append(d)
            c['arr_dep'] = c[c.columns[[0]]].apply(lambda x: '-'.join(x),axis=1)
            connectivity_dep_arr = dict(zip(c['arr_dep'],c[1]))

            df['connectivity'] = df['arr_dep'].map(connectivity_dep_arr)
            return df
        
        df_15 = set_connectivity(X_df)
        
        ################################
        # External data
        ################################
        
        distance=[]
        for i, j in zip(X_df['Departure'], X_df['Arrival']):
            k = city_airport[city_airport['IATA Code'] == i].index.tolist()[0]
            distance.append(city_airport[j][k])       
        
        affluence_2011=[]
        for j in X_df['Departure'].unique():
            for i, item in enumerate(city_airport['IATA Code']):
                if j==item:
                    affluence_2011.append((item, int(city_airport['2011'][i].replace(',',''))))
        affluence_2011 = dict(affluence_2011)
        
        affluence_2013=[]
        for j in X_df['Departure'].unique():
            for i, item in enumerate(city_airport['IATA Code']):
                if j==item:
                    affluence_2013.append((item, int(city_airport['2013'][i].replace(',',''))))
        affluence_2013 = dict(affluence_2013)
        
        ##########################
        # Preprocessing.......
        ##########################
        
        X_encoded['Affluence_Dep_2011'] = X_df['Departure'].map(affluence_2011)
        X_encoded['Affluence_Arr_2011'] = X_df['Arrival'].map(affluence_2011)
        X_encoded['Affluence_Score_2011'] = X_encoded['Affluence_Arr_2011'] + X_encoded['Affluence_Dep_2011']

        X_encoded['Affluence_Dep_2013'] = X_df['Departure'].map(affluence_2013)
        X_encoded['Affluence_Arr_2013'] = X_df['Arrival'].map(affluence_2013)
        X_encoded['Affluence_Score_2013'] = X_encoded['Affluence_Arr_2013'] + X_encoded['Affluence_Dep_2013']

        X_encoded = X_encoded.drop('Affluence_Dep_2011', axis=1)
        X_encoded = X_encoded.drop('Affluence_Arr_2011', axis=1)

        X_encoded = X_encoded.drop('Affluence_Dep_2013', axis=1)
        X_encoded = X_encoded.drop('Affluence_Arr_2013', axis=1)

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

        #data_encoded = data_encoded.join(df_6['n_year_month_dep'])
        #data_encoded = data_encoded.join(df_7['n_year_month_arr'])

        #data_encoded['n_year_month_dep_arr_sum'] = data_encoded['n_year_month_dep'] + data_encoded['n_year_month_arr']
        #data_encoded = data_encoded.drop('n_year_month_dep', axis=1)
        #data_encoded = data_encoded.drop('n_year_month_arr', axis=1)

        X_encoded['distance_airport'] = distance
        #data_encoded['city_dep'] = city_dep
        #data_encoded['city_arr'] = city_arr

        #data_encoded = data_encoded.join(pd.get_dummies(data_encoded['city_dep'], prefix='d'))
        #data_encoded = data_encoded.join(pd.get_dummies(data_encoded['city_arr'], prefix='a'))
        #data_encoded = data_encoded.drop('city_dep', axis=1)
        #data_encoded = data_encoded.drop('city_arr', axis=1)


        #data_encoded = pd.concat([data_encoded, df['oil_prices']], axis=1)

        X_encoded = X_encoded.join(df_11['n_year_month_city_dep'])
        X_encoded = X_encoded.join(df_12['n_year_month_city_arr'])

        X_encoded['n_year_month_dep_arr_city_sum'] = X_encoded['n_year_month_city_dep'] + X_encoded['n_year_month_city_arr']
        X_encoded = X_encoded.drop('n_year_month_city_dep', axis=1)
        X_encoded = X_encoded.drop('n_year_month_city_arr', axis=1)
        

        X_encoded = pd.concat([X_encoded, df_9[['centrality_month_dep','centrality_month_arr']]], axis = 1)
        X_encoded['centrality_sum'] = X_encoded['centrality_month_arr'] + X_encoded['centrality_month_dep']
        X_encoded['centrality_product'] = X_encoded['centrality_month_arr']*X_encoded['centrality_month_dep']

        X_encoded = pd.concat([X_encoded, df_10[['centrality_city_dep','centrality_city_arr']]], axis = 1)
        X_encoded['centrality_city_sum'] = X_encoded['centrality_city_arr'] + X_encoded['centrality_city_dep']
        X_encoded['centrality_city_product'] = X_encoded['centrality_city_arr']*X_encoded['centrality_city_dep']

        X_encoded = X_encoded.drop('centrality_city_dep', axis = 1)
        X_encoded = X_encoded.drop('centrality_city_arr', axis = 1)

        #data_encoded['city_pop_dep'] = city_pop_dep
        #data_encoded['city_pop_arr'] = city_pop_arr

        X_encoded = pd.concat([X_encoded, df_13[['btw_centrality_month_dep','btw_centrality_month_arr']]], axis = 1)
        X_encoded['btw_centrality_diff'] = X_encoded['btw_centrality_month_arr'] - X_encoded['btw_centrality_month_dep']


        X_encoded = pd.concat([X_encoded, df_14[['load_centrality_month_arr','load_centrality_month_dep']]], axis = 1)
        X_encoded['load_centrality_sum'] = X_encoded['load_centrality_month_arr'] + X_encoded['load_centrality_month_dep']
        X_encoded['load_centrality_product'] = X_encoded['load_centrality_month_arr']*X_encoded['load_centrality_month_dep']


        X_encoded = pd.concat([X_encoded, df_15['connectivity']], axis = 1)

        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Departure'], prefix='d'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Arrival'], prefix='a'))
        X_encoded = X_encoded.drop('Departure', axis=1)
        X_encoded = X_encoded.drop('Arrival', axis=1)
        
        X_encoded = X_encoded.drop('DateOfDeparture', axis=1)
        #X_encoded = X_encoded.drop(["WeeksToDeparture", "std_wtd", ], axis=1)

        X_array = X_encoded.values
        
        return X_array