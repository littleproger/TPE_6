from numpy.linalg import solve
from math import fabs
from math import sqrt
from scipy.stats import f, t
from random import randrange


def cohren(f1, f2, q=0.05):
    q1 = q / f1
    cohren1 = f.ppf(q=1 - q1, dfn=f2, dfd=(f1 - 1) * f2)
    return round(cohren1/ (cohren1 + f1 - 1),4)

def fisher(f1, f2, q=1 - 0.05):
    fisher1 = f.ppf(q, dfn=f2, dfd=f1)
    return round(fisher1, 4)

def student(f3, q=1 - 0.025):
    student1 = t.ppf(q, df=f3)
    return round(student1, 4)



def x(l1, l2, l3):
    x_1 = l1 * delta_x1 + x01
    x_2 = l2 * delta_x2 + x02
    x_3 = l3 * delta_x3 + x03
    return [x_1, x_2, x_3]


def generate_y():
    def create_y(x1,x2,x3):
        y = 8.6 + 6.5 * x1 + 9.5 * x2 + 4.2 * x3 + 8 * x1 * x1 + 0.5 * x2 * x2 + 2.3 * x3 * x3 + 0.6 * x1 * x2 + \
            0.2 * x1 * x3 + 5.9 * x2 * x3 + 3.9 * x1 * x2 * x3 + randrange(0, 10) - 5
        return y

    matrix = [[create_y(matrix_x[j][0], matrix_x[j][1], matrix_x[j][2]) for i in range(m)] for j in range(N)]
    return matrix


def find_ser(lst, flag):
    ser = []
    if flag == 1:
        for i in range(len(lst)):
            ser.append(sum(lst[i]) / len(lst[i]))
    else:
        for k in range(len(lst[0])):
            number_lst = []
            for i in range(len(lst)):
                number_lst.append(lst[i][k])
            ser.append(sum(number_lst) / len(number_lst))
    return ser


def a(first, second):
    a = 0
    for j in range(N):
        a += matrix_x[j][first - 1] * matrix_x[j][second - 1] / N
    return a


def find_right(number):
    need_a = 0
    for j in range(N):
        need_a += ser_y[j] * matrix_x[j][number - 1] / 15
    return need_a


def result(b_list, k):
    y = b_list[0] + b_list[1] * matrix[k][0] + b_list[2] * matrix[k][1] + b_list[3] * matrix[k][2] + \
        b_list[4] * matrix[k][3] + b_list[5] * matrix[k][4] + b_list[6] * matrix[k][5] + b_list[7] * matrix[k][6] +\
        b_list[8] * matrix[k][7] + b_list[9] * matrix[k][8] + b_list[10] * matrix[k][9]
    return y


def student_test(b_list, number_x=10):
    dispersion_b = sqrt(dispersion_b2)
    for k in range(number_x):
        t_practice = 0
        t_theoretical = student(f3, q)
        for i in range(N):
            t_practice += ser_y[i] * matrix_norm[i][k]
        if fabs(t_practice / dispersion_b) < t_theoretical:
            b_list[k] = 0
    return b_list
# Тут не потрібна була перевірка

def fisher_test():
    dispersion = 0
    f4 = N - d
    for i in range(len(ser_y)):
        dispersion += (m * (ser_y[i] - result(student_list, i))) / (N - d)
    F_practice = dispersion / dispersion_b2
    F_theoretical = fisher(f3, f4, q)
    return F_practice < F_theoretical

def printer(koef):
    print("y = {:.3f} + {:.3f} * x1 + {:.3f} * x2 + {:.3f} *x3 + {:.3f} * x1*x2 + {:.3f} * x1*x3 + {:.3f} * x2*x3 +"
          " {:.3f} * x1*x2*x3 + {:.3f} * x11^2 + {:.3f} * x22^2 + {:.3f} * x33^2 \n"
          .format(koef[0], koef[1], koef[2], koef[3], koef[4], koef[5], koef[6], koef[7], koef[8], koef[9], koef[10]))
    print('Перевірка:')
    for i in range(N):
        print("y{} = {:.3f} {:>20} y{} = {:.3f}".format((i + 1), result(koef, i), "Теоритичне", (i + 1), ser_y[i]))


