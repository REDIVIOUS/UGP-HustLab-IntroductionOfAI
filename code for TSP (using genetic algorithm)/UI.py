# coding=utf-8
from tkinter import *
from GA_TSP import GA_Algo
import time

# 读取的所有的参数
crossrate = 0.0  # 交叉概率
mutationrate = 0.0 # 变异概率
population = 0 # 种群大小
speed = 0 # 展示速度
citynum = 0 # 城市个数
location = [] # 城市坐标

# 显示参数
gennum = 0 # 当前代数
crosstime = 0 # 当前交叉次数
mutationtime = 0 # 当前变异次数
cost = 0 # 当前最优代价

count = 0 # 记录还需要输入多少个城市

run = 0 # 是否运行

# 所有有关的界面的槽函数
# 开始
def p_start():
    # 读取参数
    global crossrate,mutationrate,population
    crossrate = float(inp_crossrate.get())
    mutationrate = float(inp_mutationrate.get())
    population = int(inp_popnum.get())

    # 开始执行
    global GA_run 
    GA_run = GA_Algo(population,citynum,crossrate,mutationrate,location) 
    global run,cost,gennum,crosstime,mutationtime
    run = 1
    while run:
        GA_run.GenNext()  # 产生下一代
        cost = GA_run.cost  # 计算当前最优代价
        lb_cost.config(text="当前最优代价："+str(round(cost,2)))
        gennum = GA_run.GenNum # 当前代数
        lb_gennum.config(text="当前代数："+str(gennum))
        crosstime = GA_run.CrossTime # 当前交叉次数
        lb_crosstime.config(text="当前交叉次数："+str(crosstime))
        mutationtime = GA_run.MutationTime # 当前遗传次数
        lb_mutationtime.config(text="当前变异次数："+str(mutationtime))
        # 更新画布
        drawline(GA_run.BestResult.gen,location)
        pic.update()
        # 控制速度
        SpeedControl()

# 在所有点之间连接线
def drawline(Genlist,location):
    pic.delete("line")
    # 连成回路
    for i in range(-1,len(Genlist)-1):
        location1 = location[Genlist[i]]
        location2 = location[Genlist[i+1]]
        pic.create_line(location1,location2,tag="line")

# 暂停
def p_pause():
    global run
    run = 0

# 继续
def p_continue():
    # 继续执行
    global run,cost,gennum,crosstime,mutationtime
    run = 1
    while run:
        GA_run.GenNext()  # 产生下一代
        cost = GA_run.cost  # 计算当前最优代价
        lb_cost.config(text="当前最优代价："+str(round(cost,2)))
        gennum = GA_run.GenNum # 当前代数
        lb_gennum.config(text="当前代数："+str(gennum))
        crosstime = GA_run.CrossTime # 当前交叉次数
        lb_crosstime.config(text="当前交叉次数："+str(crosstime))
        mutationtime = GA_run.MutationTime # 当前遗传次数
        lb_mutationtime.config(text="当前变异次数："+str(mutationtime))
        # 更新画布
        drawline(GA_run.BestResult.gen,location)
        pic.update()
        # 控制速度
        SpeedControl()
# 重置
def p_resets():
    # 输入参数清零
    global crossrate,mutationrate,population,speed,citynum,location
    crossrate = 0.0  # 交叉概率
    mutationrate = 0.0 # 变异概率
    population = 0 # 种群大小
    speed = 0 # 展示速度
    citynum = 0 # 城市个数
    location = [] # 城市坐标
    # 显示参数清零
    global gennum,crosstime,mutationtime,cost,count
    # 显示参数
    gennum = 0 # 当前代数
    crosstime = 0 # 当前交叉次数
    mutationtime = 0 # 当前变异次数
    cost = 0 # 当前最优代价
    count = 0 # 记录还需要输入多少个城市
    # 显示信息清零
    lb_gennum.config(text="当前代数：0")
    lb_crosstime.config(text="当前交叉次数：0")
    lb_mutationtime.config(text="当前变异次数：0")
    lb_cost.config(text="当前最优代价：0")
    # 清空画布
    pic.delete(ALL)

# 录入城市个数
def p_citynum():
    global citynum, count
    citynum = int(inp_citynum.get())
    count = citynum

# 逐个录入城市坐标
def p_cityloc():
    first = int(inp_cityloc_x.get())
    second = int(inp_cityloc_y.get())
    result = (first,second)
    global location,count
    location.append(result)
    count = count -  1
    if count != 0:
        info = "还剩下"+str(count)+"个城市需要输入"
    else:
        info = "已经输入完成，可以开始算法"
    lb_info = Label(root,text=info,width = 25)
    lb_info.place(x = 600,y = 575)
    # 将点显示在canvas上
    pic.create_oval(first-3,second-3,first+3,second+3,fill="#ff0000",outline ="#000000",tag="point")

