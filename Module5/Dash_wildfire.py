import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

# 创建 app
app = dash.Dash(__name__)

# 清除布局并在回调执行前不显示异常
app.config.suppress_callback_exceptions = True

# 读取野火数据到 pandas dataframe
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

# 从 date 列提取年份和月份
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() 
df['Year'] = pd.to_datetime(df['Date']).dt.year

# ----------------- Layout 布局部分 -----------------
app.layout = html.Div(children=[
    # TASK 2.1: 添加仪表板标题
    html.H1('Australia Wildfire Dashboard', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}),
    
    # 外层大容器（包裹标题下方的所有交互组件和图表）
    html.Div([
        # TASK 2.2: 选择地区的单选按钮 (RadioItems)
        html.Div([
            html.H2('Select Region:', style={'margin-right': '2em'}),
            dcc.RadioItems([
                {"label": "New South Wales", "value": "NSW"},
                {"label": "Northern Territory", "value": "NT"},
                {"label": "Queensland", "value": "QL"},
                {"label": "South Australia", "value": "SA"},
                {"label": "Tasmania", "value": "TA"},
                {"label": "Victoria", "value": "VI"},
                {"label": "Western Australia", "value": "WA"}
            ], "NSW", id='region', inline=True)
        ]),
        
        # 选择年份的下拉菜单 (Dropdown)
        html.Div([
            html.H2('Select Year:', style={'margin-right': '2em'}),
            dcc.Dropdown(df.Year.unique(), value=2005, id='year')
        ]),
        
        # TASK 2.3: 添加两个用于放置图表的空 Div 容器
        html.Div([
            html.Div([], id='plot1'),
            html.Div([], id='plot2')
        ], style={'display': 'flex'}), # 设置为横向并排显示
        
    ])
])

# ----------------- Callback 交互部分 -----------------
# TASK 2.4: 绑定 Output 和 Input
@app.callback(
    [Output(component_id='plot1', component_property='children'),
     Output(component_id='plot2', component_property='children')],
    [Input(component_id='region', component_property='value'),
     Input(component_id='year', component_property='value')]
)

# TASK 2.5: 定义回调函数，处理数据并返回图表
def reg_year_display(input_region, input_year): 
    
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]
    
    
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month', 
                  title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region, input_year))  
    
    
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x='Month', y='Count', 
                  title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region, input_year))   
    
    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]

if __name__ == '__main__':
    app.run(debug=True)