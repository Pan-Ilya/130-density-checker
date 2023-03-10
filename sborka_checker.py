import re
import os
import patterns
from pretty_info import SborkaInfo


def main():
    '''Функция работает в 2ух режимах:
        - проверки конкретной сборки
        - проверки директории, содержащей ряд сборок.
    В обоих случаях для проверки используется ф-ция "sborka_checker", результат своей работы выводится в терминал.'''

    print('Добро пожаловать !\n')
    while True:
        ans = input('''Что будем делать?:\
        \n - [1] проверяем конкретную сборку.\
        \n - [2] проверяем партию сборок.\n''')

        if int(ans) == 1:
            path = input('Укажите путь к файлам тонкой сборки:\n')
            sborka_checker(path)

        elif int(ans) == 2:
            path = input('Укажите путь к тонким сборкам:\n')
            for dir in os.scandir(path):
                if dir.is_dir() and re.findall(patterns.right_sborka_name_pattern, dir.name):
                    sborka_checker(dir.path)
                elif dir.is_dir() and not re.findall(patterns.right_sborka_name_pattern, dir.name):
                    SborkaInfo.print_incorrect_name(dir.name)

        ans_1 = int(input('\nЖелаете продолжить? [1 - Yes; 2 - No]:\n'))
        if int(ans_1) == 1:
            continue
        else:
            break


def sborka_checker(path: str) -> None:
    '''Проверяет корректность имён файлов сборки согласно плотности и типа бумаги самой сборки.'''

    sborkas_name = path.split('\\')[-1]
    sborkas_density = get_sborkas_density(sborkas_name)

    filenames_to_print = get_files_list(path)

    denser_files = list()
    ofset_files = list()
    raflatak_files = list()
    incorrect_files = list()

    for filename in filenames_to_print:
        if not is_correct_filename(filename):
            incorrect_files.append(filename)
            continue

        filename_density = get_filename_density(filename)

        if filename_is_denser(sborkas_density, filename_density):
            denser_files.append(filename)
            continue

        if filename_is_ofset(sborkas_density, filename_density):
            ofset_files.append(filename)
            continue

        if filename_is_raflatak(sborkas_name, filename):
            raflatak_files.append(filename)

    SborkaInfo.print_info(name=sborkas_name,
                          density=sborkas_density,
                          ofset_files=ofset_files,
                          denser_files=denser_files,
                          raflatak_files=raflatak_files,
                          incorrect_files=incorrect_files)


def get_sborkas_density(sborkas_name: str) -> int:
    '''Возвращает плотность сборки из имени папки. Например:
        sborkas_name - 12345_1000_64x90_200mat_11_01_2023_ArtStudija_name
        sborkas_density - 200mat.'''

    sborka_density = re.findall(patterns.right_sborka_name_pattern, sborkas_name)[0][3]
    return int(sborka_density)


def get_files_list(path: str) -> list:
    '''Рекурсивно собираем все имена файлов в указанной директории и в её поддиректориях.'''

    files_list = list()

    for dirpath, dirnames, filnames in os.walk(path):
        if filnames:
            files_list.extend(filnames)
    return files_list


def get_filename_density(filename: str) -> int:
    '''Возвращает плотность файла из его имени. Например:
        filename - 12-12_98765_49x89_4+4_800_GL1+0_2000
        filename_density - 800.'''

    filename_density = re.findall(patterns.right_filename_pattern, filename)[0][4]
    filename_density = ''.join(filter(str.isdigit, filename_density))
    return int(filename_density)


def filename_is_denser(sborka_den: int, file_den: int) -> bool:
    '''Сравнивает плотность файла и плотность сборки.
    Если плотность файла выше плотность сборки + допустимый диапазон значений -> возвращает True.
    Пример:
        sborka_den = 128
        file_den = 130
        130 > 128 + 5 = 133 -> False.'''

    density_diapason = 5
    if file_den > sborka_den + density_diapason:
        return True
    return False


def is_correct_filename(filename: str) -> bool:
    '''Проверка корректности имени файла согласно регулярному выражению.'''

    return bool(re.findall(patterns.right_filename_pattern, filename))


def filename_is_ofset(sborka_den: int, file_den: int) -> bool:
    '''Проверка на наличие офсетного файла в НЕ офсетной сборки.'''

    if sborka_den != 80 and file_den == 80:
        return True
    return False


def filename_is_raflatak(sborkas_name: str, filename: str) -> bool:
    '''Проверка на наличие файла Raflatak в не-Raflatak сборке.'''

    if 'raflatak' not in sborkas_name and 'raflatak' in filename:
        return True
    return False


if __name__ == '__main__':
    main()
