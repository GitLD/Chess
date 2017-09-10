#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'LuDi'
# Date: 2017/9/9
# Version: 2.0
import random
import tkinter.messagebox
from tkinter import *
from copy import deepcopy


class Point(object):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]


class FiveChess(object):
    """
    五子棋类
    """

    def __init__(self):
        # Set Parameter
        self.size = 20  # 棋盘规模
        self.now = random.randint(1, 2)  # 落子标识位[1:玩家,2:电脑]
        self.colors_map = {1: 'white', 2: 'white', self.now: 'black'}  # 设置落子颜色
        self.chess_code = ''  # 棋型
        self.flag = False  # 结束标志位
        # 保存棋盘权值
        self.chess_Value = [[0 for i in range(self.size + 1)] for i in range(self.size + 1)]
        self.dic = {"0": 0, "1": 8, "2": 10, "11": 50, "22": 1000, "111": 3500, "222": 3000, "1111": 5000,
                    "2222": 20000,
                    "21": 4, "12": 2, "211": 25, "122": 20, "11112": 3000, "112": 30, "1112": 2800, "221": 500,
                    "2221": 2000,
                    "22221": 10000}

        self.chess_past = [[0 for i in range(self.size + 1)] for i in range(self.size + 1)]  # 棋盘记录(上一步)
        self.chess_now = deepcopy(self.chess_past)  # 棋盘记录(下一步)

        self.tk = Tk()
        self.tk.title('五子棋')
        self.tk.resizable(False, False)
        self.width = 30 * self.size + 20
        self.height = 30 * self.size + 20
        self.tk.geometry('%dx%d' % (self.width + 10, self.height + 10))
        self.canvas = Canvas(self.tk, width=self.width, height=self.height, background='white')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.draw_chessboard()
        if self.now == 2:
            self.ai_first_point()
        self.canvas.bind('<Button-1>', self.run)
        self.canvas.bind('<Button-3>', self.rollback)
        self.tk.mainloop()

    def draw_chessboard(self):
        """
        绘制棋盘
        :return:
        """
        for num in range(1, self.size + 1):
            self.canvas.create_line(num * 30, 30, num * 30, self.size * 30, width=2)
        for num in range(1, self.size + 1):
            self.canvas.create_line(30, num * 30, self.size * 30, num * 30, width=2)

    def draw_chessman(self, point):
        """
        绘制棋子
        :param point:坐标点Point对象
        :return: True/False
        """
        if point.x % 30 > 15:
            point.x = point.x // 30 + 1
        else:
            point.x = point.x // 30
        if point.y % 30 > 15:
            point.y = point.y // 30 + 1
        else:
            point.y = point.y // 30
        if point.x > self.size:
            point.x = self.size
        if point.y > self.size:
            point.y = self.size
        if point.x < 1:
            point.x = 1
        if point.y < 1:
            point.y = 1

        # Chess Draw
        x1, y1 = (point.x * 30 - 15), (point.y * 30 - 15)
        x2, y2 = (point.x * 30 + 15), (point.y * 30 + 15)
        if self.chess_now[point.x][point.y] == 0:
            color = self.colors_map[self.now]
            self.canvas.create_oval(x1, y1, x2, y2, fill=color)
            self.chess_now[point.x][point.y] = self.now
            self.is_over(point)
            self.change()
            return True
        else:
            return False

    def change(self):
        """
        改变落子玩家
        :return:
        """
        if self.now == 1:
            self.now = 2
        else:
            self.now = 1

    # 结束判定
    def is_over_horizental(self, point):
        """
        检查水平方向是否存在5子以上情形
        :param point: 上次落子点Point对象
        :return:Ture[Game Over]/False[Continue]
        """
        count = 0
        x = point.x
        y = point.y
        for i in range(x + 1, 17):
            if self.chess_now[i][y] == self.chess_now[x][y]:
                count += 1
            else:
                break
        for i in range(x, 0, -1):
            if self.chess_now[i][y] == self.chess_now[x][y]:
                count += 1
            else:
                break
        if count >= 5:
            return True
        else:
            return False

    def is_over_vertical(self, point):
        """
        检查竖直方向是否存在5子以上情形
        :param point: 上次落子点Point对象
        :return:Ture[Game Over]/False[Continue]
        """
        count = 0
        x = point.x
        y = point.y
        for i in range(y + 1, 17):
            if self.chess_now[x][i] == self.chess_now[x][y]:
                count += 1
            else:
                break
        for i in range(y, 0, -1):
            if self.chess_now[x][i] == self.chess_now[x][y]:
                count += 1
            else:
                break
        if count >= 5:
            return True
        else:
            return False

    def is_over_diagonal1(self, point):
        """
        检查主对角线方向是否存在5子以上情形
        :param point: 上次落子点Point对象
        :return:Ture[Game Over]/False[Continue]
        """
        count = 0
        x = point.x
        y = point.y
        for i, j in zip(range(x + 1, 17), range(y + 1, 17)):
            if self.chess_now[i][j] == self.chess_now[x][y]:
                count += 1
            else:
                break
        for i, j in zip(range(x, 0, -1), range(y, 0, -1)):
            if self.chess_now[i][j] == self.chess_now[x][y]:
                count += 1
            else:
                break
        if count >= 5:
            return True
        else:
            return False

    def is_over_diagonal2(self, point):
        """
        检查副对角线方向是否存在5子以上情形
        :param point: 上次落子点Point对象
        :return:Ture[Game Over]/False[Continue]
        """
        count = 0
        x = point.x
        y = point.y
        for i, j in zip(range(x - 1, 0, -1), range(y + 1, 17)):
            if self.chess_now[i][j] == self.chess_now[x][y]:
                count += 1
            else:
                break
        for i, j in zip(range(x, 17), range(y, 0, -1)):
            if self.chess_now[i][j] == self.chess_now[x][y]:
                count += 1
            else:
                break
        if count >= 5:
            return True
        else:
            return False

    def is_over(self, point):
        """
        判定落子后,游戏是否结束
        :param point: 上次落子点Point对象
        :return:
        """
        if self.chess_now[point.x][point.y] == 1:
            text = '玩家获胜!\n是否重新开始？'
        else:
            text = '电脑获胜!\n是否重新开始？'

        flag1 = self.is_over_horizental(point)
        flag2 = self.is_over_vertical(point)
        flag3 = self.is_over_diagonal1(point)
        flag4 = self.is_over_diagonal2(point)
        self.flag = flag1 or flag2 or flag3 or flag4
        if self.flag:
            answer = tkinter.messagebox.askquestion("提示", text)
            if answer == 'yes':
                self.tk.destroy()
                self.__init__()
            else:
                self.tk.destroy()
                exit()

    def restart(self):
        self.now = random.randint(1, 2)  # 落子标识位[1:玩家,2:电脑]
        self.colors_map = {1: 'white', 2: 'white', self.now: 'black'}  # 设置落子颜色
        self.chess_code = ''  # 棋型
        self.flag = False  # 结束标志位
        # 保存棋盘权值
        self.chess_Value = [[0 for i in range(self.size + 1)] for i in range(self.size + 1)]
        pass

    # AI
    def estimate_temp_x(self, i, j, iteration):
        code = ""
        chess_color = 0
        for x in iteration:
            # 如果左右方向的第一位置为空就跳出循环
            if self.chess_now[x][j] == 0:
                break
            else:
                if chess_color == 0:  # 这是左右方向第一颗棋子
                    code += str(self.chess_now[x][j])  # 记录它的颜色
                    chess_color = self.chess_now[x][j]  # 保存它的颜色
                else:
                    if chess_color == self.chess_now[x][j]:  # 跟第一颗棋子颜色相同
                        code += str(self.chess_now[x][j])  # 记录它的颜色
                    else:  # 左右方向找到一颗不同颜色的棋子
                        code += str(self.chess_now[x][j])
                        break
        # 取出对应的权值
        value = self.dic.get(code)
        if value:
            self.chess_Value[i][j] += value

    def estimate_temp_y(self, i, j, iteration):
        code = ""
        chess_color = 0
        #  上下方向
        for y in iteration:
            #  如果上下方向的第一位置为空就跳出循环
            if self.chess_now[i][y] == 0:
                break
            else:
                if chess_color == 0:  # 这是上下方向第一颗棋子
                    code += str(self.chess_now[i][y])  # 记录它的颜色
                    chess_color = self.chess_now[i][y]  # 保存它的颜色
                else:
                    if chess_color == self.chess_now[i][y]:  # 跟第一颗棋子颜色相同
                        code += str(self.chess_now[i][y])  # 记录它的颜色
                    else:  # 上下方向找到一颗不同颜色的棋子
                        code += str(self.chess_now[i][y])
                        break
        # 取出对应的权值
        value = self.dic.get(code)
        if value:
            self.chess_Value[i][j] += value
        pass

    def estimate_temp_xy(self, i, j, iteration1, iteration2):
        code = ""
        chess_color = 0
        for x, y in zip(iteration1, iteration2):
            # 如果向对角的第一位置为空就跳出循环
            if self.chess_now[x][y] == 0:
                break
            else:
                if chess_color == 0:  # 这是对角第一颗棋子
                    code += str(self.chess_now[x][y])  # 记录它的颜色
                    chess_color = self.chess_now[x][y]  # 保存它的颜色
                else:
                    if chess_color == self.chess_now[x][y]:  # 跟第一颗棋子颜色相同
                        code += str(self.chess_now[x][y])  # 记录它的颜色
                    else:  # 对角找到一颗不同颜色的棋子
                        code += str(self.chess_now[x][y])
                        break
        # 取出对应的权值
        value = self.dic.get(code)
        if value:
            self.chess_Value[i][j] += value
        pass

    def ai(self):
        """
        简易AI
        :return:AI落点
        """
        self.chess_Value = [[0 for i in range(self.size + 1)] for i in range(self.size + 1)]
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.chess_now[i][j] == 0:
                    self.estimate_temp_x(i, j, range(i + 1, self.size + 1))
                    self.estimate_temp_x(i, j, range(i - 1, 0, -1))
                    self.estimate_temp_y(i, j, range(j - 1, 0, -1))
                    self.estimate_temp_y(i, j, range(j + 1, self.size + 1))
                    self.estimate_temp_xy(i, j, range(i - 1, 0, -1), range(j + 1, self.size + 1))
                    self.estimate_temp_xy(i, j, range(i + 1, self.size + 1), range(j - 1, 0, -1))
                    self.estimate_temp_xy(i, j, range(i - 1, 0, -1), range(j - 1, 0, -1))
                    self.estimate_temp_xy(i, j, range(i + 1, self.size + 1), range(j + 1, self.size + 1))

        score_max = max([max(l) for l in self.chess_Value])
        points_list = []
        for a in range(1, self.size + 1):
            for b in range(1, self.size + 1):
                if self.chess_now[a][b] == 0:
                    if self.chess_Value[a][b] == score_max:
                        point = Point([30 * a, 30 * b])
                        points_list.append(point)
        p = random.choice(points_list)
        return p

    def ai_first_point(self):
        """
        AI 先手下的第一个点
        :return:
        """
        low = self.size//2 - self.size//8
        up = self.size//2 + self.size//8
        x = random.randint(low, up)
        y = random.randint(low, up)
        pos = [30 * x, 30 * y]
        point = Point(pos)
        self.draw_chessman(point)

    # 响应函数
    def run(self, event):
        """
        左键落子
        :param event:
        :return:
        """
        point_human = Point([event.x, event.y])
        self.chess_past = deepcopy(self.chess_now)
        if self.draw_chessman(point_human):
            point_pc = self.ai()
            self.draw_chessman(point_pc)

    def rollback(self, event):
        """
        右键后撤一步(玩家、电脑均退一步)
        :param event:
        :return:
        """
        self.canvas.delete(ALL)
        self.draw_chessboard()
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.chess_past[i][j] != 0:
                    x1, y1 = (i * 30 - 15), (j * 30 - 15)
                    x2, y2 = (i * 30 + 15), (j * 30 + 15)
                    color = self.colors_map[self.chess_past[i][j]]
                    self.canvas.create_oval(x1, y1, x2, y2, fill=color)
        self.chess_now = self.chess_past


if __name__ == '__main__':
    chess = FiveChess()
