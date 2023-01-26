# 1) Переходим в указанную директорию и извлекаем её имя - это и будет имя тонкой сборки.
# 2) Извлекаем из имени сборки её плотность +
# 3) Рекурсивно обходим содержимое папки извлекая все имена файлов
# 4) Из каждого файла извлекаем плотность макета +
# 5) Сравниваем плотность макета с плотностью сборки:
# ---- Если плотность макета меньше или равна плотности сборки - продолжаем (т.е. всё Ок).
# ---- Если выше - формируем список из таких имён (Не корректные файлы).
# 6) Выводим в консоль след. информацию:
# - полное имя сборки
# - плотность данной сборки
# - кол-во макетов в сборке "Всего n .pdf файлов в папке."
# - статус работы (один из предложенных ниже):
# ---- |. "Есть не опознанные имена файлов." - когда рег.выражение не смогло извлечь плотность макета.
# ----  Выводить их список, обязательно пронумерованным.
# ---- ||. "Присутствуют более плотные макеты." Выводить их список, обязательно пронумерованным.
# ---- |||. "Всё Ок".

import re
import os


def create_files_list(path: str) -> list:
    files_list = list()

    for dirpath, dirnames, filenames in os.walk(path):
        if filenames:
            files_list.extend(filenames)

    return files_list


def compare_density(sborka_den: int, file_den: int):  # Возможно переиграть имя функции.
    if int(sborka_den) < int(file_den):
        return True


path = input('Укажите путь к макетам в конкретной сборке:\n')
sborkas_name = path.split('\\')[-1]
sborkas_density = re.findall(r'(?i).*?_(80|90|115|128|130|150|170|200)(?:ofset|mat|_)+', sborkas_name)[0]
# Проверить случай, при передаче не корректного пути
filenames_to_print = create_files_list(path)
denser_files = list()
understood_filenames = list()

for filename in filenames_to_print:
    filename_density = re.findall(r'', filename)[0]  # Написать рег. выражение для поиска плотности тонкого макета.

    if filename_density and compare_density(sborkas_density, filename_density):
        denser_files.append(filename)
    if not filename_density:
        understood_filenames.append(filename)

# print(sborkas_name)
# print(sborkas_density)
a = f'| Name - {sborkas_name} |'
b = f'+{"-" * (len(a) - 2)}+'
print(f'{b}\n{a}\n{b}')