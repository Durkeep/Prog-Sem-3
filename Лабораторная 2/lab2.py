"""Построить бинарное дерево рекурсивно (вариант 14).

gen_bin_tree возвращает вложенные словари с ключами value, left, right.
Запуск дерева и тестов: python lab2.py. Требуется Python 3.10 или новее.
"""

import unittest
from collections import namedtuple


def gen_bin_tree(
    height: int = 4,
    root: int | float = 14,
    left_leaf=lambda x: 2 - (x - 1),
    right_leaf=lambda x: x * 2,
) -> dict | None:
    """Вернуть бинарное дерево заданной высоты с помощью рекурсии.

    height - число уровней, root - значение корня.
    left_leaf и right_leaf вычисляют потомков по значению текущего узла.
    Пропущенные аргументы берутся из варианта 14.
    Результат - словарь с ключами value, left, right; нет потомка - None.
    Высота 0 даёт None, высота 1 - только корень.
    Нецелая высота вызывает TypeError, отрицательная - ValueError.
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


Node = namedtuple("Node", ["value", "left", "right"])


def to_list(tree: dict | None) -> list | None:
    """Скопировать дерево в списки [value, left, right] или вернуть None."""
    if tree is None:
        return None
    return [tree["value"], to_list(tree["left"]), to_list(tree["right"])]


def to_namedtuple(tree: dict | None) -> Node | None:
    """Скопировать дерево в именованные кортежи или вернуть None."""
    if tree is None:
        return None
    return Node(
        tree["value"],
        to_namedtuple(tree["left"]),
        to_namedtuple(tree["right"]),
    )


class TestBinTree(unittest.TestCase):
    """Проверить основные требования задания."""

    def test_defaults(self):
        """Проверить корень, формулы и высоту варианта 14."""
        tree = gen_bin_tree()
        self.assertEqual(tree["value"], 14)
        self.assertEqual(tree["left"]["value"], -11)
        self.assertEqual(tree["right"]["value"], 28)
        leaf = tree["right"]["right"]["right"]
        self.assertEqual(leaf, {"value": 112, "left": None, "right": None})

    def test_empty_tree(self):
        """При высоте 0 дерево пустое."""
        self.assertIsNone(gen_bin_tree(height=0))

    def test_one_level(self):
        """При высоте 1 есть только заданный корень."""
        self.assertEqual(gen_bin_tree(height=1, root=5),
                         {"value": 5, "left": None, "right": None})

    def test_custom_rules(self):
        """Свои формулы работают на нескольких уровнях."""
        tree = gen_bin_tree(3, 10, lambda x: x + 1, lambda x: x - 1)
        self.assertEqual(tree["left"]["value"], 11)
        self.assertEqual(tree["right"]["value"], 9)
        self.assertEqual(tree["left"]["left"]["value"], 12)
        self.assertEqual(tree["right"]["right"]["value"], 8)
        self.assertIsNone(tree["left"]["left"]["left"])

    def test_containers(self):
        """Список и именованный кортеж сохраняют дерево."""
        tree = gen_bin_tree(height=2)
        self.assertEqual(to_list(tree),
                         [14, [-11, None, None], [28, None, None]])
        self.assertEqual(to_namedtuple(tree),
                         Node(14, Node(-11, None, None), Node(28, None, None)))


if __name__ == "__main__":
    print(gen_bin_tree())
    unittest.main(verbosity=2)
