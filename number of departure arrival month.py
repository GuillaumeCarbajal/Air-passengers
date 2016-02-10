def current_month_dep(data):
    df = data.copy()
    df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
    df['month'] = df['DateOfDeparture'].dt.month.astype(str)
    df['year'] = df['DateOfDeparture'].dt.year.astype(str)
    df['year_month_dep'] = df[df.columns[[1,6,7]]].apply(lambda x: '-'.join(x),axis=1)
    n_month_year_dep = dict(df['Departure'].groupby(df['year_month_dep']).count())
    df['n_year_month_dep'] = df['year_month_dep'].map(n_month_year_dep)
    del df['year_month_dep']
    return df

def current_month_arr(data):
    df = data.copy()
    df['DateOfDeparture'] = pd.to_datetime(df['DateOfDeparture'])
    df['month'] = df['DateOfDeparture'].dt.month.astype(str)
    df['year'] = df['DateOfDeparture'].dt.year.astype(str)
    df['year_month_arr'] = df[df.columns[[2,6,7]]].apply(lambda x: '-'.join(x),axis=1)
    n_month_year_arr = dict(df['Arrival'].groupby(df['year_month_arr']).count())
    df['n_year_month_arr'] = df['year_month_arr'].map(n_month_year_arr)
    del df['year_month_arr']
    return df  