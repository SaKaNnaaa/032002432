import viw
import worm_target08 as wt
import worm_database01 as wd
import handle_DataFrame as hd


def get_today(type):                # type表示查询今日数据类型，1表示“本土新增”，2表示“无症状新增”
    database1=hd.creat_D()
    database2=hd.creat_D()
    today_list=wt.main(database1, database2, spc_flag=True)
    # print(today_list[0][0])
    # print(today_list[1][0])
    hd.new_base(today_list[0][0],today_list[1][0])
    viw.main(type)
def get_day7():
    database1 = hd.creat_D()
    database2 = hd.creat_D()
    for day in range(7):
        wt.main(database1,database2,day+1,spc_flag=True,op_sign=day)
    # print(database1)
    # print(database2)
    hd.new_base(database1,database2)
# def dayall_dat():
#     # wd.main(1,50)
#     # print(wd.last_page)
#     op_list=1
#     for i in range(wd.last_page-1):
#         wt.main(1, i,True,op_list)



def main():
    # 更新网页信息
    if wd.date_func():      # 判断有效日期是否变化，若变化更新数据库
        print(' update ')
        wd.main()
    # 获取昨日新增
    print('***获取以下日期数据中***')
    get_day7()
    while(True):
        print('查询更多资讯请输入：')
        print('"1"：查看近7天数据概览  "0"：退出程序')
        select=input()
        if select == '0':
            return
        elif select == '1':         # 7天数据概况
            viw.main()
        elif select == '2':         # 查询某省数据
            pass
        elif select == '3':         # 7天无本土新增统计
            pass
        elif select == '4':         # 今日热点
            pass
        else:
            print('please try input by rules')
if __name__=='__main__':
    main()