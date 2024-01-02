import requests
import json
import csv
from lxml import etree
import pandas as pd
import os


##共爬取两个天气网站
##获取页面
def get_html(url):##第一个网站
    # 定义头文件
    headers = {'user-agent': 'Mozilla/5.0 ',
               'Host': 'www.weather.com.cn'
               }
    # 发起请求
    response = requests.get(url,headers=headers)
    # 修改编码
    response.encoding = 'utf8'
    # 处理成HTML格式
    html = etree.HTML(response.text)
    return html
##获取城市信息
def get_data(url):
    headers = {'user-agent': 'Mozilla/5.0 ',
               'Host': 'www.weather.com.cn'
               }
    # 发起请求
    response = requests.get(url, headers=headers)
    # 修改编码
    response.encoding = 'utf8'
    dict_data = json.loads(response.text)["data"]
    return dict_data

##将城市信息写入文件
def get_city(url):
    headers = {'user-agent': 'Mozilla/5.0 '
               }
    res = requests.get(url, headers)
    res.encoding = 'utf-8'
    citystr = res.text
    cityjson = json.loads(citystr)
    city_list = cityjson["data"]["city"]
    with open("城市信息.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        header = ["city_name", "city_id"]
        writer.writerow(header)
        for city in city_list:
            writer.writerow([city[1], city[0]])

def get_html1(url):
    # 定义头文件
    headers = {'user-agent': 'Mozilla/5.0 ',
               'Host': 'www.weather.com.cn'
               }
    # 发起请求
    response = requests.get(url, headers=headers)
    # 修改编码
    response.encoding = 'utf8'
    # 处理成HTML格式
    html = etree.HTML(response.text)
    return html

# 获取城市信息并保存到本地
def get_cityinfo_write1(html):
    print('获取城市信息')
    city_info = {}
    # 获取到城市信息
    province_url = html.xpath('//div[@class="lqcontentBoxheader"]//ul//li/a/@href')
    for i in range(len(province_url)):
        # 拼接出每个城市的URL，并获取到对应的HTML
        the_html = get_html1('http://www.weather.com.cn' + province_url[i])
        # 解析出城市名称
        city_name = the_html.xpath('//div[@class="conMidtab3"]//tr//td[position()<3]/a/text()')

        # 解析出城市链接
        city_url = the_html.xpath('//div[@class="conMidtab3"]//tr//td[position()<3]/a/@href')
        # 将城市信息存储到city_info中
        for j in range(len(city_name)):
            if j != 0 and city_name[j] == city_name[0]:
                break
            else:
                city_info[city_name[j]] = city_url[j][34:43]
    # 给数据设置列名
    data = pd.DataFrame(columns=['city_name', 'city_url'])
    # 填充数据
    data['city_name'] = city_info.keys()
    data['city_url'] = city_info.values()
    # 保存到本地
    data.to_csv(file_path, index=False, encoding='utf8')

def main1():
    url = "https://weather.cma.cn/api/map/weather/1?t=1702210667325"
    file_path = '城市信息.csv'
    # 判断存放城市信息的数据文件是否存在。如果不存在，则调用get_cityinfo_write方法下载
    if not os.path.exists(file_path):
        get_city(url)
    url1 = 'http://www.weather.com.cn/textFC/hb.shtml'
    # 调用获取HTML的方法
    html1 = get_html1(url1)
    file_path1 = 'C:/Users/29753/PycharmProjects/pythonProject/python_design/中国天气网城市信息.csv'
    # 判断存放城市信息的数据文件是否存在。如果不存在，则调用get_cityinfo_write方法下载
    if not os.path.exists(file_path1):
        get_cityinfo_write1(html1)


if __name__ == '__main__':
    url = "https://weather.cma.cn/api/map/weather/1?t=1702210667325"
    file_path = '城市信息.csv'
    # 判断存放城市信息的数据文件是否存在。如果不存在，则调用get_cityinfo_write方法下载
    if not os.path.exists(file_path):
        get_city(url)
    data = pd.read_csv(file_path, encoding='utf8')
    # 获取到城市名称
    city_name = data['city_name'].tolist()
    # 获取到城市URL
    city_url = data['city_id'].tolist()
    url1 = 'http://www.weather.com.cn/textFC/hb.shtml'
    # 调用获取HTML的方法
    html1 = get_html1(url1)
    file_path1 = '中国天气网城市信息.csv'
    # 判断存放城市信息的数据文件是否存在。如果不存在，则调用get_cityinfo_write方法下载
    if not os.path.exists(file_path1):
        get_cityinfo_write1(html1)
    # 读取城市信息
    data1 = pd.read_csv(file_path1, encoding='utf8')
    # 获取到城市名称
    city_name1 = data1['city_name'].tolist()
    # 获取到城市URL
    city_url1 = data1['city_url'].tolist()
    # 让用户输入需要查询的城市
    name = input('请输入需要查询的城市名称：')
    if name in city_name and name in city_name1:
        ##当天详细信息
        url_now="https://weather.cma.cn/api/now/"+str(city_url[city_name.index(name)])
        print(get_data(url_now))

        ##未来七天
        url_next="https://weather.cma.cn/web/weather/"+str(city_url[city_name.index(name)])+".html"
        city_html=get_html(url_next)
        list=[]
        print(city_html.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/text()'))
        for i in range(2,8):
            list_day = []
            for j in range(1,3):
                day=f'//*[@id="dayList"]/div[{i}]/div[1]/text()[{j}]'
                list_day.append(city_html.xpath(day)[0].strip())
            for j in range(3,6):
                weather=f'//*[@id="dayList"]/div[{i}]/div[{j}]/text()'
                list_day.append(city_html.xpath(weather)[0].strip())
            for j in range(1,3):
                temper=f'//*[@id="dayList"]/div[{i}]/div[6]/div/div[{j}]/text()'
                list_day.append(city_html.xpath(temper)[0].strip())
            for j in range(8,11):
                wind=f'//*[@id="dayList"]/div[{i}]/div[{j}]/text()'
                list_day.append(city_html.xpath(wind)[0].strip())
            list.append(list_day)
        print(list)
        ##未来二十四小时        list_day = []
        for i in range(1, 10):
            if(i==2) :continue
            title = f'//*[@id="hourTable_0"]/tbody/tr[{i}]/td[1]/text()'
            d = {city_html.xpath(title)[0]:[]}
            for j in range(2, 10):
                content1 = f'//*[@id="hourTable_0"]/tbody/tr[{i}]/td[{j}]/text()'
                d[city_html.xpath(title)[0]].append(city_html.xpath(content1))
            list_day.append(d)
        print(list_day)

        city_html1 = get_html1('http://www.weather.com.cn/weather/' + str(city_url[city_name.index(name)]) + '.shtml')
        print(city_url[city_name.index(name)])
        print(type(city_url[city_name.index(name)]))
        print('http://www.weather.com.cn/weather/' + '(city_url[city_name.index(name)]' + '.shtml')
    else:
        print('输入的城市名称有误！')

