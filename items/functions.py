import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as opy
import plotly.express as px
from django.db.models import Max
from pandas import DataFrame
from plotly.subplots import make_subplots
from scipy import stats
from statsmodels.compat import lmap
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose


def autocorr_plot(series):
    n = len(series)
    data = np.asarray(series)
    mean = np.mean(data)
    c0 = np.sum((data - mean) ** 2) / float(n)

    def r(h):
        return ((data[:n - h] - mean) *
                (data[h:] - mean)).sum() / float(n) / c0

    x = np.arange(n) + 1
    y = lmap(r, x)
    z95 = 1.959963984540054
    z99 = 2.5758293035489004
    topline1 = z99 / np.sqrt(n)
    topline2 = z95 / np.sqrt(n)
    bottomline1 = -z95 / np.sqrt(n)
    bottomline2 = -z99 / np.sqrt(n)
    return x, y, topline1, topline2, bottomline1, bottomline2


def sales_plot(data):
    df = DataFrame(data)
    if df.__contains__('fyeid'):
        df['d'] = 1
        df['firstofmonth'] = pd.to_datetime(dict(year=df['fyeid'], month=df['fipid'], day=df['d']))
        df = df.sort_values('firstofmonth')
        layout = go.Layout(title="Sales", xaxis={'title': 'year'}, yaxis={'title': 'total'})
        df2 = df.groupby('fyeid').agg('mean').reset_index()
        slope, intercept, r_value, p_value, std_err = stats.linregress(df2.fyeid, df2.value)
        line = slope * df2.fyeid + intercept
        r = pd.date_range(start=df.firstofmonth.min(), end=df.firstofmonth.max(), freq='MS')
        df.index = pd.DatetimeIndex(data=df.firstofmonth)
        df.value.index = pd.DatetimeIndex(data=df.firstofmonth)
        # df.set_index('firstofmonth').reindex(r).fillna(0.0).reset_index()
        df = df.set_index(df.index).reindex(r).fillna(0.0).reset_index()
        df['firstofmonth'] = df['index']
        y = seasonal_decompose(df.value, freq=12)
        model = ARIMA(df.value, order=(5, 1, 0))
        model_fit = model.fit(disp=0)
        predictions = list()
        predictions.append(model_fit.forecast())
        figure2 = make_subplots(rows=4, cols=1,
                                subplot_titles=("Actual Sales", "12-month trend", "Seasonality", "Residuals"))
        figure2.append_trace(go.Scatter(x=df['firstofmonth'], y=df['value'], line_shape='linear', name='Sales'), row=1,
                             col=1)
        figure2.add_trace(go.Scatter(x=df['firstofmonth'], y=predictions, line_shape='linear', name='Predictions',
                                     marker=go.Marker(color='red')))
        figure2.add_trace(go.Scatter(x=df2.fyeid, y=line, line_shape='linear', name='Fit',
                                     marker=go.Marker(color='rgb(255, 160, 122)')))
        figure2.append_trace(go.Scatter(x=y.trend.index, y=y.trend.values, name='12m trend'), row=2, col=1)
        figure2.append_trace(go.Scatter(x=y.seasonal.index, y=y.seasonal.values, name='Seasonality'), row=3, col=1)
        figure2.append_trace(go.Scatter(x=y.resid.index, y=y.resid.values, name='Residuals'), row=4, col=1)
        acp = autocorr_plot(df.value)
        figure = go.Figure()
        figure.add_bar(x=acp[0], y=acp[1])
        layout = go.Layout(margin=dict(l=20, r=20, t=25, b=20), title="Seasonal analysis")
        figure2['layout'].update(layout)
        layout2 = go.Layout(margin=dict(l=20, r=20, t=25, b=20), title="Autocorrelation", yaxis=dict(range=[-1, 1]))
        figure.update_layout(shapes=[  # Line Horizontal Dashed
            go.layout.Shape(
                type="line",
                x0=0,
                x1=acp[0].max(),
                y0=acp[2],
                y1=acp[2],
                line=dict(
                    color="Grey",
                    width=2,
                    dash="dashdot",
                )
            ),  # Line Horizontal Full
            go.layout.Shape(
                type="line",
                x0=0,
                x1=acp[0].max(),
                y0=acp[3],
                y1=acp[3],
                line=dict(
                    color="Grey",
                    width=2,
                )
            ),  # Line Horizontal Full Negative
            go.layout.Shape(
                type="line",
                x0=0,
                x1=acp[0].max(),
                y0=acp[4],
                y1=acp[4],
                line=dict(
                    color="Grey",
                    width=2,
                )
            ),  # Line Horizontal Dashed Negative
            go.layout.Shape(
                type="line",
                x0=0,
                x1=acp[0].max(),
                y0=acp[5],
                y1=acp[5],
                line=dict(
                    color="Grey",
                    width=2,
                    dash="dashdot",
                )
            )])
        figure.update_layout(layout2)
        div = opy.plot(figure, auto_open=False, output_type='div')
        div2 = opy.plot(figure2, auto_open=False, output_type='div')
    return div, div2


