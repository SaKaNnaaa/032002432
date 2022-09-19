import webbrowser
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Map,Page
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from bs4 import BeautifulSoup

# from pyecharts import Grid
import pyecharts.options as opts
from pyecharts.charts import Bar3D


def _map(day, madta_list):
    data = [[[x["name"], x["value"]] for x in d["data"]] for d in madta_list if d["time"] == f'{day}'][0]
    chart_map = (
        Map()
        .add(
            series_name='',
            data_pair=data,
            is_map_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f'前{day}日疫情本土新增情况',
                subtitle='单位/人',
                pos_left='center',
                pos_top='top',
                title_textstyle_opts=opts.TextStyleOpts(
                    color="rgba(123,123,123,0.8)",

                )
            ),
            visualmap_opts=opts.VisualMapOpts(
                dimension=0,
                max_=max([num[1][0] for num in data[:32]]),         # 因为港澳台通常人数较多，所以不做参照指标
                min_=min([num[1][0] for num in data]),
                # max_ =100,
                # min_ = 0,
                range_text=['High', 'Low'],
                pos_left='5%',
                pos_bottom='center'
            )
        )

    )
    return chart_map
def _map1(day, madta_list):
    data = [[[x["name"], x["value"]] for x in d["data"]] for d in madta_list if d["time"] == f'{day}'][0]
    chart_map = (
        Map()
        .add(
            series_name='',
            data_pair=data,
            is_map_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f'前{day}日疫情无症状新增情况',
                subtitle='单位/人',
                pos_left='center',
                pos_top='top',
                title_textstyle_opts=opts.TextStyleOpts(
                    color="rgba(0,0,0,0.8)",

                )
            ),
            visualmap_opts=opts.VisualMapOpts(
                dimension=0,
                max_=max([num[1][0] for num in data[:32]]),         # 因为港澳台通常人数较多，所以不做参照指标
                min_=min([num[1][0] for num in data]),
                # max_ =100,
                # min_ = 0,
                range_text=['High', 'Low'],
                pos_left='5%',
                pos_bottom='center'
            )
        )

    )
    return chart_map


def timel(madta_list):
    timeLine = Timeline(init_opts=opts.InitOpts(
        theme=ThemeType.DARK
    ))
    for day in range(1,8,1):
        chart_map = _map(day, madta_list)
        timeLine.add(
            chart=chart_map,
            time_point=day
        )
    return timeLine
def timel1(madta_list):
    timeLine = Timeline(init_opts=opts.InitOpts())
    for day in range(1,8,1):
        chart_map = _map1(day, madta_list)
        timeLine.add(
            chart=chart_map,
            time_point=day
        )
    return timeLine
def viw_handle(day,df):
    madta_list = []
    for day in range(day):
        mdata = {
            'time': str(day + 1),
            'data': []
        }
        for i in range(35):
            dirin = {
                'name': df.index[i],
                'value': [df.iloc[i][day] * 1.0, df.index[i]]
            }
            mdata['data'].append(dirin)
        madta_list.append(mdata)
    return madta_list


def ba3d(df):
    names = df.index
    names = names.tolist()
    days = ["1", "2", "3", "4", "5", "6", "7"]
    data = []
    for x in range(32):
        for day in range(7):
            data.append([day, x, int(df.iloc[x][day])])
    data = [[d[1], d[0], d[2]] for d in data]
    b=(
        Bar3D(init_opts=opts.InitOpts(width="1600px", height="800px", ))
        .add(
            series_name="",
            data=data,
            xaxis3d_opts=opts.Axis3DOpts(type_="category", data=names, interval=0),
            yaxis3d_opts=opts.Axis3DOpts(type_="category", data=days),
            zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        )
        # .set_global_opts(
        #     title_opts=opts.TitleOpts(title="3D概览（1图为本土新增，2图为无症状新增）"),
        # )
        .set_global_opts(

            visualmap_opts=opts.VisualMapOpts(
                max_=20,
                range_color=[
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ],
            )
        )
        # .render("bar3d_punch_card.html")
    )
    return b
def main(opation=1):                    # opation表示获取数据形式
    if opation == 1:                  # 生成当日本土新增分布图
        df = pd.read_excel('res_databas.xlsx', sheet_name=0, index_col=0)
        df1 = pd.read_excel('res_databas.xlsx', sheet_name=1, index_col=0)
        P = Page(layout=Page.SimplePageLayout)
        mdata_list = viw_handle(7,df)
        mdata_list1 = viw_handle(7,df1)
        t = timel(mdata_list)
        t1 = timel1(mdata_list1)
        b=ba3d(df)
        b1=ba3d(df1)
        P.add(t,t1,b,b1)
        P.render()
        webbrowser.open('render.html')


if __name__ == '__main__':
    main(1)



