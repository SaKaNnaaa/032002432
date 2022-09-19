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
                                columns=[1, 2, 3, 4, 5, 6, 7],
                                )
    Base_data = Base_data.astype(int)
    return Base_data



if __name__=='__main__':
    pass