# -*- coding: utf-8 -*-
# 创建一个矩形，指定画布的颜色为白色
import copy
import time
from tkinter import *
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
import operator

points = list()
window = list()
line = list()
tk = Tk()

tk.state('zoomed')
tk.update()

tk.title("直线与多边形裁剪")
# 创建一个Canvas，设置其背景色为白色
cv = Canvas(tk, bg='white')
normal_ddl = Label(tk, text="图形")
ddl = ttk.Combobox(tk)
ddl['value'] = ('直线裁剪', '多边形裁剪')
ddl['state'] = 'readonly'
ddl.current(1)
ddl.pack()
width = tk.winfo_width()
height = tk.winfo_height()


def interBresenham(x0, y0, x1, y1, color):
    if x0 == x1:
        down = min(y0, y1)
        up = max(y0, y1)
        for i in range(down, up + 1, 1):
            cv.create_line(int(x0), int(i), int(x0 + 1), int(i + 1), fill=color)
    else:
        e = 0
        dx = x1 - x0
        dy = y1 - y0
        k = dy / dx
        if 0 <= k <= 1:
            if x0 < x1:
                e = x0 - x1
                dx = x1 - x0
                dy = y1 - y0
                x = x0
                y = y0
            else:
                e = x1 - x0
                dx = x0 - x1
                dy = y0 - y1
                x = x1
                y = y1
            for i in range(int(dx)):
                cv.create_line(int(x), int(y), int(x + 1), int(y + 1), fill=color)
                x = x + 1
                e = e + 2 * dy
                if e >= 0:
                    y = y + 1
                    e = e - 2 * dx
        elif -1 <= k < 0:
            if x0 < x1:
                e = x0 - x1
                dx = x1 - x0
                dy = y1 - y0
                x = x0
                y = y0
            else:
                e = x1 - x0
                dx = x0 - x1
                dy = y0 - y1
                x = x1
                y = y1
            for i in range(int(dx)):
                cv.create_line(int(x), int(y), int(x + 1), int(y + 1), fill=color)
                x = x + 1
                e = e - 2 * dy
                if e >= 0:
                    y = y - 1
                    e = e - 2 * dx
        elif k > 1:
            if y0 < y1:
                e = y0 - y1
                dx = x1 - x0
                dy = y1 - y0
                x = x0
                y = y0
            else:
                e = x1 - x0
                dx = x0 - x1
                dy = y0 - y1
                x = x1
                y = y1
            for i in range(int(dy)):
                cv.create_line(int(x), int(y), int(x + 1), int(y + 1), fill=color)
                y = y + 1
                e = e + 2 * dx
                if e >= 0:
                    x = x + 1
                    e = e - 2 * dy
        else:
            if y0 < y1:
                e = y0 - y1
                dx = x1 - x0
                dy = y1 - y0
                x = x0
                y = y0
            else:
                e = x1 - x0
                dx = x0 - x1
                dy = y0 - y1
                x = x1
                y = y1
            for i in range(int(dy)):
                cv.create_line(int(x), int(y), int(x + 1), int(y + 1), fill=color)
                y = y + 1
                e = e - 2 * dx
                if e >= 0:
                    x = x - 1
                    e = e - 2 * dy


def encode(x: int, y: int, x_min: int, y_min: int, x_max: int, y_max: int) -> int:
    c = 0
    if x < x_min:
        c |= 1
    if x > x_max:
        c |= 2
    if y < y_min:
        c |= 4
    if y > y_max:
        c |= 8
    return c


def Cohen_Sutherland(x0: int, y0: int, x1: int, y1: int, color):
    x_min = min(x0, x1)
    x_max = max(x0, x1)
    y_min = min(y0, y1)
    y_max = max(y0, y1)
    interBresenham(x_min, y_min, x_min, y_max, color)
    interBresenham(x_max, y_min, x_max, y_max, color)
    interBresenham(x_min, y_min, x_max, y_min, color)
    interBresenham(x_min, y_max, x_max, y_max, color)
    print(line)
    for point in line:
        x_1 = point[0][0]
        y_1 = point[0][1]
        x_2 = point[1][0]
        y_2 = point[1][1]
        code1 = encode(x_1, y_1, x_min, y_min, x_max, y_max)
        code2 = encode(x_2, y_2, x_min, y_min, x_max, y_max)
        flag = False
        while code1 != 0 or code2 != 0:
            if code1 & code2 != 0:
                flag = True
                break
            code = code1
            if code == 0:
                code = code2
            if 1 & code != 0:
                x = x_min
                y = y_1 + (y_2 - y_1) * (x_min - x_1) / (x_2 - x_1)
            elif 2 & code != 0:
                x = x_max
                y = y_1 + (y_2 - y_1) * (x_max - x_1) / (x_2 - x_1)
            elif 4 & code != 0:
                y = y_min
                x = x_1 + (x_2 - x_1) * (y_min - y_1) / (y_2 - y_1)
            elif 8 & code != 0:
                y = y_max
                x = x_1 + (x_2 - x_1) * (y_max - y_1) / (y_2 - y_1)
            if code == code1:
                x_1 = x
                y_1 = y
                code1 = encode(x, y, x_min, y_min, x_max, y_max)
            else:
                x_2 = x
                y_2 = y
                code2 = encode(x, y, x_min, y_min, x_max, y_max)
        if flag:
            continue
        interBresenham(x_1, y_1, x_2, y_2, "red")


