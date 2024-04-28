# Explanations for ZipZipTree public member functions:

# any variable annotated with KeyType should use the same type for each tree, and should be comparable.
# ValType is for any additional data to be stored in the nodes.
# Rank is a container representing each node's rank, both geometric and uniform.
#           If using an earlier form of Python, you can use a named tuple instead.
# ZipZipTree(): constructs the zip-zip tree with a specific capacity.
# get_random_rank(): returns a random node rank, chosen independently from:
#           a geometric distribution of mean 1 and,
#           a uniform distribution of integers from 0 to log(capacity)^3 - 1 (log capacity cubed minus 1).
# insert(): inserts item with parameter key, value, and rank into tree.
#           if rank is not provided, a random rank should be selected by using get_random_rank().
# remove(): removes item with parameter key from tree.
#           you can assume that the item exists in the tree.
# find(): returns the value of item with parameter key.
#         you can assume that the item exists in the tree.
# get_size(): returns the number of nodes in the tree.
# get_height(): returns the height of the tree.
# get_depth(): returns the depth of the item with parameter key.
#              you can assume that the item exists in the tree.

from __future__ import annotations

from typing import TypeVar
from dataclasses import dataclass
import math
import random

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

@dataclass
class Rank:
	geometric_rank: int
	uniform_rank: int
 
@dataclass
class Node:
	key: KeyType
	val: ValType
	rank: Rank
	left: Node
	right: Node

class ZipZipTree:
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.size = 0
		self.root = None

	def get_random_rank(self) -> Rank:
		geometric_rank = int(math.log(1 - random.random()) / math.log(1 - .5))
		uniform_rank = random.randint(0, int(math.log(self.capacity) ** 3) - 1)
		return Rank(geometric_rank, uniform_rank)

	def insert(self, key: KeyType, val: ValType, rank: Rank = None):
		if rank is None:
			rank = self.get_random_rank()
		self.size += 1
		self.root = self._insert(self.root, key, val, rank)

	def _insert(self, node: Node, key: KeyType, val: ValType, rank: Rank) -> Node:
		if node is None:
			return Node(key, val, rank, None, None)
		if rank.geometric_rank < node.rank.geometric_rank or (rank.geometric_rank == node.rank.geometric_rank and rank.uniform_rank < node.rank.uniform_rank):
			if key < node.key:
				node.left = self._insert(node.left, key, val, rank)
			else:
				node.right = self._insert(node.right, key, val, rank)
			return node
		if key < node.key:
			node.left = self._insert(node.left, key, val, rank)
			return self._rotate_right(node)
		node.right = self._insert(node.right, key, val, rank)
		return self._rotate_left(node)

	def _rotate_right(self, node: Node) -> Node:
		if node.left.rank.geometric_rank < node.rank.geometric_rank or (node.left.rank.geometric_rank == node.rank.geometric_rank and node.left.rank.uniform_rank < node.rank.uniform_rank):
			return node
		left = node.left
		node.left = left.right
		left.right = node
		return left

	def _rotate_left(self, node: Node) -> Node:
		if node.right.rank.geometric_rank < node.rank.geometric_rank or (node.right.rank.geometric_rank == node.rank.geometric_rank and node.right.rank.uniform_rank < node.rank.uniform_rank):
			return node
		right = node.right
		node.right = right.left
		right.left = node
		return right

	def remove(self, key: KeyType):
		self.size -= 1
		self.root = self._remove(self.root, key)

	def _remove(self, node: Node, key: KeyType) -> Node:
		if node is None:
			return None
		if key < node.key:
			node.left = self._remove(node.left, key)
			return node
		if key > node.key:
			node.right = self._remove(node.right, key)
			return node
		if node.left is None:
			return node.right
		if node.right is None:
			return node.left
		node.key = self._min(node.right)
		node.right = self._remove(node.right, node.key)
		return node

	def find(self, key: KeyType) -> ValType:
		return self._find(self.root, key)

	def _find(self, node: Node, key: KeyType) -> ValType:
		if node is None:
			return None
		if key < node.key:
			return self._find(node.left, key)
		if key > node.key:
			return self._find(node.right, key)
		return node.val

	def get_size(self) -> int:
		return self.size

	def get_height(self) -> int:
		return self._get_height(self.root)-1

	def _get_height(self, node: Node) -> int:
		if node is None:
			return 0
		return 1+ max(self._get_height(node.left), self._get_height(node.right))

	def get_depth(self, key: KeyType):
		return self._get_depth(self.root, key)-1

	def _get_depth(self, node: Node, key: KeyType):
		if key < node.key:
			return 1 + self._get_depth(node.left, key)
		if key > node.key:
			return 1 + self._get_depth(node.right, key)
		return 1