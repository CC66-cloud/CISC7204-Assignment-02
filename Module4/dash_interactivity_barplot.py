# 1. 导入所需库并读取数据集
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# 读取航空公司数据集
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# 创建 Dash 应用
app = dash.Dash(__name__)

# 2. 设置页面布局 (Layout)
app.layout = html.Div(children=[
    # 大标题
    html.H1('Total number of flights to the destination state split by reporting airline', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # 输入年份的文本框区域
    html.Div([
        "Input Year: ", 
        dcc.Input(
            id='input-year', 
            value='2010', 
            type='number', 
            style={'height': '50px', 'font-size': 35}
        ),
    ], style={'font-size': 40}),
    
    html.Br(),
    html.Br(),
    
    # 图表展示区域
    html.Div(dcc.Graph(id='bar-plot')),
])

# 3. 添加 Callback 装饰器，实现输入与输出的交互绑定
@app.callback(
    Output(component_id='bar-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value')
)

# 4. 定义回调函数：根据输入的年份计算柱状图数据并返回图形
def get_graph(entered_year):
    # 根据输入的年份筛选数据
    df = airline_data[airline_data['Year'] == int(entered_year)]
    
    # 按目标州 (DestState) 分组，并对航班数 (Flights) 求和
    bar_data = df.groupby(['DestState'])['Flights'].sum().reset_index()
    
    # 使用 Plotly Express 生成柱状图
    fig = px.bar(
        bar_data, 
        x='DestState', 
        y='Flights', 
        title='Total number of flights to the destination state'
    )
    
    return fig

# 5. 运行应用
if __name__ == '__main__':
    app.run(debug=True)