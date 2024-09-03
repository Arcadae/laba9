"""
Требуется написать объектно-ориентированную программу с графическим интерфейсом в соответствии со своим вариантом.
В программе должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных использовать нельзя. При необходимости сохранять информацию в виде файлов, разделяя значения запятыми или пробелами.
Для GUI использовать библиотеку tkinter.

Вариант 20: Объекты – торговые сделки
Функции:	сегментация полного списка сделок по видам товаров
            визуализация предыдущей функции в форме круговой диаграммы
            сегментация полного списка договоров по продавцам
            визуализация предыдущей функции в форме круговой диаграммы
"""

import tkinter as tk
import os
import re
import matplotlib.pyplot as plt
from itertools import groupby
from tkinter import filedialog


class Trade:
    """
    Класс сделки
    """
    def __init__(self,name:str,data:str,trader_name:str,trade_price:int,
                 item_type:str) -> None:
        self.name = name
        self.data = data
        self.trader_name = trader_name
        self.trade_price = trade_price
        self.item_type = item_type

    def __repr__(self) -> str:
        return f'{self.__dict__}'

class TradeList:
    """
    Класс списка сделок
    """
    def __init__(self) -> None:
        self.trades = []

    def add_trade(self,trade) -> None:
        self.trades.append(trade)

    def segmentation_by_type(self) -> None:
        output_text.delete(1.0, 'end')
        grouped:list = groupby([trade.item_type for trade in sorted(self.trades, key = lambda trade: trade.item_type)])
        for key, group in grouped:
            lng:int = len(list(group))
            output_text.insert('end',f'{key}:{lng}\n')


    def visualization_type_segmentation(self) -> None:
        grouped: list = groupby([trade.item_type for trade in sorted(self.trades, key=lambda trade: trade.item_type)])
        labels, sizes = [], []
        for key, group in grouped:
            lng: int = len(list(group))
            labels.append(key), sizes.append(lng)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels = labels, autopct = '%1.1f%%', shadow = True,
                startangle = 90)
        ax1.axis('equal')
        plt.show()

    def segmentation_by_trader_name(self) -> None:
        output_text.delete(1.0, 'end')
        grouped:list = groupby([trade.trader_name for trade in sorted(self.trades, key = lambda trade: trade.trader_name)])
        for key, group in grouped:
            lng:int = len(list(group))
            output_text.insert('end',f'{key}:{lng}\n')

    def visualization_name_segmentation(self) -> None:
        grouped: list = groupby(
            [trade.trader_name for trade in sorted(self.trades, key=lambda trade: trade.trader_name)])
        labels, sizes = [], []
        for key, group in grouped:
            lng: int = len(list(group))
            labels.append(key), sizes.append(lng)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels = labels, autopct = '%1.1f%%', shadow = True,
                startangle = 90)
        ax1.axis('equal')
        plt.show()

    def __repr__(self) -> str:
        return f'{self.__dict__}'

def compilation() -> list:
    global file
    file = filedialog.askopenfilename()

    global trade_list
    trade_list = TradeList()

    count: int = 0
    for inf in file_reader(file):
        count += 1
        trade_list.add_trade(Trade(f'trade_{count}', inf[0],
                                   inf[1], int(inf[2]), inf[3]))
    return trade_list


pattern: str = (r'((0?[1-9]|1?[0-9]|2?[0-9]|3?[0-1])\.(0?[1-9]|1?[1-2])\.(\d{4})):'
                r'([А-Я]{1}[а-я]+ [А-Я]{1}[а-я]+):(\d+):([А-Я]{1}[а-я]+)')
def file_reader(file) -> None:
    if os.stat(file).st_size == 0: raise SystemExit('Ваш файл пуст')
    try:
        with open(file,'r',encoding = 'utf-8') as file:
            yield from (tuple(line.strip().split(':')) for line in file if re.fullmatch(pattern, line.strip()) != None)
    except FileNotFoundError:
        print(f'Ваш файл не найден')

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Окно')
    root.geometry('500x500+700+250')

    tk.Button(root, text = 'Открыть файл', command = compilation).pack(fill='x')
    trade_list = compilation()

    tk.Label(root, text = f'Ваш файл: {file} ').pack()

    tk.Label(root, text='-Вам доступны следующие функции-', font = ('Arial', 14)).pack(fill= 'x', pady = 10)

    tk.Button(root, text = 'Визуализация сегментации по типу товара', font = ('Arial',12), command = trade_list.visualization_type_segmentation).pack(pady = 5)
    tk.Button(root, text = 'Визуализация сегментации по имени продавца', font = ('Arial',12), command = trade_list.visualization_name_segmentation).pack(pady = 5)
    tk.Button(root, text = 'Сегментация по типу товара', font = ('Arial',12), command = trade_list.segmentation_by_type).pack(pady = 5)
    tk.Button(root, text = 'Сегментация по имени продавца', font = ('Arial',12), command = trade_list.segmentation_by_trader_name).pack(pady = 5)

    output_text = tk.Text(root, wrap='word', height=10)
    output_text.pack(fill='both', expand=True)

    root.mainloop()