m, d = 3, 0
N = 15
p = 0.95

x1_min = -25
x1_max = -5
x2_min= -30
x2_max =45
x3_min = -5
x3_max = 5
x01 = (x1_max + x1_min) / 2
x02 = (x2_max + x2_min) / 2
x03 = (x3_max + x3_min) / 2
delta_x1 = x1_max - x01
delta_x2 = x2_max - x02
delta_x3 = x3_max - x03
y_min = 200 + int((x1_min + x2_min + x3_min) / 3)
y_max = 200 + int((x1_max + x2_max + x3_max) / 3)

matrix_norm = [
    [-1, -1, -1, +1, +1, +1, -1, +1, +1, +1],
    [-1, -1, +1, +1, -1, -1, +1, +1, +1, +1],
    [-1, +1, -1, -1, +1, -1, +1, +1, +1, +1],
    [-1, +1, +1, -1, -1, +1, -1, +1, +1, +1],
    [+1, -1, -1, -1, -1, +1, +1, +1, +1, +1],
    [+1, -1, +1, -1, +1, -1, -1, +1, +1, +1],
    [+1, +1, -1, +1, -1, -1, -1, +1, +1, +1],
    [+1, +1, +1, +1, +1, +1, +1, +1, +1, +1],
    [-1.73, 0, 0, 0, 0, 0, 0, 2.9929, 0, 0],
    [+1.73, 0, 0, 0, 0, 0, 0, 2.9929, 0, 0],
    [0, -1.73, 0, 0, 0, 0, 0, 0, 2.9929, 0],
    [0, +1.73, 0, 0, 0, 0, 0, 0, 2.9929, 0],
    [0, 0, -1.73, 0, 0, 0, 0, 0, 0, 2.9929],
    [0, 0, +1.73, 0, 0, 0, 0, 0, 0, 2.9929],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

matrix_x = [[] for x in range(N)]
for i in range(len(matrix_x)):
    if i < 8:
        x1 = x1_min if matrix_norm[i][0] == -1 else x1_max
        x2 = x2_min if matrix_norm[i][1] == -1 else x2_max
        x3 = x3_min if matrix_norm[i][2] == -1 else x3_max
    else:
        x_lst = x(matrix_norm[i][0], matrix_norm[i][1], matrix_norm[i][2])
        x1, x2, x3 = x_lst
    matrix_x[i] = [x1, x2, x3, x1 * x2, x1 * x3, x2 * x3, x1 * x2 * x3, x1 ** 2, x2 ** 2, x3 ** 2]

matrix_y = generate_y()
ser_x = find_ser(matrix_x, 0)
ser_y = find_ser(matrix_y, 1)
matrix = [(matrix_x[i] + matrix_y[i]) for i in range(N)]
mx_i = ser_x
my = sum(ser_y) / 15

left = [
    [1, mx_i[0], mx_i[1], mx_i[2], mx_i[3], mx_i[4], mx_i[5], mx_i[6], mx_i[7], mx_i[8], mx_i[9]],
    [mx_i[0], a(1, 1), a(1, 2), a(1, 3), a(1, 4), a(1, 5), a(1, 6), a(1, 7), a(1, 8), a(1, 9), a(1, 10)],
    [mx_i[1], a(2, 1), a(2, 2), a(2, 3), a(2, 4), a(2, 5), a(2, 6), a(2, 7), a(2, 8), a(2, 9), a(2, 10)],
    [mx_i[2], a(3, 1), a(3, 2), a(3, 3), a(3, 4), a(3, 5), a(3, 6), a(3, 7), a(3, 8), a(3, 9), a(3, 10)],
    [mx_i[3], a(4, 1), a(4, 2), a(4, 3), a(4, 4), a(4, 5), a(4, 6), a(4, 7), a(4, 8), a(4, 9), a(4, 10)],
    [mx_i[4], a(5, 1), a(5, 2), a(5, 3), a(5, 4), a(5, 5), a(5, 6), a(5, 7), a(5, 8), a(5, 9), a(5, 10)],
    [mx_i[5], a(6, 1), a(6, 2), a(6, 3), a(6, 4), a(6, 5), a(6, 6), a(6, 7), a(6, 8), a(6, 9), a(6, 10)],
    [mx_i[6], a(7, 1), a(7, 2), a(7, 3), a(7, 4), a(7, 5), a(7, 6), a(7, 7), a(7, 8), a(7, 9), a(7, 10)],
    [mx_i[7], a(8, 1), a(8, 2), a(8, 3), a(8, 4), a(8, 5), a(8, 6), a(8, 7), a(8, 8), a(8, 9), a(8, 10)],
    [mx_i[8], a(9, 1), a(9, 2), a(9, 3), a(9, 4), a(9, 5), a(9, 6), a(9, 7), a(9, 8), a(9, 9), a(9, 10)],
    [mx_i[9], a(10, 1), a(10, 2), a(10, 3), a(10, 4), a(10, 5), a(10, 6), a(10, 7), a(10, 8), a(10, 9), a(10, 10)]
]
right = [my, find_right(1), find_right(2), find_right(3), find_right(4), find_right(5), find_right(6), find_right(7),
         find_right(8), find_right(9), find_right(10)]

beta = solve(left, right)

# right і left це матриці, які потрбні для того аби знайти beta - масив з коефіцієнтів рівняння регресії

print("\n{:>25}{:>5} \n{:>19}{:>5}{:>5} \n{:>5}{:>7}{:>5}{:>5}{:>160} \n{:>19}{:>5}{:>5}"
      .format("min","max","x1:",x1_min,x1_max,"Варіант: 110","x2:",x2_min,x2_max,
              "f=8.6 + 6.5 * x1 + 9.5 * x2 + 4.2 * x3 + 8 * x1 * x1 + 0.5 * x2 * x2 + 2.3 * x3 * x3 +"
              " 0.6 * x1 * x2 + 0.2 * x1 * x3 + 5.9 * x2 * x3 + 3.9 * x1 * x2 * x3","x3:",x3_min,x3_max))

print("\nРівняння регресії з квадратичними членами:")
printer(beta)

cohrenFlag = False
while not cohrenFlag:
    print("\n{:>100}\n".format("Матриця планування експерименту"))
    print("{:>8} {:>12} {:>12} {:>13} {:>12} {:>12} {:>13} {:>12} {:>11} {:>11} {:>11} {:>11} {:>11}"
          .format("x1","x2","x3","x1x2","x1x3","x2x3","x1x2x3","x1x1","x2x2","x3x3","y1","y2","y3"))
    for i in range(N):
        print("\n", end=' ')
        for k in range(len(matrix[0])):
            print("{:^12.3f}".format(matrix[i][k]), end=' ')

    dispersion_y = [0.0 for x in range(N)]
    for i in range(N):
        dispersion_i = 0
        for j in range(m):
            dispersion_i += (matrix_y[i][j] - ser_y[i]) ** 2
        dispersion_y.append(dispersion_i / (m - 1))
    f1 = m - 1
    f2 = N
    f3 = f1 * f2
    q = 1 - p
    Gp = max(dispersion_y) / sum(dispersion_y)

    print("\n\nКритерій Кохрена:")
    Gt = cohren(f2, f1, q)
    if Gt > Gp or m >= 25:
        print("Дисперсія однорідна при рівні значимості {:.2f}\n".format(q))
        cohrenFlag = True
    else:
        print("Дисперсія не однорідна при рівні значимості {:.2f}\n".format(q))
        m += 1
    if m == 25:
        exit()

dispersion_b2 = sum(dispersion_y) / (N * N * m)
student_list = list(student_test(beta))
print("Отримане рівняння регресії з критерієм Стьюдента:")
printer(student_list)


print("\nКритерій Фішера:")
d = 11 - student_list.count(0)
if fisher_test():
    print("Рівняння регресії адекватне оригіналу.")
else:
    print("Рівняння регресії неадекватне оригіналу.")