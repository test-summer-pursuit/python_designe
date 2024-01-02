import sys
# 引入PyQt6模块
from PyQt6.QtWidgets import QApplication, QMainWindow,QMessageBox
from PyQt6 import QtGui
import pre_cityid_csv, weatherui
import pandas as pd
import os
import get_1
import get_14
import get_csv




class MainWindow(QMainWindow, weatherui.Ui_weather_tool):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setCentralWidget(self.centralwidget)
        #将绑定按钮
        self.sure.clicked.connect(lambda :self.page_weather.setCurrentIndex(0))
        self.map.clicked.connect(lambda :self.do_show("长清"))
        self.today.clicked.connect(lambda :self.page_weather.setCurrentIndex(0))
        self.page_weather.setCurrentIndex(2)
        self.today.clicked.connect(lambda :self.do_show(self.search_city.text()))
        self.next_seven_day.clicked.connect(lambda :self.page_weather.setCurrentIndex(1))
        self.next_seven_day.clicked.connect(lambda :self.do_show(self.search_city.text()))
        ##绑定页面变化
        self.air_1.clicked.connect(lambda :self.page_weather.setCurrentIndex(5))
        self.hum_1.clicked.connect(lambda :self.page_weather.setCurrentIndex(4))
        self.wind_1.clicked.connect(lambda :self.page_weather.setCurrentIndex(6))
        self.temp_1.clicked.connect(lambda :self.page_weather.setCurrentIndex(3))
        self.temp_14.clicked.connect(lambda :self.page_weather.setCurrentIndex(9))
        self.weather_14.clicked.connect(lambda :self.page_weather.setCurrentIndex(8))
        self.wind_14.clicked.connect(lambda :self.page_weather.setCurrentIndex(7))
        self.return_11.clicked.connect(lambda :self.page_weather.setCurrentIndex(0))
        self.return_12.clicked.connect(lambda :self.page_weather.setCurrentIndex(0))
        self.return_13.clicked.connect(lambda :self.page_weather.setCurrentIndex(0))
        self.return_14.clicked.connect(lambda :self.page_weather.setCurrentIndex(0))
        self.return_21.clicked.connect(lambda :self.page_weather.setCurrentIndex(1))
        self.return_23.clicked.connect(lambda: self.page_weather.setCurrentIndex(1))
        self.return22.clicked.connect(lambda :self.page_weather.setCurrentIndex(1))

    ##下载绘制的图表
    def save_pic(self):
        get_1.main()
        get_14.main()

    ##展示字符页面
    def show_str(self,name,):
        file_path = '城市信息.csv'
        data = pd.read_csv(file_path, encoding='utf8')
        # 获取到城市名称
        city_name = data['city_name'].tolist()
        # 获取到城市URL
        city_url = data['city_id'].tolist()
        result = []
        ##当天详细信息
        url_now = "https://weather.cma.cn/api/now/" + str(city_url[city_name.index(name)])
        ##加入当天信息
        result.append(pre_cityid_csv.get_data(url_now))

        ##未来七天
        url_next = "https://weather.cma.cn/web/weather/" + str(city_url[city_name.index(name)]) + ".html"
        city_html = pre_cityid_csv.get_html(url_next)
        list = []
        ##加入七天信息title
        result.append(city_html.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/text()'))
        for i in range(1, 8):
            list_day = []
            for j in range(1, 3):
                day = f'//*[@id="dayList"]/div[{i}]/div[1]/text()[{j}]'
                list_day.append(city_html.xpath(day)[0].strip())
            for j in range(3, 6):
                weather = f'//*[@id="dayList"]/div[{i}]/div[{j}]/text()'
                list_day.append(city_html.xpath(weather)[0].strip())
            for j in range(1, 3):
                temper = f'//*[@id="dayList"]/div[{i}]/div[6]/div/div[{j}]/text()'
                list_day.append(city_html.xpath(temper)[0].strip())
            for j in range(8, 11):
                wind = f'//*[@id="dayList"]/div[{i}]/div[{j}]/text()'
                list_day.append(city_html.xpath(wind)[0].strip())
            list.append(list_day)
        ##加入七天信息
        result.append(list)
        # print(list)
        ##未来二十四小时
        list_day = []
        for i in range(1, 10):
            if (i == 2): continue
            title = f'//*[@id="hourTable_0"]/tbody/tr[{i}]/td[1]/text()'
            d = {city_html.xpath(title)[0]: []}
            for j in range(2, 10):
                content1 = f'//*[@id="hourTable_0"]/tbody/tr[{i}]/td[{j}]/text()'
                d[city_html.xpath(title)[0]].append(city_html.xpath(content1))
            list_day.append(d)
        ##加入未来24小时信息
        result.append(list_day)
        # print(list_day)
        self.city_now.setText(result[0]['location']['path'])
        self.tem_now.setText(str(result[0]['now']['temperature']))
        self.update_time.setText(result[0]['lastUpdate'])
        self.HPA.setText(str(result[0]['now']['pressure']))
        self.HUM.setText(str(result[0]['now']['humidity']))
        if (len(result[0]['alarm']) != 0):
            alarm = result[0]['alarm'][0]
            self.alarm.setText(alarm['signallevel'] + "预警：\n" + \
                               alarm['title'] + alarm['signaltype'] + \
                               "\n发布时间：" + alarm['effective'] + \
                               "\n请注意安全！")
        else:
            self.alarm.setText(" ")
        if (result[0]['now']['windDirection'] != '9999'):
            self.windDirection.setText(result[0]['now']['windDirection'])
        self.windScale.setText(result[0]['now']['windScale'])
        self.next_seven.setText(result[1][0].strip())

        title_to = [' 时间', ' 气温', ' 降水', ' 风速', ' 风向', ' 气压', ' 湿度', ' 云量']
        for i in range(0, 8):
            item = result[3][i][title_to[i]]
            for j in range(1, 9):
                exec(f"self.l{i + 1}{j}.setText(item[{j - 1}][0])")
        ####输出七天

        for i in range(1, 8):
            item = result[2]
            for j in range(0, 10):
                exec(f"self.label_1{j}{i}.setText(item[{i - 1}][{j}])")

        self.label_5.setText("白天")
        self.label_7.setText("夜间")

    def show_pic(self,name):
        file_path1 = '中国天气网城市信息.csv'
        data1 = pd.read_csv(file_path1, encoding='utf8')
        city_name1 = data1['city_name'].tolist()
        # 获取到城市URL
        city_url1 = data1['city_url'].tolist()
        url3 = 'http://www.weather.com.cn/weather/' + str(city_url1[city_name1.index(name)]) + '.shtml'  # 7天天气中国天气网
        url2 = 'http://www.weather.com.cn/weather15d/' + str(city_url1[city_name1.index(name)]) + '.shtml'  # 8-15天天气中国天气网

        html1 = get_csv.getHTMLtext(url3)
        data1, data1_7 = get_csv.get_content(html1)  # 获得1-7天和当天的数据

        html2 = get_csv.getHTMLtext(url2)
        data8_14 = get_csv.get_content2(html2)  # 获得8-14天数据
        data14 = data1_7 + data8_14
        # print(data)
        get_csv.write_to_csv('weather14.csv', data14, 14)  # 保存为csv文件
        get_csv.write_to_csv('weather1.csv', data1, 1)
        self.save_pic()
        get_14.main()##绘制14天的可视图
        get_1.main()##绘制当天可视图
        ##将可视图与页面绑定进行展示
        pixmap1 = QtGui.QPixmap('./image/air1.png')
        pixmap2=  QtGui.QPixmap('./image/hum1.png')
        pixmap3=  QtGui.QPixmap('./image/wind1.png')
        pixmap4=  QtGui.QPixmap('./image/temp1.png')
        pixmap5=  QtGui.QPixmap('./image/temp14.png')
        pixmap6=  QtGui.QPixmap('./image/weather14.png')
        pixmap7=  QtGui.QPixmap('./image/wind14.png')
        self.label_air1.setPixmap(pixmap1)
        self.label_hum1.setPixmap(pixmap2)
        self.label_wind1.setPixmap(pixmap3)
        self.label_temp1.setPixmap(pixmap4)
        self.label_temp14.setPixmap(pixmap5)
        self.label_wind14.setPixmap(pixmap7)
        self.label_weather14.setPixmap(pixmap6)

    #展示页面信息
    def do_show(self,name1):
        ##使用第一个网站的数据
        pre_cityid_csv.main1()
        file_path = '城市信息.csv'
        data = pd.read_csv(file_path, encoding='utf8')
        # 获取到城市名称
        city_name = data['city_name'].tolist()
        # 让用户输入需要查询的城市
        name=name1
        ##使用第二个网站的数据
        file_path1='中国天气网城市信息.csv'
        data1 = pd.read_csv(file_path1, encoding='utf8')
        # 获取到城市名称
        city_name1 = data1['city_name'].tolist()
        ##存储爬到信息
        if name in city_name and name in city_name1:
            self.show_str(name)
            self.show_pic(name)
        else:
            QMessageBox.warning(self, "信息提示","输入的城市名称有误！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())