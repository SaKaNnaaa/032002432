# 用于爬取国家卫健委全部疫情防控数据

import json
import urllib.request
from lxml import etree
import re
import pandas as pd

url1 = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd'
url2 = '.shtml'
url3 = 'http://www.nhc.gov.cn'
last_page = 41

def crate_tree(url,page):
    headers = {
        'Cookie': 'yfx_c_g_u_id_10006654=_ck22091309115919177477821311645; yfx_mr_10006654=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10006654=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10006654=; sVoELocvxVW0S=5.KsK_WRfnfWa0G3WsJX3Cml6tHZIBBdbpbHVAxgJM0RfwhawlD40Adz3RktBxBplRJJqqO9XynjWFkAZMsOQgA; _gscu_2059686908=63031563rnnn1h12; yfx_f_l_v_t_10006654=f_t_1663031519914__r_t_1663031519914__v_t_1663043091627__r_c_0; insert_cookie=91349450; security_session_verify=3bef9658e2f284f004c8eb608f92c468; sVoELocvxVW0T=53nqW1bWGkW7qqqDkJsqlXG_wBd.Hr__uHTMh63NRkUAmm43MANqODJJtCuHs8r1L73fC794JJMDbt58JXu.mQeSJObR2QNQLEI_rpLKW3OvJABvy8V74rqyv9zk1DJZPiIhNmNJXZOFm2Xeyg1.22NHsUZCY5YtU5sLlADi3GyDI9xUSM39nnc1YuWyaFkuqzy0K2i6RbI7SN70GppD5F8bvMtOyS5UtmRnVruSeN484YsNJ9O26LTGEtkErqum4g',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
    }
    request = urllib.request.Request(url=url, headers=headers)

    response = urllib.request.urlopen(request)
    content = response.read().decode('utf8')
    tree = etree.HTML(content)
    return tree

def get_data(tree,page):
    date_list = tree.xpath('//div/ul/li/span/text()')
    src_list = tree.xpath('//div/div/ul/li/a/@href')
    df = pd.DataFrame({
        '日期': [],
        '链接': []
    })
    for i in range(len(date_list)):
        date = date_list[i]
        url = url3 + src_list[i]
        df.loc[len(df)] = [date, url]
        df.to_excel(r'.\Database\li' + str(page) + '.xlsx')

def main(start_page = 1,end_page = 1):
    for page in range(start_page, end_page + 1):
        if page == 1:
            url = url1 + url2
        else:
            url = url1 + '_' + str(page) + url2
        try:
            tree = crate_tree(url,page)
            get_data(tree, page)
        except:
            global last_page
            last_page = page
            print('No More')
            break


if __name__ == '__main__':
    main()