# Запись АЧХ, ФЧХ узла
'''
Программа выполняет запись АЧХ и ФЧХ узла с FSH4 в таблицу Excel.
'''
# v0.02
'''
Исправление считывания маркеров
'''
# v0.01
'''
1 ЗАПРОС: Требуется ли загрузка настроек с прибора?

1.1 True:
    Проверка наличия директории и А0160.dataset на приборе
    1.1.1 True:
        ВЫВОД: Загрузка device.dataset выполнена.
        Нажмите enter.
        Переход к 2 Выполнение измерений
    1.1.2 False:
        Запрос: A0160.dataset в FSH4 отсутсвует. Выполните калибровку прибора.
        По завершению калибровки нажмите enter.
        в FSH4 сохранен A0160.dataset.
        Переход к 2 Выполнение измерений
1.2 False:
    Переход к 2 Выполнение измерений


2 Выполнение измерений
2.1 Запрос: Наименование документа Excel
2.2 Запрос в цикле: Плата. Значение 0 для завершения цикла
2.3 Сохранение информации в Excel

2.4 Ввод стандартных маркеров
!!! Список частот маркеров формируется неверно

3 Шаблон ecxel:
Лист 1 - Сводная таблица АЧХ и ФЧХ
Лист 2 - АЧХ по маркерам
Лист 3 - все АЧХ
Лист 4 - все ФЧХ
'''


def preset_fsh():
    fsh.write('inst nan; *wai')
    fsh.write('*rst; *wai')
    fsh.write('meas:mode vect')
    fsh.write('meas:func:sel s12')
    fsh.write_int('swe:coun', 10)
    fsh.write_float('freq:star', 1e6)
    fsh.write_float('freq:stop', 31e6)
    fsh.write_int('band', 1e3)
    fsh.write('meas:form mph')
    fsh.write_float('disp1:magn:ref:pos', 5.0)
    fsh.write_float('disp1:magn:ref', -0.50)
    fsh.write_float('disp1:magn:y:scal', 5.00)
    fsh.write_float('disp2:phas:ref:pos', 0.5)
    fsh.write_float('disp2:phas:ref', -9.00)
    fsh.write_bool('disp2:phas:unwr', True)
    fsh.write_int('disp2:phas:y:scal', 90)
    fsh.write('calc:mark:aoff')
    fsh.write_float('calc:mark1:x', 1.5e6)
    fsh.write_float('calc:mark2:x', 10e6)
    fsh.write_float('calc:mark3:x', 20e6)
    fsh.write_float('calc:mark4:x', 30e6)
    fsh.write('*wai')


def load_setup():
    path_set = '\\Public\\User'
    file_set = f'{name_set}.set'
    fsh.write('mmem:cdir "\\Public"')

    if 'User' not in fsh.query('mmem:cat:dir?').split(','):
        fsh.write(f'mmem:mdir "{path_set}"')
        print(f'Создана директория {instr_info}{path_set}')
    fsh.write(f'mmem:cdir "{path_set}"')
    print(f'Выполнен вход в {instr_info}{path_set}')

    if fsh.file_exists(file_set):
        fsh.write(f'mmem:load:stat 1, "{file_set}"')
        fsh.write('*wai')
        print(f'Выполнена настройка {instr_info}{path_set}\\{file_set}')
    else:
        print(f'Отсутствует настройка {instr_info}{path_set}\\{file_set}')
        preset_fsh()
        print('Выполнена предустановка по умолчанию.')
        input('Выполните калибровку. По завершению нажмите enter.')
        fsh.write(f'mmem:stor:stat 1, "{file_set}"')
        print(f'Сохранена настройка {instr_info}{path_set}\\{file_set}')

    input('\nНастройка завершена. Чтобы перейти к измерениям, нажмите enter.')
    fsh.write_float('disp1:magn:ref', 5.50)
    fsh.write_float('disp2:phas:ref', -201.00)


from RsInstrument import RsInstrument
from pprint import pprint

import numpy as np
import pandas as pd

import os

