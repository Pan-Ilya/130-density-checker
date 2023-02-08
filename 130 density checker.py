import re
import os
import patterns


def main():
    path = input(f'{"*" * 55}\nУкажите путь к файлам тонкой сборки:\n')
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
        # print(filename_density)

        if filename_is_denser(sborkas_density, filename_density):
            denser_files.append(filename)
            continue

        if filename_is_ofset(sborkas_density, filename_density):
            ofset_files.append(filename)
            continue

        if filename_is_raflatak(sborkas_name, filename):
            raflatak_files.append(filename)

    print(f'\nИмя сборки - {sborkas_name}')
    print(f'Плотность сборки - {sborkas_density} г/м2', end='\n\n')

    print_info(denser_files, incorrect_files, ofset_files, raflatak_files)


def get_sborkas_density(sborkas_name: str) -> int:
    # sborkas_name - 12345_1000_64x90_200mat_11_01_2023_ArtStudija_name
    # sborkas_density - 200mat

    sborka_density = re.findall(patterns.sborka_density, sborkas_name)[0][1]
    return int(sborka_density)


def get_files_list(path: str) -> list:
    files_list = list()

    for dirpath, dirnames, filnames in os.walk(path):
        if filnames:
            files_list.extend(filnames)

    return files_list


def get_filename_density(filename: str) -> int:
    filename_density = re.findall(patterns.right_filename_pattern, filename)[0][4]
    filename_density = ''.join(filter(str.isdigit, filename_density))
    return int(filename_density)


def filename_is_denser(sborka_den: int, file_den: int) -> bool:
    # sborka_den = 128;  file_den = 130
    #  128 + 5 = 133
    #  128 - 5 = 123

    if file_den > sborka_den + 5:
        return True
    return False


def is_correct_filename(filename: str) -> bool:
    return bool(re.findall(patterns.right_filename_pattern, filename))


def filename_is_ofset(sborka_den: int, file_den: int) -> bool:
    if sborka_den != 80 and file_den == 80:
        return True
    return False


def filename_is_raflatak(sborkas_name: str, filename: str) -> bool:
    if 'raflatak' not in sborkas_name and 'raflatak' in filename:
        return True
    return False


def print_info(*args: list) -> None:
    phrases = [
        'Список более плотных макетов:',
        'Не могу прочитать имена следующих файлов:',
        'Список файлов плотностью 80 г/м2:',
        'Внимание, присутствуют файлы Raflatak:'
    ]

    for i, lst in enumerate(args):
        if lst:
            print(phrases[i])
            print(*lst, sep='\n', end='\n\n')

    if all(map(lambda lst: not bool(lst), args)):
        print('Всё Ок!\n')


if __name__ == '__main__':
    ans = 1
    while ans != 2:
        main()
        ans = int(input('Желаете продолжить? [1 - Yes; 2 - No]:\n'))
