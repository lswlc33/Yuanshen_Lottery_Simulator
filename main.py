import sys, configparser, random, time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Ui_untitled import *
import res_rc, ast

# 抽卡概率
prob_5 = ""
prob_4 = ""
# 卡池列表
list_3 = ""
list_4_1 = ""
list_4_2 = ""
list_5_1 = ""
list_5_2 = ""
# 保底数
luck_4 = 0
luck_5 = 0


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 添加字体
        fontDb = QFontDatabase()
        fontID = fontDb.addApplicationFont(":/font/res/zh-cn.ttf")
        fontFamilies = fontDb.applicationFontFamilies(fontID)
        print(fontFamilies)
        self.setFont(QFont("SDK_SC_Web"))
        # 初始化窗口
        self.setupUi(self)
        self.init()
        self.pushButton.mousePressEvent = self.danchou
        self.pushButton_2.mousePressEvent = self.shilian
        self.pushButton_3.mousePressEvent = self.goto_chongzhi
        self.pushButton_4.mousePressEvent = self.goto_chouka
        self.frame_17.mousePressEvent = self.fenqiu__goumai
        self.frame.mousePressEvent = self.yuanshi__goumai
        # 无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

    # 无边框窗口的移动
    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def mouseMoveEvent(self, e: QMouseEvent):
        try:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except:
            pass

    def init(self):
        self.init_ini()
        self.init_outputbox()

    def init_ini(self):
        # 确认配置文件是否存在
        try:
            f = open("setting.ini")
            f.close()
            print("找到配置文件\n")
        except IOError:
            # 创建配置
            config = configparser.ConfigParser()
            # 加载配置
            config["money"] = {
                "yuanshi": "160",
                "fenqiu": "160",
            }
            luck_4
            config["luck"] = {
                "luck_4": "0",
                "luck_5": "0",
            }
            config["probability"] = {
                "prob_5": "0.6",
                "prob_4": "5.1",
            }
            config["pool"] = {
                "list_3": [
                    "黎明神剑",
                    "以理服人",
                    "冷刀",
                    "黑缨枪",
                    "弹弓",
                    "神射手之誓",
                    "鸦羽弓",
                    "讨龙英杰谭",
                    "沐浴龙血的剑",
                    "飞天御剑",
                    "翡玉法球",
                    "魔导绪论",
                    "铁影阔剑",
                ],
                "list_4_1": ["珐露珊", "五郎", "烟绯"],
                "list_4_2": [
                    "坎蒂丝",
                    "柯莱",
                    "云董" "九条",
                    "裟罗" "托马",
                    "辛焱",
                    "迪奥娜",
                    "诺艾尔",
                    "莱依拉",
                    "多莉",
                    "久岐忍",
                    "鹿野院平藏",
                    "早柚",
                    "罗莎莉亚",
                    "砂糖",
                    "重云",
                    "班尼特",
                    "菲谢尔",
                    "行秋",
                    "香菱",
                    "芭芭拉",
                    "祭礼弓",
                    "西风猎弓",
                    "祭礼残章",
                    "西风秘典",
                    "匣里灭辰",
                    "凝光",
                    "北斗",
                    "雷泽",
                    "弓藏",
                    "绝弦",
                    "昭心",
                    "流浪乐章",
                    "西风长枪",
                    "雨裁",
                    "祭礼大剑",
                    "西风大剑",
                    "祭礼剑",
                    "西风剑",
                    "钟剑",
                    "甲里龙吟",
                    "笛剑",
                ],
                "list_5_1": ["流浪者"],
                "list_5_2": ["提纳里", "刻晴", "莫娜", "七七", "迪卢克", "琴"],
            }
            # 创建ini文件
            with open("setting.ini", "w") as configfile:
                # 写入配置
                config.write(configfile)
            print("初始化应用配置完成！\n")

    def init_outputbox(self):
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        global prob_5, prob_4, list_3, list_4_1, list_4_2, list_5_1, list_5_2, luck_4, luck_5

        prob_5 = config.getfloat("probability", "prob_5")
        prob_4 = config.getfloat("probability", "prob_4")

        list_3 = ast.literal_eval(config.get("pool", "list_3"))
        list_4_1 = ast.literal_eval(config.get("pool", "list_4_1"))
        list_4_2 = ast.literal_eval(config.get("pool", "list_4_2"))
        list_5_1 = ast.literal_eval(config.get("pool", "list_5_1"))
        list_5_2 = ast.literal_eval(config.get("pool", "list_5_2"))

        luck_4 = config.get("luck", "luck_4")
        luck_5 = config.get("luck", "luck_5")

        dict1 = dict(config.items("money"))
        # 设置显示金钱
        self.label_11.setText(dict1["yuanshi"])
        self.label_13.setText(dict1["fenqiu"])
        self.label_23.setText(dict1["yuanshi"])
        self.label_25.setText(dict1["fenqiu"])
        # 输出窗口
        self.plainTextEdit.setPlainText(
            "左下个是抽卡喵~~\n关注雪中明月喵~~\n没有钱吃饭了喵~~\n求三连好不好喵~~\n" + "-" * 24
        )

    def goto_chongzhi(self, event):
        # 进入充值界面
        self.stackedWidget.setCurrentIndex(1)
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        fenqiu = config.getint("money", "fenqiu")
        yuanshi = config.getint("money", "yuanshi")

        self.label_13.setText(str(fenqiu))
        self.label_25.setText(str(fenqiu))
        self.label_11.setText(str(yuanshi))
        self.label_23.setText(str(yuanshi))

    def goto_chouka(self, event):
        # 进入抽卡界面
        self.stackedWidget.setCurrentIndex(0)
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        fenqiu = config.getint("money", "fenqiu")
        yuanshi = config.getint("money", "yuanshi")

        self.label_13.setText(str(fenqiu))
        self.label_25.setText(str(fenqiu))
        self.label_11.setText(str(yuanshi))
        self.label_23.setText(str(yuanshi))

    def fenqiu_jian(self):
        # 纠缠之缘的减扣事件
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        fenqiu = config.getint("money", "fenqiu")
        fenqiu = fenqiu - 1
        config.set("money", "fenqiu", str(fenqiu))
        config.write(open("setting.ini", "w"))

        self.label_13.setText(str(fenqiu))
        self.label_25.setText(str(fenqiu))

    def fenqiu_jian_10(self):
        # 纠缠之缘的减扣事件 * 10
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        fenqiu = config.getint("money", "fenqiu")
        fenqiu = fenqiu - 10
        config.set("money", "fenqiu", str(fenqiu))
        config.write(open("setting.ini", "w"))

        self.label_13.setText(str(fenqiu))
        self.label_25.setText(str(fenqiu))

    def danchou(self, event):
        # 单抽函数
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        fenqiu = config.getint("money", "fenqiu")

        if fenqiu < 1:
            QMessageBox.information(self, "失败", "纠缠之缘不足！")
        else:
            try:
                self.fenqiu_jian()
            except PermissionError:
                pass
            try:
                self.choujiang()
            except PermissionError:
                self.choujiang()
            self.plainTextEdit.appendPlainText("-" * 24)

    def fenqiu__goumai(self, event):
        # 纠缠之缘的购买
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        fenqiu = config.getint("money", "fenqiu")
        yuanshi = config.getint("money", "yuanshi")

        if yuanshi < 1600:
            QMessageBox.information(self, "失败", "原石不足！")
        else:
            fenqiu = fenqiu + 10
            yuanshi = yuanshi - 1600

        config.set("money", "fenqiu", str(fenqiu))
        config.set("money", "yuanshi", str(yuanshi))
        config.write(open("setting.ini", "w"))

        self.label_13.setText(str(fenqiu))
        self.label_25.setText(str(fenqiu))
        self.label_11.setText(str(yuanshi))
        self.label_23.setText(str(yuanshi))

    def yuanshi__goumai(self, event):
        # 原石的购买
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        yuanshi = config.getint("money", "yuanshi")
        yuanshi = yuanshi + 6480
        config.set("money", "yuanshi", str(yuanshi))
        config.write(open("setting.ini", "w"))

        self.label_11.setText(str(yuanshi))
        self.label_23.setText(str(yuanshi))

    def shilian(self, event):
        # 十连
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        fenqiu = config.getint("money", "fenqiu")

        if fenqiu < 10:
            QMessageBox.information(self, "失败", "纠缠之缘不足！")
        else:
            try:
                self.fenqiu_jian_10()
            except PermissionError:
                pass
            for i in range(10):
                try:
                    self.choujiang()
                except PermissionError:
                    self.choujiang()
            self.plainTextEdit.appendPlainText("-" * 15)

    def choujiang(self):
        # 抽卡主要函数，概率等
        global luck_4, luck_5
        config = configparser.ConfigParser()
        config.read("setting.ini", encoding="gbk")
        result_1 = random.randint(1, 1000)

        luck_4 = int(config.get("luck", "luck_4"))
        luck_5 = int(config.get("luck", "luck_5"))
        # 四星保底
        if luck_4 >= 10:
            luck_4 = 0
            luck_5 = luck_5 + 1
            if random.randint(0, 1) == 1:
                ch_name = random.choice(list_4_1)
                result_2 = "[四星]  " + ch_name

            else:
                ch_name = random.choice(list_4_2)
                result_2 = "[四星]  " + ch_name
        # 五星保底
        elif luck_5 >= 80:
            luck_5 = 0
            luck_4 = luck_4 + 1
            if random.randint(0, 1) == 1:
                ch_name = random.choice(list_5_1)
                result_2 = "[五星]  " + ch_name

            else:
                ch_name = random.choice(list_5_2)
                result_2 = "[五星]  " + ch_name
        # 正常抽卡
        else:
            # 三星抽卡
            if 0 <= result_1 <= 1000 - prob_4 * 10 - prob_5 * 10:
                luck_4 = luck_4 + 1
                luck_5 = luck_5 + 1
                ch_name = random.choice(list_3)
                result_2 = "[三星]  " + ch_name
            # 四星抽卡
            elif 1000 - prob_4 * 10 - prob_5 * 10 <= result_1 <= 1000 - prob_5 * 10:
                luck_5 = luck_5 + 1
                luck_4 = 0
                if random.randint(0, 1) == 1:
                    ch_name = random.choice(list_4_1)
                    result_2 = "[四星]  " + ch_name

                else:
                    ch_name = random.choice(list_4_2)
                    result_2 = "[四星]  " + ch_name
            # 五星抽卡
            else:
                luck_5 = 0
                luck_4 = luck_4 + 1
                if random.randint(0, 1) == 1:
                    ch_name = random.choice(list_5_1)
                    result_2 = "[五星]  " + ch_name

                else:
                    ch_name = random.choice(list_5_2)
                    result_2 = "[五星]  " + ch_name

        config.set("luck", "luck_4", str(luck_4))
        config.set("luck", "luck_5", str(luck_5))
        config.write(open("setting.ini", "w"))

        self.plainTextEdit.appendPlainText(result_2)
        self.plainTextEdit.moveCursor(QTextCursor.End)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = MainWindow()
    a.show()
    sys.exit(app.exec_())
