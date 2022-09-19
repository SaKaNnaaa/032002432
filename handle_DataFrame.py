import pandas as pdimport
import numpy as np
import pandas as pd

def creat_D():
    arr = np.zeros((35, 7))
    index_list = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南','湖北', '湖南',
                  '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏','新疆', '北京',
                  '天津', '上海', '重庆', '兵团', '香港', '澳门', '台湾']
    Base_data = pd.DataFrame(data=arr,
                                index=index_list,
                                )
    Base_data = Base_data.astype(int)
    return Base_data
def new_base(Base_data1,Base_data2):
    wr = pd.ExcelWriter(r'res_databas.xlsx')
    Base_data1.to_excel(wr, sheet_name='本土新增')
    Base_data2.to_excel(wr, sheet_name='新增无症状')
    wr.save()
# def add_base(Base_data1,Base_data2,day):
#     if day == 1:
#         new_base(Base_data1,Base_data2)
#     else:
#         base1=pd.read_excel(r'res_databas.xlsx',sheet_name=0,index_col=0)
#         base2=pd.read_excel(r'res_databas.xlsx',sheet_name=1,index_col=0)
#         base1.iloc[day]=Base_data1.iloc[0]
#         base2.iloc[day]=Base_data1.iloc[0]
#         new_base(base1, base2)

if __name__=='__main__':
    df=creat_D()
    df.iloc[0]=[1,2,3,4,5,6,7]
    print(df.iloc[0])
    pass