def objforecast_plot(data, pk=1):
    import plotly.tools as tls
    df = DataFrame(data)
    if df.__contains__('fyeid'):
        d1, fc_series, lower_series,upper_series,series2 = arima_run(df)
        figure = go.Figure()
        df['d'] = 1
        df['firstofmonth'] = pd.to_datetime(dict(year=df['fyeid'], month=df['fipid'], day=df['d']))
        df=df.sort_values(by=['firstofmonth'])
        fc_series=fc_series.sort_index()
        figure.add_trace(go.Scatter(x=df['firstofmonth'], y=df['value'],mode='lines', name='Sales'))
        figure.add_trace(go.Scatter(x=fc_series.index, y=fc_series,mode='lines', line_color='red', name='Forecast'))
        figure.add_trace(go.Scatter(x=lower_series.index, y=lower_series, fill=None,mode='lines', line_color='grey', name='5% conf'))  # fill to trace0 y
        figure.add_trace(go.Scatter(x=upper_series.index, y=upper_series, fill='tonexty',mode='lines', line_color='lightgrey', name='95% conf'))  # fill to trace0 y
        figure.add_trace(go.Scatter(x=series2.index, y=series2, line_shape='linear', line_color='green', name='Actual'))
        figure.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        try:
            plotly_fig = tls.mpl_to_plotly(d1.plot_diagnostics())
            div2 = opy.plot(plotly_fig, output_type='div', filename="plotly version of an mpl figure")
            div = opy.plot(figure, auto_open=False, output_type='div')
        except:
            plotly_fig=[]
            div2=[]
            div=[]
    return div,div2, d1.seasonal_order, fc_series


def dist_plot(data, title):
    fig = px.histogram(data['Quantity'],'Quantity',width=600, height=500 )
    fig['layout'].update(margin=dict(l=0, r=0, b=0, t=0))
    div = opy.plot(fig, auto_open=False, output_type='div')
    return div


def gauge_plot(data, title):
    max_value = data.aggregate(Max('value')).get('value__max')
    layout = go.Layout(
        autosize=False,
        width=450,
        height=300,
        font=dict(size=8, color='#7f7f7f'),
        # width=260,
        # height=260,
        margin=go.layout.Margin(
            l=20,
            r=20,
            b=20,
            t=25,
            pad=4
        ))
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=data[0].get('value'),
        delta={'reference': data[1].get('value')},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={'axis': {'range': [None, max_value + 50]},
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_value}}), layout)
    div = opy.plot(fig, auto_open=False, output_type='div')
    return div
    # div2 = opy.plot(figure2, auto_open=False, output_type='div')


def sunburst_plot(data, title, type=1):
    # ids = [y['perid__code'] for y in data if 'perid__code' in y]
    df = pd.DataFrame(data)
    if type == 1:
        labels = list(df['perid__name'])
        ids = labels.copy()
        ids.insert(0, 'domestic')
        ids.insert(0, 'export')
        labels.insert(0, 'domestic')
        labels.insert(0, 'export')
        parents = list(df['domorex'])
        parents.insert(0, "")
        parents.insert(0, "")
        values = list(df['value'])
        addvalues = values.copy()
        addvalues.insert(0, df[df['domorex'] == 'domestic']['value'].sum())
        addvalues.insert(0, df[df['domorex'] == 'export']['value'].sum())
        values.insert(0, 0)  # domestic
        values.insert(0, 0)  # export
        fig = go.Figure(go.Sunburst(ids=ids, labels=labels, values=values, parents=parents, customdata=addvalues,
                                    branchvalues='remainder', hovertemplate=
                                    "<b>%{label}</b><br><br>" +
                                    "Amount: %{customdata:,.0f}<br>" +
                                    "<extra></extra>"))
    elif type == 2:
        labels = list(df['iteid__code'])
        cats = list(df['iteid__category__descr'].unique())
        ids = labels.copy()
        ids.extend(cats)
        labels.extend(cats)
        parents = list(df['iteid__category__descr'])
        values = list(df['value'])
        addvalues = values.copy()
        for i in cats:
            parents.append('')
            addvalues.append(df[df['iteid__category__descr'] == i]['value'].sum())
            values.append(0)
        fig = go.Figure(go.Sunburst(ids=ids, labels=labels, values=values, parents=parents, customdata=addvalues,
                                    branchvalues='remainder', hovertemplate=
                                    "<b>%{label}</b><br><br>" +
                                    "Amount: %{customdata:,.0f}<br>" +
                                    "<extra></extra>"))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    div = opy.plot(fig, auto_open=False, output_type='div')
    return div


