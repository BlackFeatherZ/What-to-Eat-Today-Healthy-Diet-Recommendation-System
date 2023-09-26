#!/usr/bin/python3
# -*- coding: utf-8 -*-
from numpy import *
import time
from texttable import Texttable


class CF:
    def __init__(self, foods, frequency, k=7, n=20):
        self.foods = foods
        self.frequency = frequency
        # The number of close eating food users
        self.k = k
        # The number of searching items
        self.n = n
        # Frequency of number eating one kind of food
        self.userDict = {}
        self.ItemUser = {}
        # Information
        self.neighbors = []
        # Recommendation list
        self.recommandList = []
        self.cost = 0.0

    # Based on users
    # Calculate the similarity between users according to the film rating
    def recommendByUser(self, userId):
        self.formatRate()
        self.n = len(self.userDict[userId])
        self.getNearestNeighbor(userId)
        self.getrecommandList(userId)
        self.getPrecision(userId)

    # Get recommended list
    def getrecommandList(self, userId):
        self.recommandList = []
        # Establish recommendation dictionary
        recommandDict = {}
        for neighbor in self.neighbors:
            foods = self.userDict[neighbor[1]]
            for f in foods:
                if (f[0] in recommandDict):
                    recommandDict[f[0]] += neighbor[0]
                else:
                    recommandDict[f[0]] = neighbor[0]

        # 建立推荐列表
        for key in recommandDict:
            self.recommandList.append([recommandDict[key], key])
        self.recommandList.sort(reverse=True)
        self.recommandList = self.recommandList[:self.k]

    # 将ratings转换为userDict和ItemUser
    def formatRate(self):
        self.userDict = {}
        self.ItemUser = {}
        for i in self.frequency:
            # 评分最高为7 除以7 进行数据归一化
            temp = (i[1], float(i[2]) / 7)
            #print("测试:"+i[1])
            # 计算userDict {'1':[(1,5),(2,5)...],'2':[...]...}
            if (i[0] in self.userDict):
                self.userDict[i[0]].append(temp)
            else:
                self.userDict[i[0]] = [temp]
            # 计算ItemUser {'1',[1,2,3..],...}
            if (i[1] in self.ItemUser):
                self.ItemUser[i[1]].append(i[0])
            else:
                self.ItemUser[i[1]] = [i[0]]

    # 找到某用户的相邻用户
    def getNearestNeighbor(self, userId):
        neighbors = []
        self.neighbors = []
        # 获取userId评分的电影都有那些用户也评过分
        for i in self.userDict[userId]:
            for j in self.ItemUser[i[0]]:
                if (j != userId and j not in neighbors):
                    neighbors.append(j)
        # 计算这些用户与userId的相似度并排序
        for i in neighbors:
            dist = self.getCost(userId, i)
            self.neighbors.append([dist, i])
        # 排序默认是升序，reverse=True表示降序
        self.neighbors.sort(reverse=True)
        self.neighbors = self.neighbors[:self.k]

    # 格式化userDict数据
    def formatuserDict(self, userId, l):
        user = {}
        for i in self.userDict[userId]:
            user[i[0]] = [i[1], 0]
        for j in self.userDict[l]:
            if (j[0] not in user):
                user[j[0]] = [0, j[1]]
            else:
                user[j[0]][1] = j[1]
        return user

    # 计算余弦距离
    def getCost(self, userId, l):
        # 获取用户userId和l评分电影的并集
        # {'电影ID'：[userId的评分，l的评分]} 没有评分为0
        user = self.formatuserDict(userId, l)
        x = 0.0
        y = 0.0
        z = 0.0
        for k, v in user.items():
            x += float(v[0]) * float(v[0])
            y += float(v[1]) * float(v[1])
            z += float(v[0]) * float(v[1])
        if (z == 0.0):
            return 0
        return z / sqrt(x * y)

    # 推荐的准确率
    def getPrecision(self, userId):
        user = [i[0] for i in self.userDict[userId]]
        recommand = [i[1] for i in self.recommandList]
        count = 0.0
        if (len(user) >= len(recommand)):
            for i in recommand:
                if (i in user):
                    count += 1.0
            self.cost = count / len(recommand)
        else:
            for i in user:
                if (i in recommand):
                    count += 1.0
            self.cost = count / len(user)

    # 显示推荐列表
    def showTable(self):
        neighbors_id = [i[1] for i in self.neighbors]
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(["t", "t", "t"])
        table.set_cols_align(["l", "l", "l"])
        rows = []
        rows.append([u"food ID", u"Name", u"from userID"])
        for item in self.recommandList:
            fromID = []
            for i in self.foods:
                if i[0] == item[1]:
                    food = i
                    break
            for i in self.ItemUser[item[1]]:
                if i in neighbors_id:
                    fromID.append(i)
            food.append(fromID)
            rows.append(food)
        table.add_rows(rows)
        print(table.draw())


def readFile(filename):
    files = open(filename, "r", encoding="utf-8-sig")
    data = []
    for line in files.readlines():
        item = line.strip().split(",")
        data.append(item)
    print(data)
    return data


# -------------------------Begin-------------------------------
start = time.process_time()

foods = readFile(r"C:\Users\78531\Desktop\FYP_code and dataset\milk.csv")
frequency = readFile(r"C:\Users\78531\Desktop\FYP_code and dataset\fre_milk.csv")
demo = CF(foods, frequency, k=20,n=20)
demo.recommendByUser("user")  # Recommending for 'user'
print("Recommendation Table：")
demo.showTable()
print('\n')
print("The Recommendation Table ends.")
print("Please enjoy yourself and have a nice day!")
print('\n')
print("Total number of users: %d" % (len(demo.frequency)))
#print("准确率： %.2f %%" % (demo.cost * 100))
end = time.process_time()
print("Time cost： %f s" % (end - start))