def cross(x1, y1, x2, y2, x3, y3):  # 跨立实验
    """
    x1,y1,x2,y2是同一线段
    x3,y3是另一线段的一个断点
    """
    x_1 = x2 - x1
    y_1 = y2 - y1
    x_2 = x3 - x1
    y_2 = y3 - y1
    return x_1 * y_2 - x_2 * y_1


def IsIntersec(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    :return: bool  判断两条线段是否相交
    """
    # 快速排斥，以l1、l2为对角线的矩形必相交，否则两线段不相交
    if (max(x1, x2) >= min(x3, x4)  # 矩形1最右端大于矩形2最左端
            and max(x3, x4) >= min(x1, x2)  # 矩形2最右端大于矩形最左端
            and max(y1, y2) >= min(y3, y4)  # 矩形1最高端大于矩形最低端
            and max(y3, y4) >= min(y1, y2)):  # 矩形2最高端大于矩形最低端

        # 若通过快速排斥则进行跨立实验
        if (cross(x1, y1, x2, y2, x3, y3) * cross(x1, y1, x2, y2, x4, y4) <= 0
                and cross(x3, y3, x4, y4, x1, y1) * cross(x3, y3, x4, y4, x2, y2) <= 0):
            D = 1
        else:
            D = 0
    else:
        D = 0
    return D


def findIntersection(x1, y1, x2, y2, x3, y3, x4, y4) -> list:
    """
    :return: 两线段的交点
    """
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
            (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
            (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    return [px, py]


def get_series(a: list, b: list) -> [list, list]:
    """
    :param a: 被裁剪的多边形
    :param b: 用于裁剪的多边形窗口
    :return: 插入交点的被裁减多边形序列与插入交点的裁剪多边形窗口的顶点序列
    """
    result_a = list()
    result_b = list()
    # 构建用于存放新增交点的被裁减多边形
    print("被裁剪多边形的顶点个数为：" + str(len(a)))
    print("裁剪多边形的顶点个数为：" + str(len(b)))
    for i in range(len(a) - 1):
        result_a.append([a[i], a[i + 1]])
    # 将最后一个点与第一个点构成的边放入
    result_a.append([a[len(a) - 1], a[0]])
    tmp_a = copy.deepcopy(result_a)
    print(result_a)
    # 构建用于存放新增交点的裁剪多边形窗口
    for i in range(len(b) - 1):
        result_b.append([b[i], b[i + 1]])
    # 将最后一个点与第一个点构成的边放入
    result_b.append([b[len(b) - 1], b[0]])
    tmp_b = copy.deepcopy(result_b)
    print(result_b)
    # 对每条边进行裁剪
    print("开始对每条边求交")
    for i in range(len(tmp_a)):
        point1 = tmp_a[i][0]
        point2 = tmp_a[i][1]
        for j in range(len(tmp_b)):
            point3 = tmp_b[j][0]
            point4 = tmp_b[j][1]
            # 判断两条边之间是否有交点
            if IsIntersec(point1[0], point1[1], point2[0], point2[1], point3[0], point3[1], point4[0], point4[1]):
                # 求两边交点
                sec_point = findIntersection(point1[0], point1[1], point2[0], point2[1], point3[0], point3[1],
                                             point4[0], point4[1])
                # 插入结果数组
                sec_point.append(0)
                result_a[i].insert(-1, sec_point)
                result_b[j].insert(-1, sec_point)
    # 对每条边中的点的结果进行标注，判断是入点还是出点，入点为0，出点为1
    print("求交完成")
    print(result_a)
    print(result_b)
    for i in result_a:
        if i[0][0] < i[-1][0]:
            i.sort(key=lambda x: x[0])
        else:
            i.sort(key=lambda x: x[0], reverse=True)
    for i in result_b:
        if i[0][0] < i[-1][0]:
            i.sort(key=lambda x: x[0])
        else:
            i.sort(key=lambda x: x[0], reverse=True)
    print("还原为点表示")
    result_point_a = list()
    for i in result_a:
        for j in range(len(i) - 1):
            result_point_a.append(i[j])
    result_point_b = list()
    for i in result_b:
        for j in range(len(i) - 1):
            result_point_b.append(i[j])
    result_a = copy.deepcopy(result_point_a)
    result_b = copy.deepcopy(result_point_b)
    print(result_a)
    print(result_b)
    # 对入点和出点标记
    print("对入点和出点进行标注")
    cnt_a = -1
    cnt_b = -1
    # 找到A中的第一个入点
    for i in range(len(result_a)):
        if len(result_a[i]) == 3:
            cnt_a = i
            print("找到了被裁剪多边形的第一个入点：")
            print(cnt_a)
            print(result_a[cnt_a])
            break
    # 对A中的点进行标记
    cnt = (cnt_a + 1) % len(result_a)
    flag = False
    result_a[cnt_a][2] = 0
    while cnt != cnt_a:
        print(cnt)
        if len(result_a[cnt]) == 3:
            print("找到了一个交点：")
            print(result_a[cnt])
            if flag:
                result_a[cnt][2] = 0
                flag = False
            else:
                result_a[cnt][2] = 1
                flag = True
        cnt = (cnt + 1) % len(result_a)
    # 利用A中的交点的标记，对B中的点进行标记
    for i in result_a:
        if len(i) == 3:
            for j in range(len(result_b)):
                if len(result_b[j]) == 3 and result_b[j][0] == i[0] and result_b[j][1] == i[1]:
                    result_b[j][2] = i[2]
    for j in range(len(result_a)):
        result_a[j][0] = int(result_a[j][0])
        result_a[j][1] = int(result_a[j][1])
    for j in range(len(result_b)):
        result_b[j][0] = int(result_b[j][0])
        result_b[j][1] = int(result_b[j][1])
    return result_a, result_b


def clip(a: list, b: list) -> list:
    """
    :param a: 被裁剪多边形顶点序列
    :param b: 裁剪多边形顶点序列
    :return: 裁剪结果的顶点序列
    """
    a_series, b_series = get_series(a, b)

    print(a_series)
    print(b_series)
    print("完成点表示，开始裁剪")

    output = list()
    # 用于判断顶点序列中是否有入点
    flag = True
    while flag:
        flag = False
        q = list()
        cnt = -1
        # 寻找入点
        for i in range(len(a_series)):
            if len(a_series[i]) == 3:
                if a_series[i][2] == 0:
                    flag = True
                    cnt = i
                    # 将入点暂时缓存到tmp_point中
                    tmp_point = copy.deepcopy(a_series[i])
                    # 将入点标记删去
                    a_series[cnt].pop()
                    break
        flag1 = False
        if flag:
            # 用于判断是否经历了一个闭环
            while not flag1:
                # 沿着A数组顺序取出顶点，当顶点不是出点，将顶点录入到数组q中
                while len(a_series[cnt]) != 3 or len(a_series[cnt]) == 3 and a_series[cnt][2] != 1:
                    q.append(a_series[cnt])
                    cnt += 1
                    cnt = cnt % len(a_series)
                # 寻找B中相对应的点
                cnt_b = 0
                while b_series[cnt_b][0] != a_series[cnt][0] and b_series[cnt_b][1] != a_series[cnt][1]:
                    cnt_b += 1
                # 沿着B数组顺序寻找，若顶点不是入点，将顶点录入到q中
                while len(b_series[cnt_b]) != 3 or len(b_series[cnt_b]) == 3 and b_series[cnt_b][2] != 0:
                    q.append(b_series[cnt_b])
                    cnt_b += 1
                    cnt_b = cnt_b % len(b_series)
                # 判断顶点是否等于tmp_point，若不是，则继续追踪A数组，否则将数组q保存
                if b_series[cnt_b][0] == tmp_point[0] and b_series[cnt_b][1] == tmp_point[1]:
                    # 形成了闭环
                    print("找到一个闭环")
                    print(q)
                    print(a_series)
                    print(b_series)
                    flag1 = True
                    output.append(copy.deepcopy(q))
                else:
                    # 在被裁剪多边形中找到相对应的点
                    cnt = 0
                    while a_series[cnt][0] != b_series[cnt_b][0] or a_series[cnt][1] != b_series[cnt_b][1]:
                        cnt += 1
                        cnt = cnt % len(a_series)
                    # 将入点标记去掉
                    if len(a_series[cnt])==3 and a_series[cnt][2]==0:
                        a_series[cnt].pop()
                    print("没有找到闭环")
                    print(a_series[cnt])
                    print(q)
                    print(a_series)
                    print(b_series)
                    #time.sleep(10)
    for i in output:
        for j in range(len(i)):
            i[j][0] = int(i[j][0])
            i[j][1] = int(i[j][1])
    print(output)
    return output


# 扫描线填充算法
def scanline_fill(points1: list, color):
    scan_points = copy.deepcopy(points1)
    y_max = -1
    y_min = 1000
    # find y_max
    for i in range(len(scan_points)):
        if y_max < scan_points[i][1]:
            y_max = scan_points[i][1]
            # max_index=i
        if y_min > scan_points[i][1]:
            y_min = scan_points[i][1]
            # min_index=i
    # set the y_min=0
    begin_y = y_min
    interval = y_max - y_min
    for i in scan_points:
        i[1] = i[1] - y_min
    # initialize net
    net = [[] for i in range(interval + 1)]
    for i in range(len(scan_points)):
        point1 = scan_points[i]
        point2 = scan_points[(i + 1) % len(scan_points)]
        if point1[1] < point2[1]:
            max_point = point2
            min_point = point1
        else:
            max_point = point1
            min_point = point2
        if max_point[0] == min_point[0]:
            k = 0
        elif max_point[1] == min_point[1]:
            continue
        else:
            k = (max_point[0] - min_point[0]) / (max_point[1] - min_point[1])
        edge = [max_point[0], k, min_point[1]]
        net[max_point[1]].append(edge)
    # sort net
    for i in net:
        if len(i) > 1:
            i.sort(key=operator.itemgetter(0, 1))
    # initialize aet
    aet = [[] for i in range(interval + 1)]
    for i in range(interval, -1, -1):
        if len(net[i]) > 0:
            for j in net[i]:
                # if the point above the scanline add the point
                if j[2] < i:
                    aet[i].append(j)
        if i < interval:
            for j in aet[i + 1]:
                if j[2] < i:
                    aet[i].append([j[0] - j[1], j[1], j[2]])
    # sort aet
    for i in aet:
        if len(i) > 0:
            i.sort(key=operator.itemgetter(0, 1))
    for i in range(interval + 1):
        for j in range(0, len(aet[i]), 2):

            x_begin = int(aet[i][j][0])
            x_end = int(aet[i][j + 1][0])
            print(str(x_begin) + "   " + str(x_end))
            x = x_begin
            while x <= x_end:
                cv.create_line(int(x), int(begin_y + i), int(x + 1), int(begin_y + i + 1), fill=color)
                x += 1


# 获取左键鼠标的点坐标
def get_point(event):
    print(f"鼠标左键点击{event.x, event.y}")
    points.append([event.x, event.y])
    method = ddl.get()
    if method == "直线裁剪":
        if len(points) == 2:
            interBresenham(points[0][0], points[0][1], points[1][0], points[1][1], "black")
            line.append(copy.deepcopy(points))
            print(points)
            points.clear()
            print(line)


# 画出直线裁剪的窗口
def draw_window(event):
    print(f"鼠标右键点击{event.x, event.y}")
    window.append([event.x, event.y])
    method = ddl.get()
    if method == "直线裁剪":
        if len(window) == 2:
            Cohen_Sutherland(window[0][0], window[0][1], window[1][0], window[1][1], "black")
            window.clear()


def draw_pic(self):
    method = ddl.get()
    if method == "直线裁剪":
        if len(points) > 2:
            line.clear()
            line.append(copy.deepcopy(points))
            for i in range(len(points) - 1):
                interBresenham(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], "black")
            interBresenham(points[0][0], points[0][1], points[len(points) - 1][0], points[len(points) - 1][1], "black")
            points.clear()
    # 画出被裁剪多边形
    elif method == "多边形裁剪":
        if len(points) > 2:
            line.clear()
            line.append(copy.deepcopy(points))
            for i in range(len(points) - 1):
                interBresenham(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], "black")
            interBresenham(points[0][0], points[0][1], points[len(points) - 1][0], points[len(points) - 1][1], "black")


# 画出裁剪多边形
def draw_polygon_window(self):
    if len(window) > 2:
        for i in range(len(window) - 1):
            interBresenham(window[i][0], window[i][1], window[i + 1][0], window[i + 1][1], "red")
        interBresenham(window[0][0], window[0][1], window[len(window) - 1][0], window[len(window) - 1][1], "red")


# 进行裁剪图形的绘制
def clip_polygon(self):
    a = copy.deepcopy(points)
    points.clear()
    b = copy.deepcopy(window)
    window.clear()
    result = clip(a, b)
    for i in result:
        scanline_fill(i, "blue")


tk.bind("<Return>", draw_pic)
tk.bind("c", clip_polygon)
tk.bind("d", draw_polygon_window)
cv.bind("<Button-1>", get_point)  # 给按钮控件绑定左键单击事件
cv.bind("<Button-3>", draw_window)  # 给按钮控件绑定右键单击事件
cv.pack(fill='both', expand=True)
mainloop()
