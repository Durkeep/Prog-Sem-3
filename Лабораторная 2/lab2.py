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

    height — число уровней, root — значение корня.
    left_leaf и right_leaf вычисляют потомков по значению текущего узла.
    Пропущенные аргументы берутся из варианта 14.
    Результат — словарь с ключами value, left, right; нет потомка — None.
    Высота 0 даёт None, высота 1 — только корень.
    Нецелая высота вызывает TypeError, отрицательная — ValueError.
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
