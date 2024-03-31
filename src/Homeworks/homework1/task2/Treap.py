from random import randint
from typing import Generic, MutableMapping, Optional, Set, TypeVar

Key = TypeVar("Key")
Value = TypeVar("Value")


class Node(Generic[Key, Value]):
    def __init__(self, key: Key, value: Value) -> None:
        self.key: Key = key
        self.value: Value = value
        self.priority: int = randint(1, 10**9)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self) -> str:
        if self:
            return f"<key = {self.key}, value = {self.value}, priority = {self.priority}>, left={self.left.__repr__()}, right={self.right.__repr__()}"
        else:
            return "None"


class Treap(MutableMapping):
    def __init__(self, root=None) -> None:
        self.root: Optional[Node] = root
        self.length: int = 0

    def __len__(self) -> int:
        return self.length

    @staticmethod
    def split(root: Node, key: Key) -> tuple[Optional[Node], Optional[Node]]:
        if root is None:
            return None, None
        if root.key < key:
            first_root, second_root = Treap.split(root.right, key)
            root.right = first_root
            return root, second_root
        else:
            first_root, second_root = Treap.split(root.left, key)
            root.left = second_root
            return first_root, root

    @staticmethod
    def merge(first_root: Optional[Node], second_root: Optional[Node]) -> Optional[Node]:
        if first_root is None:
            return second_root
        if second_root is None:
            return first_root
        if first_root.priority > second_root.priority:
            first_root.right = Treap.merge(first_root.right, second_root)
            return first_root
        else:
            second_root.left = Treap.merge(first_root, second_root.left)
            return second_root

    def __delitem__(self, key: Key) -> None:
        first_treap, second_treap = self.split(self.root, key)
        node_to_del, new_second_treap = self.split(second_treap, key + 1)
        if node_to_del is None:
            raise KeyError(f"No key {key} in structure.")
        del node_to_del
        self.root = self.merge(first_treap, new_second_treap)
        self.length -= 1

    def __getitem__(self, key) -> Value:
        def find(root, key):
            if root is not None:
                if root.key == key:
                    return root.value
                elif root.key > key:
                    return find(root.left, key)
                else:
                    return find(root.right, key)
            raise KeyError(f"No key {key} in structure.")

        return find(self.root, key)

    def __setitem__(self, key: Key, value: Value) -> None:
        if self.root:
            first_treap, second_treap = self.split(self.root, key)
            new_node = Node(key, value)
            first_treap = self.merge(first_treap, new_node)
            self.root = self.merge(first_treap, second_treap)
        else:
            self.root = Node(key, value)
        self.length += 1

    def __iter__(self) -> iter:
        def iterate(node: Optional[Node], output: Set[Key]) -> set:
            if node is not None:
                output.add(node.key)
                output = iterate(node.left, output)
                output = iterate(node.right, output)
            return output

        return iter(iterate(self.root, set()))

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        root = self.root
        if root:
            return f"<key = {root.key}, value = {root.value}, priority = {root.priority}>, left={root.left.__repr__()}, right={root.right.__repr__()}"
        else:
            return "None"
