# 获取单日新增数据

import json
import urllib.request
import pandas
from lxml import etree
import pandas as pd
from html2text import html2text
import matplotlib.pyplot as plt
import numpy as np

NEW_LOCAL = 0
COVER_INNFD = 1
SPEC_ARE = 2
SPE_NO = 32


def get_src_data(context, type_num):
    # print(context)
    if type_num == SPEC_ARE:
        st1 = '香港'
        ed1 = '）。'
        sta1 = context.find(st1)
        end1 = context.find(ed1, sta1)
        text1 = context[sta1:end1]
        st2 = '区'
        ed2 = '例'
        sta_t = sta1
        res_list = []
        for i in range(3):
            sta2 = context.find(st2, sta_t)
            end2 = context.find(ed2, sta2)
            sta_t = end2
            val_s = int(context[sta2 + 1:end2])
            res_list.append(val_s)

        return res_list

    if type_num == NEW_LOCAL:
        st1 = '本土病例'
        ed1 = '当日新增治愈'
    elif type_num == COVER_INNFD:
        st1 = '新增无症状'
        ed1 = '当日解除'
    # print(context)
    sta1 = context.find(st1)
    end1 = context.find(ed1, sta1)
    text1 = context[sta1:end1]
    # print(text1)
    sta2 = text1.find('（')
    end2 = text1.find('）', sta2)
    text1 = text1[sta2 + 1:end2]
    text1 = text1.replace('*', '')
    src_loc = text1.split('，')
    # print(src_loc)
    return src_loc



def add_Data(db,el1, el2, type_num,op_list):
    db.loc[el1][op_list] = el2


def handl_src(Base_data,src_data, type_num, date,op_list):
    for elemt in src_data:
        sta_pos = 0
        check_vail = 0
        for i in range(len(elemt)):                 # 通过‘；’截取前面多余部分
            if elemt[i] == '；':
                sta_pos = i + 1
                break
        for i in range(len(elemt)):
            if elemt[i] == '例':                     # 查找字符串是否含‘例’，若有则必定在该字符串末尾
                check_vail = 1
        if check_vail == 0:                         # 若字符串中无‘例’，则表明无效数据
            continue
        elemt_t = elemt[sta_pos:]                    # 提出最简字符串，如‘四川36例’

        break_point = 0
        for i in range(len(elemt_t)):               # 查找文字和数字分界点
            if elemt_t[i].isdigit():
                break_point = i
                break
        try:
            el1 = elemt_t[:break_point]                         # 获取省份名字
            el2 = int(elemt_t[break_point:len(elemt_t) - 1])    # 获取人数
            # el2 = int(elemt_t[break_point:elemt_t.find('例')])
            # print(el1)
            # print(el2)
            if type_num == NEW_LOCAL:
                # print('*******************')
                add_Data(Base_data, el1, el2, NEW_LOCAL, op_list)
            else:
                # print('&&&&&&&&&&&&&&&&&&&&&&&&&')
                add_Data(Base_data, el1, el2, COVER_INNFD, op_list)
        except:
            # pass
            print('*****************' + date + 'abnormal****************')


def creat_context(url):
    headers = {
        'Cookie': 'yfx_c_g_u_id_10006654=_ck22091309115919177477821311645; yfx_mr_10006654=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10006654=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10006654=; sVoELocvxVW0S=5.KsK_WRfnfWa0G3WsJX3Cml6tHZIBBdbpbHVAxgJM0RfwhawlD40Adz3RktBxBplRJJqqO9XynjWFkAZMsOQgA; _gscu_2059686908=63031563rnnn1h12; yfx_f_l_v_t_10006654=f_t_1663031519914__r_t_1663031519914__v_t_1663043091627__r_c_0; insert_cookie=91349450; security_session_verify=3bef9658e2f284f004c8eb608f92c468; sVoELocvxVW0T=53nqW1bWGkW7qqqDkJsqlXG_wBd.Hr__uHTMh63NRkUAmm43MANqODJJtCuHs8r1L73fC794JJMDbt58JXu.mQeSJObR2QNQLEI_rpLKW3OvJABvy8V74rqyv9zk1DJZPiIhNmNJXZOFm2Xeyg1.22NHsUZCY5YtU5sLlADi3GyDI9xUSM39nnc1YuWyaFkuqzy0K2i6RbI7SN70GppD5F8bvMtOyS5UtmRnVruSeN484YsNJ9O26LTGEtkErqum4g',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf8')

    tree=etree.HTML(content)
    title = tree.xpath('//title/text()')
    # print(title[0])
    if title[0].startswith('截至'):                               # 判断是否是疫情通报文章
        context = html2text(content)
        return context
    else:
        return ''

def get_src_spc(Base_data1,context, context_s,op_sign):
    # print(context_s)
    context_list = get_src_data(context, SPEC_ARE)
    context_list_s = get_src_data(context_s, SPEC_ARE)
    # print(context_list)
    # print(context_list_s)
    area_list = ['香港', '澳门', '台湾']
    for i in range(3):
        Base_data1.loc[area_list[i]][op_sign] = context_list[i] - context_list_s[i]

def crate_bas(Base_data1,Base_data2,day, list_no=1, spc_flag=False,op_sign=0):
    df = pd.read_excel(r'Database/li' + str(list_no) + '.xlsx')
    date = df.loc[day-1].values[1]
    print(date)
    context = creat_context(df.loc[day-1].values[2])
    if context=='':
        return
    # try:
    src_loc = get_src_data(context, NEW_LOCAL)
    # print(src_loc)
    handl_src(Base_data1, src_loc, NEW_LOCAL, date,op_sign)
    src_cov = get_src_data(context, COVER_INNFD)
    handl_src(Base_data2, src_cov, COVER_INNFD, date,op_sign)
    # 获取港澳台新增所需的前一天数据
    if spc_flag:
        if day < 23:
            context_s = creat_context(df.loc[day].values[2])
        else:
            df = pd.read_excel(r'Database/li' + str(list_no + 1) + '.xlsx')
            context = creat_context(df.loc[0].values[2])
        get_src_spc(Base_data1,context, context_s,op_sign)
    # except:
    #      print('*****************' + date + 'error****************')





def main(Base_data1,Base_data2,day=1, spc_flag=False,op_sign = 0, list_no=1):
    # 获取第list_no列表中，第day条信息，spc_flag表示是否记录港澳台地区数据，op_sign记录数据记录在database中的第几列
    crate_bas(Base_data1,Base_data2,day, list_no, spc_flag,op_sign)
    # print(Base_data1)
    # print(Base_data2)
    return [Base_data1,Base_data2]
    # save_base(Base_data1,Base_data2)



if __name__ == '__main__':
    main(5, 5, 8, True)