# 速度控制
def SpeedControl():
    global speed
    speed = int(scl.get())
    current_speed = 0.3
    if(speed != 0):
        current_speed = 0.3/speed
    time.sleep(current_speed)


# 有关窗口交互
if __name__ == '__main__':
    root = Tk()
    root.geometry('800x600')
    root.title('GA_TSP')

    # 窗口大标题
    main_lb = Label(root,text="基于遗传算法求解TSP问题",font=('华文楷体',24),bd = 4,width = 71,height=2,relief = SUNKEN)
    main_lb.place(x =5,y=0)

    # 开始
    btn_start = Button(root, text='遗传算法开始',command=p_start,width = 10,height  = 1)
    btn_start.place(x=15, y=65)

    # 暂停
    btn_pause = Button(root, text='遗传算法暂停',command=p_pause,width = 10,height  = 1)
    btn_pause.place(x=145, y=65)

    # 继续
    btn_pause = Button(root, text='遗传算法继续',command=p_continue,width = 10,height  = 1)
    btn_pause.place(x=275, y=65)

    # 重置
    btn_reset = Button(root, text='重置',command=p_resets,width = 10,height  = 1)
    btn_reset.place(x=405, y=65)

    # 录入城市个数
    btn_num = Button(root, text='录入城市个数',command=p_citynum,width = 10,height  = 1)
    btn_num.place(x=535, y=65)

    # 录入城市坐标
    btn_location = Button(root, text='录入城市坐标',command=p_cityloc,width = 10,height  = 1)
    btn_location.place(x=665, y=65)




    # 动态显示区域
    pic = Canvas(root,width = 770, height =300 ,relief = SUNKEN,bd =5)
    pic.place(x=5,y=100)

    # 显示参数区域
    lb_gennum = Label(root,text="当前代数：0",height=1, width = 18, relief = SUNKEN,)
    lb_gennum.place(x = 30,y = 425)

    lb_crosstime = Label(root,text="当前交叉次数：0",height=1, width = 18, relief = SUNKEN,)
    lb_crosstime.place(x = 230,y = 425)

    lb_mutationtime = Label(root,text="当前变异次数：0",height=1, width = 18, relief = SUNKEN,)
    lb_mutationtime.place(x = 430,y = 425)

    lb_cost = Label(root,text="当前最优代价：0",height=1, width = 18, relief = SUNKEN,)
    lb_cost.place(x = 630,y = 425)

    # 输入参数区域
    lb_crossrate = Label(root,text="交叉概率：",width = 12)
    lb_crossrate.place(x = 20,y = 480)
    inp_crossrate = Entry(root)
    inp_crossrate.place(x = 120,y = 480,width = 120)

    # 变异概率
    lb_mutationrate = Label(root,text="变异概率：",width = 12)
    lb_mutationrate.place(x = 270,y = 480)
    inp_mutationrate = Entry(root)
    inp_mutationrate.place(x = 370,y = 480,width = 120)

    # 种群初始数量
    lb_popnum = Label(root,text="种群初始数量：",width = 12)
    lb_popnum.place(x = 520,y = 480)
    inp_popnum = Entry(root)
    inp_popnum.place(x = 620,y = 480,width = 120)

    # 速度滑块
    lb_speed = Label(root,text="调整速度：",width = 12)
    lb_speed.place(x = 20,y = 540)
    var=IntVar()
    scl = Scale(root,orient=HORIZONTAL,length=120,from_=0,to=32,tickinterval=8,resolution=1,variable=var,width = 8)
    scl.place(x = 120,y=520)

    # TSP问题自定义接口
    # 城市个数
    lb_citynum = Label(root,text="城市个数：",width = 12)
    lb_citynum.place(x = 270,y = 540)
    inp_citynum = Entry(root)
    inp_citynum.place(x = 370,y = 540,width = 120)

    # 城市坐标
    lb_cityloc = Label(root,text="城市坐标：",width = 12)
    lb_cityloc.place(x = 520,y = 540)
    lb_x =  Label(root,text="x：",width = 3)
    lb_x.place(x = 600,y = 540)
    inp_cityloc_x = Entry(root)
    inp_cityloc_x.place(x = 620,y = 540,width = 50)
    lb_y =  Label(root,text="y：",width = 3)
    lb_y.place(x = 670,y = 540)
    inp_cityloc_y = Entry(root)
    inp_cityloc_y.place(x = 690,y = 540,width = 50)

    root.mainloop()