print()
print('Измерение АЧХ, ФЧХ узла. v0.02'.center(50, '.'))
print('Установки по умолчанию'.center(50, '.'))
print('''
ip-адрес FSH4: 20.20.215.200
Файл-dataset: FSH\\User\\device.set
Файл-отчет: ПК\\C:\\Измерения\<Файл_отчет>.xlsx
''')

# Подключаемся к прибору, проверяем

while True:
    try:
        fsh = RsInstrument('tcpip::20.20.215.200')
    except:
        input('Проверьте сетевой адрес FSH4 (enter)')
        continue
    break

instr_info = fsh.query('*idn?').split(',')[1]
print(f"{instr_info} подключен.\n")
fsh.clear_status()
fsh.write('inst nan; *wai')

# Калибруемся или начинаем измерять

name_set = 'device'
print(f'0     - Загрузка FSH\\User\\{name_set}.set')
question1 = input('enter - Начать измерения\n')
if question1 == '0':
    load_setup()

# Собираем список частот в рабочем диапазоне

freq_start = fsh.query_float('freq:star?')
freq_stop = fsh.query_float('freq:stop?')
points = fsh.query_int('swe:poin?')
freq_step = (freq_stop - freq_start) / (points - 1)
freq_list = [round((freq_start + freq_step * i) / 1e6, 3) for i in range(points)]
data = [freq_list]
head = ['Частота, МГц']

# Собираем список активных маркеров

marker_list = []
marker_data = [[]]
for i in range(1, 7):
    if fsh.query_bool(f'calc:mark{i}?'):
        marker_list.append(i)
        marker_data[0].append(round(fsh.query_float(f'calc:mark{i}:x?') / 1e+6, 3))

# Подготавливаем директорию для результатов

path_name = 'C:/'
folder_name = 'Измерения'
os.chdir(path_name)
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)
path_name += folder_name
os.chdir(path_name)

# Подготавливаем файл для результатов

while True:
    name = input('Название файла-отчета: ')
    if not name:
        print('Имя файла не может быть пустым')
        continue
    file_name = f'{name}.xlsx'
    file_path = f'{path_name}/{file_name}'
    if os.path.exists(file_path):
        print('Такой файл уже существует')
        continue
    break

# Начало цикла измерений

fsh.write('disp:trac1:mode aver')
fsh.write('disp:trac2:mode aver')
fsh.write_bool('init:cont', False)

print('\nЧтобы закончить измерения, введите 0')
name_index = input('Измерение №: ')
while name_index != '0':
    fsh.write('init; *wai')
    afc_list = fsh.query('trac? trace1').split(',')
    pfc_list = fsh.query('trac? trace2').split(',')
    afc_list = [round(float(afc_list[i]), 2) for i in range(points)]
    pfc_list = [round(float(pfc_list[i]), 2) for i in range(points)]
    data.append(afc_list)
    data.append(pfc_list)
    head.append(f'{name_index}, дБ')
    head.append(f'{name_index}, \u00b0')

    afc_marks = []
    for m in marker_list:
        afc_marks.append(fsh.query(f'calc1:mark{m}:y?').split(',')[0])
    marker_data.append(afc_marks)

    name_index = input('Измерение №: ')
fsh.write_bool('init:cont', True)

# Формирование таблиц для переноса

data = np.transpose(data).tolist()
marker_data = np.transpose(marker_data).tolist()

data_df = pd.DataFrame(data, columns=head)
afc_head = [head[0]] + head[1::2]
afc_df = data_df[afc_head]
pfc_head = [head[0]] + head[2::2]
pfc_df = data_df[pfc_head]

mark_df = pd.DataFrame(marker_data, columns=afc_head)

writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

data_df.to_excel(writer, sheet_name='АФЧХ')
afc_df.to_excel(writer, sheet_name='АЧХ')
pfc_df.to_excel(writer, sheet_name='ФЧХ')
mark_df.to_excel(writer, sheet_name='Маркеры')
writer.close()

print(f'\nИзмерения завершены, {file_path}')