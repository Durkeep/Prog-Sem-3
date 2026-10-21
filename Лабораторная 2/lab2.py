"""Построить бинарное дерево рекурсивно (вариант 14).

gen_bin_tree возвращает вложенные словари с ключами value, left, right.
Запуск примера: python lab2.py. Требуется Python 3.10 или новее.
"""

from pprint import pprint
from typing import Callable


def gen_bin_tree(
    height: int = 4,
    root: int | float = 14,
    left_leaf: Callable[[int | float], int | float] = lambda x: 2 - (x - 1),
    right_leaf: Callable[[int | float], int | float] = lambda x: x * 2,
) -> dict | None:
    """Вернуть бинарное дерево заданной высоты с помощью рекурсии.

    Аргументы:
        height: число уровней (по умолчанию 4). Ноль задаёт пустое дерево.
        root: значение корня (по умолчанию 14).
        left_leaf: формула левого потомка (по умолчанию 2 - (x - 1)).
        right_leaf: формула правого потомка (по умолчанию x * 2).

    Формулы получают значение текущего узла. Каждый узел — словарь
    с ключами value, left, right. Отсутствующий потомок обозначается None.
    При высоте 1 дерево состоит только из корня.

    Вызывает TypeError, если высота не целое число, и ValueError,
    если высота отрицательная. Слишком большая высота может привести
    к RecursionError или нехватке памяти.
    """
    if type(height) is not int:
        raise TypeError("Высота должна быть целым числом")
    if height < 0:
        raise ValueError("Высота не может быть отрицательной")
    if height == 0:
        return None

    tree = {"value": root, "left": None, "right": None}
    if height > 1:
        tree["left"] = gen_bin_tree(height - 1, left_leaf(root), left_leaf, right_leaf)
        tree["right"] = gen_bin_tree(height - 1, right_leaf(root), left_leaf, right_leaf)
    return tree


if __name__ == "__main__":
    pprint(gen_bin_tree(), sort_dicts=False)