def plotly_table(data, type=1):
    if type == 1:
        df = pd.DataFrame(data)
        # df['value']=df['value'].round()
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Year</b>', '<b>Total Sales</b>', '<b>YoY % Change</b>'],
                line_color='gray', fill_color='lightgrey',
                align='center', font=dict(color='black', size=15)
            ),
            cells=dict(
                values=[df.fyeid, df.value, df.yoy],
                line_color='gray',
                fill_color=[df.color],
                align='center', font=dict(color='black', size=14)
            ))
        ])
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div
    elif type == 2:
        # df['value']=df['value'].round()
        data=data.round()
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Month</b>', '<b>Predicted Quantity</b>'],
                line_color='gray', fill_color='lightgrey',
                align='center', font=dict(color='black', size=15)
            ),
            cells=dict(
                values=[data.index, data.values],
                line_color='gray',
                fill_color=['white'],
                align='center', font=dict(color='black', size=14)
            ))
        ])
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div


def arima_run(data, test_run = False, output = True):
    from dateutil.relativedelta import relativedelta
    import pmdarima as pm
    import numpy as np
    import pandas as pd
    import datetime
    from scipy.stats import zscore
    # d1 = pd.DataFrame(Itemtrans.objects.filter(iteid=iteid).values('fyeid', 'fipid').annotate(
    #     value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField())))
    d1=data
    # calculates z-score values
    pd.options.mode.chained_assignment = None
    d1["zscore"] = zscore(d1["value"])
    # creates `is_outlier` column with either True or False values,
    # so that you could filter your dataframe accordingly
    d1["is_outlier"] = d1["zscore"].apply(lambda x: x <= -1.96 or x >= 1.96)
    d1['d'] = 1
    d1['firstofmonth'] = pd.to_datetime(dict(year=d1['fyeid'], month=d1['fipid'], day=d1['d']))
    d1 = d1.sort_values('firstofmonth')
    d1.index = pd.to_datetime(d1.firstofmonth, format="%Y-%m-%d")
    d1=d1[d1['is_outlier']==False]
    #start_date = datetime.datetime(2020,12,31) - relativedelta(months=25)
    start_date=min(d1.index)
    if test_run:
        test_date = datetime.datetime(2020,12,31) - relativedelta(months=13)
    else:
        test_date = datetime.datetime(2020,12,31)
    series = pd.Series(d1.value[(d1.index>start_date) & (d1.index <= test_date)], index=d1.index[(d1.index>start_date) & (d1.index <= test_date)])
    date1 = d1.firstofmonth.min()
    idx = pd.date_range(date1, test_date, freq='MS')
    series = series.reindex(idx)
    series[np.isnan(series)] = 0
    series2 = pd.Series(d1.value[d1.index >test_date], index=d1.index[d1.index > test_date])
    try:
        dd = pm.auto_arima(series, start_p=1, start_q=1,
                           test='adf',
                           max_p=5, max_q=5, m=12,
                           start_P=0, seasonal=True,
                           d=None, D=1, trace=output,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
    except:
        dd = pm.auto_arima(series, start_p=1, start_q=1,
                           test='adf',
                           max_p=5, max_q=5, m=6,
                           start_P=0, seasonal=True,
                           d=None, D=0, trace=output,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
    n_periods = 12
    fc, confint = dd.predict(n_periods=n_periods, return_conf_int=True, alpha=0.05)
    index_of_fc = np.array([max(series.index)+relativedelta(months=i) for i in range(1,n_periods+1)])

    # make series for plotting purpose
    fc_series = pd.Series(fc, index=index_of_fc)
    lower_series = pd.Series(confint[:, 0], index=index_of_fc)
    upper_series = pd.Series(confint[:, 1], index=index_of_fc)
    fc_series[fc_series < 0] = 0
    # figure = go.Figure()
    # figure.add_trace(go.Scatter(x=d1['firstofmonth'],y=d1['value'], line_shape='linear', name='Sales'))

    # # Plot
    # plt.plot(d1.value, label='Sales')
    # plt.plot(fc_series, color='darkgreen', label='Predicted sales')
    # plt.fill_between(lower_series.index,
    #                  lower_series,
    #                  upper_series,
    #                  color='k', alpha=.15)
    # plt.plot(series2, color='red', label='Actual sales')
    return dd, fc_series, lower_series,upper_series,series2



