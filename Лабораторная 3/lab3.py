"""Построить бинарное дерево без рекурсии (вариант 14).

gen_bin_tree возвращает вложенные словари с ключами value, left, right.
Запуск примера: python lab3.py. Требуется Python 3.10 или новее.
"""

from pprint import pprint
from typing import Callable


def gen_bin_tree(
    height: int = 4,
    root: int | float = 14,
    left_leaf: Callable[[int | float], int | float] = lambda x: 2 - (x - 1),
    right_leaf: Callable[[int | float], int | float] = lambda x: x * 2,
) -> dict | None:
    """Вернуть бинарное дерево заданной высоты с помощью цикла.

    Аргументы:
        height: число уровней (по умолчанию 4). Ноль задаёт пустое дерево.
        root: значение корня (по умолчанию 14).
        left_leaf: формула левого потомка (по умолчанию 2 - (x - 1)).
        right_leaf: формула правого потомка (по умолчанию x * 2).

    Формулы получают значение текущего узла. Каждый узел — словарь
    с ключами value, left, right. Отсутствующий потомок обозначается None.
    При высоте 1 дерево состоит только из корня. Рекурсия не используется.

    Вызывает TypeError, если высота не целое число, и ValueError,
    если высота отрицательная. Число узлов быстро растёт с высотой,
    поэтому для больших деревьев может не хватить памяти.
    """
    if type(height) is not int:
        raise TypeError("Высота должна быть целым числом")
    if height < 0:
        raise ValueError("Высота не может быть отрицательной")
    if height == 0:
        return None

    tree = {"value": root, "left": None, "right": None}
    level = [tree]

    for _ in range(height - 1):
        next_level = []
        for node in level:
            node["left"] = {"value": left_leaf(node["value"]), "left": None, "right": None}
            node["right"] = {"value": right_leaf(node["value"]), "left": None, "right": None}
            next_level.append(node["left"])
            next_level.append(node["right"])
        level = next_level

    return tree


if __name__ == "__main__":
    pprint(gen_bin_tree(), sort_dicts=False)
