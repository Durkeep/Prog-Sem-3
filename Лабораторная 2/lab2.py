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
    """Проверить значения узлов, высоту и пользовательские формулы."""

    def test_defaults(self):
        """Проверить формулы варианта 14 на нескольких уровнях."""
        tree = gen_bin_tree()
        self.assertEqual(tree["value"], 14)
        self.assertEqual(tree["left"]["value"], -11)
        self.assertEqual(tree["right"]["value"], 28)
        self.assertEqual(tree["left"]["left"]["value"], 14)
        self.assertEqual(tree["right"]["left"]["value"], -25)
        leaf = tree["right"]["right"]["right"]
        self.assertEqual(leaf["value"], 112)
        self.assertIsNone(leaf["left"])
        self.assertIsNone(leaf["right"])

    def test_partial_override(self):
        """Непереданные аргументы сохраняют значения по умолчанию."""
        tree = gen_bin_tree(height=2, root=5, left_leaf=lambda x: x + 10)
        self.assertEqual(tree["left"]["value"], 15)
        self.assertEqual(tree["right"]["value"], 10)
        tree = gen_bin_tree(height=2, right_leaf=lambda x: x - 10)
        self.assertEqual(tree["value"], 14)
        self.assertEqual(tree["left"]["value"], -11)
        self.assertEqual(tree["right"]["value"], 4)

    def test_empty_tree(self):
        """При нулевой высоте дерево пустое."""
        self.assertIsNone(gen_bin_tree(height=0))

    def test_one_level(self):
        """При высоте один есть только корень."""
        self.assertEqual(
            gen_bin_tree(height=1, root=10),
            {"value": 10, "left": None, "right": None},
        )

    def test_custom_rules(self):
        """Формулы применяются к текущему узлу на каждом уровне."""
        tree = gen_bin_tree(3, 10, lambda x: x + 1, lambda x: x - 1)
        self.assertEqual(tree, {
            "value": 10,
            "left": {
                "value": 11,
                "left": {"value": 12, "left": None, "right": None},
                "right": {"value": 10, "left": None, "right": None},
            },
            "right": {
                "value": 9,
                "left": {"value": 10, "left": None, "right": None},
                "right": {"value": 8, "left": None, "right": None},
            },
        })

    def test_zero_root(self):
        """Нулевой корень не заменяется значением по умолчанию."""
        self.assertEqual(gen_bin_tree(height=1, root=0)["value"], 0)

    def test_fractional_values(self):
        """В узлах могут храниться дробные числа."""
        tree = gen_bin_tree(2, 5, lambda x: x / 2, lambda x: x * 2)
        self.assertEqual(tree["left"]["value"], 2.5)
        self.assertEqual(tree["right"]["value"], 10)

    def test_negative_height(self):
        """Отрицательная высота вызывает понятную ошибку."""
        with self.assertRaises(ValueError):
            gen_bin_tree(height=-1)

    def test_invalid_height_type(self):
        """Высота должна быть целым числом, а не строкой или дробью."""
        for height in (1.5, "3", True):
            with self.subTest(height=height):
                with self.assertRaises(TypeError):
                    gen_bin_tree(height=height)

    def test_leaf_does_not_call_rules(self):
        """Для последнего уровня формулы потомков не вызываются."""
        def fail(value):
            """Сообщить о ненужном вычислении потомка."""
            raise AssertionError("У листа нет потомков")

        self.assertEqual(gen_bin_tree(1, 7, fail, fail)["value"], 7)

    def test_list(self):
        """Список сохраняет значение и порядок обеих ветвей."""
        tree = gen_bin_tree(2, 1, lambda x: x + 1, lambda x: x + 2)
        self.assertEqual(to_list(tree), [1, [2, None, None], [3, None, None]])

    def test_namedtuple(self):
        """Именованный кортеж сохраняет обе ветви и доступ по именам."""
        tree = gen_bin_tree(2, 1, lambda x: x + 1, lambda x: x + 2)
        node = to_namedtuple(tree)
        self.assertEqual(node.value, 1)
        self.assertEqual(node.left.value, 2)
        self.assertEqual(node.right.value, 3)
        self.assertIsNone(node.left.left)
        self.assertIsNone(node.left.right)
        self.assertIsNone(node.right.left)
        self.assertIsNone(node.right.right)

    def test_empty_conversions(self):
        """Преобразование пустого дерева возвращает None."""
        self.assertIsNone(to_list(None))
        self.assertIsNone(to_namedtuple(None))


if __name__ == "__main__":
    print(gen_bin_tree())
    unittest.main(verbosity=2)
