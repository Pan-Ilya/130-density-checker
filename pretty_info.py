from rich import print
from rich import box
from rich.text import Text
from rich.panel import Panel
from rich.tree import Tree
from rich.table import Table


class SborkaInfo:
    tree_phrases = [Text('Список файлов плотностью 80 г/м2:', style='magenta bold'),
                    Text('Список более плотных макетов:', style='magenta'),
                    Text('Внимание, присутствуют файлы Raflatak:', style='cyan'),
                    Text('Не могу прочитать имена следующих файлов:', style='cyan bold')]

    @classmethod
    def build_trees(cls,
                    *,
                    ofset_files: list,
                    denser_files: list,
                    raflatak_files: list,
                    incorrect_files: list) -> list:

        trees = list()
        for indx, lst in enumerate([ofset_files, denser_files, raflatak_files, incorrect_files]):
            tree = Tree(cls.tree_phrases[indx])
            for obj in lst:
                tree.add(obj)
            trees.append(tree)
            tree = None

        return trees

    @classmethod
    def build_table(cls, sborka_density: int, trees: list) -> Table:
        table = Table.grid(expand=True)
        table.add_column()
        table.add_row(Panel(f'Плотность сборки - {sborka_density} г/м2', border_style='red'))

        if all(map(lambda t: not t.children, trees)):
            table.add_row('Всё Ок :heavy_check_mark:', style='bold green')
        else:
            for tree in trees:
                if tree.children:
                    table.add_row(tree)
                    table.add_row()

        return table

    @classmethod
    def print_incorrect_name(cls, name: str):
        print(f'[magenta]\nНе понимаю имя сборки - {name}[/]')

    @classmethod
    def print_info(cls,
                   *,
                   name: str,
                   density: int,
                   ofset_files: list,
                   denser_files: list,
                   raflatak_files: list,
                   incorrect_files: list) -> None:

        trees = cls.build_trees(ofset_files=ofset_files,
                                denser_files=denser_files,
                                raflatak_files=raflatak_files,
                                incorrect_files=incorrect_files)

        table = cls.build_table(density, trees)
        name = Text(name, style='white')

        print('\n', Panel.fit(table, title=name, box=box.ROUNDED, border_style='cyan bold'))

        return None
