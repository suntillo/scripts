import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('YNDX_240223_240523.csv')

fig = go.Figure(data=[go.Candlestick(x=df['<DATE>'],
                open=df['<OPEN>'], high=df['<HIGH>'],
                low=df['<LOW>'], close=df['<CLOSE>'])
                     ])

fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()