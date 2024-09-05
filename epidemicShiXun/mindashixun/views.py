import json

import pymysql
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html")


# 从数据库当中获取数据,然后封装成字典
'''
1.连接数据库
2.获取游标
3.执行sql语句
4.获取结果
5.进行封装
'''


def getConnection():
    # 获取连接
    con = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="mindasx")
    # 获取游标:执行sql语句,获取结果
    cur = con.cursor()
    return cur


def getConfirmedAndCured(request):
    cur = getConnection()
    # sql语句:获取到全国感染和治愈总人数
    sql = "SELECT SUM(confirmedCount),SUM(curedCount) FROM info WHERE cityName IS NULL "
    # 执行sql语句
    cur.execute(sql)
    # 获取结果 获取到查询的结果
    result = cur.fetchall()
    print(result)
    # 封装数据
    dictData = {}  # 用来装封装的数据  因为前端代码是json类型,key:value,在这儿就可以用字典装数据,然后转化为json返回带前端
    for i in result:
        dictData["ConfirmedCount"] = i[0].to_eng_string()  # to_eng_string()可将数据库查询到的Decimal类型数据转化为str
        dictData["CuredCount"] = i[1].to_eng_string()
    # 使用HttpResponse返回结果,并且将字典数据通过json.dumps方法转化成json类型的数据
    return HttpResponse(json.dumps(dictData), content_type="application/json")


def getConfirmedTopSeven(request):
    # 获取数据库连接,获取游标
    cur = getConnection()
    # sql语句:获取感染前七的省份
    sql = "SELECT provinceShortName,confirmedCount FROM info WHERE cityName is NULL ORDER BY confirmedCount DESC LIMIT 0,7"
    # 执行sql语句
    cur.execute(sql)
    # 获取结果
    result = cur.fetchall()
    # 封装数据
    listName = []  # 装省份名称的列表
    listConfirmedCount = []  # 装感染人数的列表
    for i in result:
        listName.append(i[0])
        listConfirmedCount.append(i[1])
    print(listName)
    print(listConfirmedCount)
    dictInfo = {"listName": listName, "listConfirmedCount": listConfirmedCount}
    return HttpResponse(json.dumps(dictInfo), content_type="application/json")


def getSCConfirmedTopFive(request):
    # 四川前五感染的地区以及感染人数
    cur = getConnection()
    sql = "SELECT info.cityName, info.curedCount FROM info WHERE info.cityName IS NOT NULL AND info.provinceShortName = '四川' ORDER BY info.curedCount DESC LIMIT 1, 5"
    cur.execute(sql)
    result = cur.fetchall()
    # 封装结果
    listCityName = []
    listDict = []
    for i in result:
        listCityName.append(i[0])
        listDict.append({"name": i[0], "value": i[1]})  # i[0]为地区名称,i[1]为对应的数据
    dictInfo = {"listCityName": listCityName, "listDict": listDict}
    return HttpResponse(json.dumps(dictInfo), content_type="application/json")


def getMap(request):
    cur = getConnection()
    sql = "SELECT provinceShortName,confirmedCount FROM info WHERE cityName is NULL "
    cur.execute(sql)
    result = cur.fetchall()
    listDict = []
    for i in result:
        dictData = {}
        dictData["name"] = i[0]
        dictData["value"] = i[1]
        listDict.append(dictData)
    print(listDict)
    dictInfo = {"listDict": listDict}
    return HttpResponse(json.dumps(dictInfo), content_type="application/json")


def getConfirmedCuredDead(request):
    # 目的  地区名称 感染 治愈 死亡
    cur = getConnection()
    sql = "SELECT cityName, confirmedCount, curedCount, deadCount FROM info WHERE cityName IS NOT NULL ORDER BY confirmedCount DESC LIMIT 0, 8"
    cur.execute(sql)
    result = cur.fetchall()
    listCityName = []
    listConfirmed = []
    listCured = []
    listDead = []
    for i in result:
        listCityName.append(i[0])
        listConfirmed.append(i[1])
        listCured.append(i[2])
        listDead.append(i[3])
    dictInfo = {"listCityName": listCityName, "listConfirmed": listConfirmed, "listCured": listCured,
                "listDead": listDead}
    return HttpResponse(json.dumps(dictInfo), content_type="application/json")
