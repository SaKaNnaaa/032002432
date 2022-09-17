import worm_target05 as wt
import worm_database01 as wd

def today_data():
    wd.main()
    wt.main(spc_flag=True)
def day7_data():
    wd.main()
    wt.main(1,7,spc_flag=True)
def dayall_dat():
    # wd.main(1,50)
    # print(wd.last_page)
    for i in range(wd.last_page-1):
        wt.main(1, 24,i,True)
    # wt.main(1, 24)
def main():
    # 获取昨日新增
    # today_data()

    # 获取一星期新增
    # day7_data()

    # *********Error**********
    # 获取全部历史数据
    # dayall_dat()

if __name__=='__main__':
    main()