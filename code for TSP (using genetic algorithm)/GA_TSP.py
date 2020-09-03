# coding=utf-8
import random
import math

# 个体
class individual(object):
    def __init__(self,Igen):
        self.gen = Igen #个体的基因
        self.rate = 0.0 #适应度


# TSP问题
class TSP(object):
    def __init__(self,IndiNum,CityNum,City):
        self.cityNum = CityNum
        self.indiNum = IndiNum
        self.city = City 

    # 计算总代价
    def dis(self, gen):
        dis = 0.0
        for i in range(-1,self.cityNum - 1):
            # 计算两个城市之间的距离
            location1 = self.city[gen[i]]
            location2 = self.city[gen[i+1]]
            dis = dis + math.sqrt((location1[0] - location2[0]) ** 2 + (location1[1] - location2[1]) ** 2)
        return dis

    # 计算适应函数
    def AdaptFunction(self,gen):
        result = 1.0/self.dis(gen)
        return result

# 遗传算法产生下一代
class GA_Algo(object):
    # 类初始化
    def __init__(self,IndiNum,Genlen,CRate,MRate,City):
        # 参数信息
        self.CrossTime = 0 #交叉次数
        self.GenNum = 0 #遗传代数
        self.MutationTime = 0 #变异次数
        self.population = [] #种群信息
        self.indiNum = IndiNum #种群个体数
        self.genlen = Genlen  #基因长度（城市个数）
        self.CrossOverRate = CRate #交叉概率
        self.MutationRate = MRate #变异概率
        self.BestResult = None #当代最优解
        self.cost = 0.0
        self.totalRate  = 0.0 #所有适应度之和
        self.city = City
        self.PopInit() #种群初始化
        
    # 种群初始化
    def PopInit(self):
        # 初始化population数组
        self.population = []
        # 生成顺序排列基因
        gen = []
        for j in range(self.genlen):
            gen.append(j)
        for i in range(self.indiNum):
            # 随机给出基因的排列
            random.shuffle(gen)
            # 加入一个个体
            self.population.append(individual(gen))


    # 交叉过程
    def crossover(self, ParentGen1, ParentGen2):
        # 随机选择一段基因即行交叉
        crossnum1 = random.randint(0, self.genlen - 2)
        crossnum2 = random.randint(crossnum1, self.genlen - 1)

        # 我们选择交叉的片段
        gentemp = ParentGen2[crossnum1:crossnum2]
        i = 0

        # 完成交叉，产生新基因
        NewGen = [] # 声明新基因
        for num in ParentGen1:
            # 遇到了要交叉的片段插入
            if (i == crossnum1):
                NewGen.extend(gentemp)
                i = i + 1
            # 如果不是交叉的基因，顺序排列（保持不交叉的基因的顺序保持一致）
            if num not in gentemp:
                NewGen.append(num)
                i = i + 1

        self.CrossTime = self.CrossTime + 1

        return NewGen


    # 变异过程
    def GenMutation(self,gen):
        # 随机选择两个编译的基因进行交换
        mutgennum1 = random.randint(0, self.genlen - 1)
        mutgennum2 = random.randint(0, self.genlen - 1)

        # 产生新的基因
        mutgen = gen[:]
        mutgen[mutgennum2] = gen[mutgennum1]
        mutgen[mutgennum1] = gen[mutgennum2]

        self.MutationTime = self.MutationTime + 1
        return mutgen

    # 产生下一代的个体
    def NextGenIndi(self):
        # 按照环境适应度加权随机选择两个父代（可以相同）
        rate = random.uniform(0, self.totalRate)
        for pop in self.population:
            rate = rate - pop.rate
            if (rate <= 0):
                Parent1 = pop
                break

        rate = random.uniform(0, self.totalRate)
        for pop in self.population:
            rate = rate - pop.rate
            if (rate <= 0):
                Parent2 = pop
                break

        #选择第一个父代作为基因
        gen = Parent1.gen
        gen_cross = Parent2.gen

        # 按照crossrate的概率交叉
        prob = random.uniform(0,1)
        if(prob <= self.CrossOverRate):
            gen = self.crossover(gen,gen_cross)

        # 按照MutationRate的概率进行变异
        prob = random.uniform(0,1)
        if(prob <= self.MutationRate):
            gen = self.GenMutation(gen)
        
        NewIndi = individual(gen)

        return NewIndi


    # 生成下一代的种群
    def GenNext(self):
        # 这里采取的策略是每一次留下这一代的最优解
        # 首先我们来计算这个最优解
        temp = self.population[0]
        for pop in self.population:
            TSP_run = TSP(self.indiNum,self.genlen,self.city)
            pop.rate = TSP_run.AdaptFunction(pop.gen)
            if temp.rate < pop.rate:
                temp = pop
        self.BestResult = temp
        TSP_run = TSP(self.indiNum,self.genlen,self.city)
        self.cost = TSP_run.dis(self.BestResult.gen)

        # 生成下一代
        NextGen = [self.BestResult] #首先加入上一代的最优解
        for i in range(self.indiNum - 1):
            NextGen.append(self.NextGenIndi()) # 产生下一代个体
        self.GenNum = self.GenNum + 1 #遗传代数加一
        
        self.population = NextGen #换代





        
