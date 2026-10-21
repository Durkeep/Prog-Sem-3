"""Преобразовать дерево-словарь в список или collections.namedtuple."""

from collections import namedtuple


Node = namedtuple("Node", ["value", "left", "right"])


def to_list(tree: dict | None) -> list | None:
    """Вернуть вложенные списки вида [значение, левое, правое].

    tree — дерево-словарь или None для пустого дерева.
    Пустое дерево преобразуется в None. Исходное дерево не изменяется.
    """
    if tree is None:
        return None
    return [tree["value"], to_list(tree["left"]), to_list(tree["right"])]


def to_namedtuple(tree: dict | None) -> Node | None:
    """Вернуть дерево из именованных кортежей Node(value, left, right).

    tree — дерево-словарь или None для пустого дерева.
    Пустое дерево преобразуется в None. Исходное дерево не изменяется.
    """
    if tree is None:
        return None
    return Node(
        tree["value"],
        to_namedtuple(tree["left"]),
        to_namedtuple(tree["right"]),
    )
