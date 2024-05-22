from random import randint
from typing import Generic, Iterator, MutableMapping, Optional, Tuple, TypeVar

Key = TypeVar("Key")
Value = TypeVar("Value")


class Node(Generic[Key, Value]):
    def __init__(self, key: Key, value: Value) -> None:
        self.key: Key = key
        self.value: Value = value
        self.priority: int = randint(1, 10**9)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __iter__(self) -> Iterator[Key]:
        if self.left:
            yield from self.left
        yield self.key
        if self.right:
            yield from self.right

    def __repr__(self) -> str:
        return f"<key = {self.key}, value = {self.value}, priority = {self.priority}>, left={self.left.__repr__()}, right={self.right.__repr__()}"


class Treap(MutableMapping, Generic[Key, Value]):
    def __init__(self, root: Optional[Node] = None) -> None:
        self.root: Optional[Node] = root
        self.length: int = 0

    def __len__(self) -> int:
        return self.length

    @staticmethod
    def split(root: Optional[Node], key: Key) -> Tuple[Optional[Node], Optional[Node]]:
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
        def recursion(node: Node) -> Node | None:
            if key < node.key:
                if node.left is None:
                    raise ValueError(f"No element {key} in tree.")
                node.left = recursion(node.left)
            elif key > node.key:
                if node.right is None:
                    raise ValueError(f"No element {key} in tree.")
                node.right = recursion(node.right)
            else:
                return self.merge(node.left, node.right)
            return node

        if self.root is None:
            raise ValueError("Tree is empty.")
        self.root = recursion(self.root)
        self.length -= 1

    def __getitem__(self, key: Key) -> Optional[Value]:
        def find(root: Optional[Node], key: Key) -> Optional[Value]:
            if root is None:
                raise KeyError(f"No key {key} in structure.")
            if root.key == key:
                return root.value
            elif root.key > key:
                return find(root.left, key)
            else:
                return find(root.right, key)

        return find(self.root, key)

    def __setitem__(self, key: Key, value: Value) -> None:
        if not self.root:
            self.root = Node(key, value)
        else:
            first_treap, second_treap = self.split(self.root, key)
            new_node = Node(key, value)
            first_treap = self.merge(first_treap, new_node)
            self.root = self.merge(first_treap, second_treap)
        self.length += 1

    def __iter__(self) -> Iterator[Key]:
        if self.root is None:
            raise ValueError("Tree is empty.")
        return iter(self.root)

    def __str__(self) -> str:
        result = f"Count of elements in tree: {self.length}\n"
        result += f"Items in order:\n"
        for key in iter(self):
            result += f"Key: {key}, Value: {self[key]}"
        return result

    def __repr__(self) -> str:
        root = self.root
        if root:
            return f"<key = {root.key}, value = {root.value}, priority = {root.priority}>, left={root.left.__repr__()}, right={root.right.__repr__()}"
        else:
            return "None"
