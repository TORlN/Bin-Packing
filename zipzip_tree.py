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
from hybrid_sort3 import hybrid_sort3_desc


KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')


@dataclass(order=True)
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
	parent: Node

class ZipZipTree:
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.size = 0
		self.root = None

	def get_random_rank(self) -> Rank:
		geometric_rank = int(math.log(random.random()) / math.log(.5))
		if self.capacity > 1:
			max_uniform = int(math.log2(self.capacity)**3) - 1
			uniform_rank = random.randint(0, max_uniform)
		else:
			uniform_rank = 0
		return Rank(geometric_rank, uniform_rank)



	def insert(self, key: KeyType, val: ValType, rank: Rank = None):
		self.size += 1
		existing_node = self.findNode(key)
		if existing_node and isinstance(val[0], list):
			if val[0][0] not in existing_node.val[0]:
				existing_node.val[0].append(val[0][0])
			return None
		if rank is None:
			rank = self.get_random_rank()
		x = Node(key, val, rank, None, None, None)
		cur = self.root
		prev = None
		while cur is not None and (rank < cur.rank or (rank == cur.rank and key > cur.key)):
			prev = cur
			if key < cur.key:
				cur = cur.left
			else:
				cur = cur.right
		if cur == self.root:
			self.root = x
		elif key < prev.key:
			prev.left = x
			x.parent = prev
		else:
			prev.right = x
			x.parent = prev

		if cur is None:
			x.left = None
			x.right = None
			return x
		if key < cur.key:
			x.right = cur
			cur.parent = x
		else:
			x.left = cur
			cur.parent = x
		prev = x
		while cur is not None:
			fix = prev
			if cur.key < key:
				while cur is not None and cur.key <= key:
					prev = cur
					cur = cur.right
			else:
				while cur is not None and cur.key >= key:
					prev = cur
					cur = cur.left   
			if fix.key > key or (fix == x and prev.key > key):
				fix.left = cur
				if cur:
					cur.parent = fix
			else:
				fix.right = cur
				if cur:
					cur.parent = fix
		return x

	def remove(self, key: KeyType):
		self.size -= 1
		cur = self.root
		val = None
		prev = None
		while key != cur.key:
			prev = cur
			if key < cur.key:
				cur = cur.left
			else:
				cur = cur.right
		if isinstance(cur.val[0], list):
			if len(cur.val[0]) > 1:
				val = cur.val[0].pop()

		left = cur.left
		right = cur.right

		if left is None:
			next_node = right
		elif right is None:
			next_node = left
		elif left.rank >= right.rank:
			next_node = left
		else:
			next_node = right

		if next_node:
			next_node.parent = prev

		if prev is None:
			self.root = next_node
		elif key < prev.key:
			prev.left = next_node
		else:
			prev.right = next_node

		
		lowest_affected_node = next_node if next_node else prev 

		while left is not None and right is not None:
			if left.rank >= right.rank:
				while left is not None and left.rank >= right.rank:
					prev = left
					left = left.right
				prev.right = right
				if right:
					right.parent = prev
			else:
				while right is not None and left.rank < right.rank:
					prev = right
					right = right.left
				prev.left = left
				if left:
					left.parent = prev

			lowest_affected_node = prev
		if val is not None:
			return lowest_affected_node, val
		return lowest_affected_node

	def find(self, key: KeyType) -> ValType:
		return self._find(self.root, key)

	def findNode(self, key: KeyType) -> Node:
		return self._findNode(self.root, key)

	def _findNode(self, node: Node, key: KeyType) -> Node:

		if node is None:
			return None
		if key < node.key:
			return self._findNode(node.left, key)
		if key > node.key:
			return self._findNode(node.right, key)
		return node


	def _find(self, node: Node, key: KeyType) -> ValType:
		if node is None:
			return self.root.val
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
		if node is None:
			return 0
		if key < node.key:
			return 1 + self._get_depth(node.left, key)
		if key > node.key:
			return 1 + self._get_depth(node.right, key)
		return 1



