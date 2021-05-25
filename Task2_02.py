import requests
import math
import scipy.special
import numpy as np
from scipy.special import spherical_jn, spherical_yn
import matplotlib.pyplot as plt
import requests as rqst
import csv

# Рассчитать ЭПР
# Построить график
# Сохранить результаты в файл

# Radar cross section
def RCS(lam, r):
    summ = 0
    kr = 2 * math.pi * r / lam
    # Задаем значения функций Бесселя для n = 0 для первой итерации
    J_prev = spherical_jn (0, kr)
    Y_prev = spherical_yn (0, kr)
    H_prev = J_prev + 1j * Y_prev
    for n in range(1, 50):
        # Вычисляем значения функций Бесселя для текущей n
        J_now = spherical_jn (n, kr)
        #J_prev = spherical_jn (n - 1, kr)
        Y_now = spherical_yn (n, kr)
        #Y_prev = spherical_yn (n - 1, kr)
        H_now = J_now + 1j * Y_now
        #H_prev = J_prev + 1j * Y_prev
        # Считаем коэффициенты a и b
        a = J_now / H_now
        b = (kr * J_prev - n * J_now) / (kr * H_prev - n * H_now)
        summ += ((-1) ** n) * (n + 0.5) * (b - a)
        # Переносим значения функций Бесселя на следующий шаг
        J_prev = J_now
        Y_prev = Y_now
        H_prev = H_now
    return lam * lam * np.abs(summ) * np.abs(summ) / math.pi

def graf(lam, p):
  plt.plot(lam, p)
  plt.ylabel('RCS')
  plt.xlabel('lambda')
  plt.grid()
  plt.show()

def graf_freq(f, p):
  plt.plot(f, p)
  plt.ylabel('RCS, [м^2]')
  plt.xlabel('freq, [Гц]')
  plt.grid()
  plt.show()

# Скачать файл с вариантом задания 

def download(url):
  r=rqst.get(url)
  return r.text


# Возврат данных по номеру варианта
def var(text,nomervar):
  t=text.splitlines()
  return t[nomervar]

# Запись в csv-файл
def to_csv(ls, s):
    data = [['№', 'f, Гц', 'RCS, m2']]
    for i in range(len(ls)):
        data.append([i, ls[i],  s[i]])
    with open('task_02.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
  
if __name__ == '__main__':
    txt = download('https://jenyay.net/uploads/Student/Modelling/task_02_02.txt')
    print(txt)
    nomervar = 6
    line = " ".join(var(txt,nomervar).split())
    L = list(line.split(' '))
    D = float(L[1])
    fmin = float(L[2])
    fmax = float(L[3])
    s=[]
    ls=np.linspace(fmin,fmax,300)
    for f in ls:
        p=RCS(3e8 / f, D/2)
        s.append(p)
    
    graf_freq(ls,s)
    to_csv(ls, s)
