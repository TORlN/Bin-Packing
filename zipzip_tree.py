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
		self.size += 1
		if rank is None:
			rank = self.get_random_rank()
		x = Node(key, val, rank, None, None)
		cur = self.root
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
		else:
			prev.right = x
   
		if cur is None:
			x.left = None
			x.right = None
			return
		if key < cur.key:
			x.right = cur
		else:
			x.left = cur
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
			else:
				fix.right = cur

	def remove(self, key: KeyType):
		self.size -= 1
		cur = self.root
		prev = None
		while key is not cur.key:
			prev = cur
			if key < cur.key:
				cur = cur.left
			else:
				cur = cur.right
		left = cur.left
		right = cur.right
  

		if left is None:
			cur = right
		elif right is None:
			cur = left
		elif left.rank >= right.rank:
			cur = left
		else:
			cur = right
   
		if prev is None:
			self.root = cur
		elif key < prev.key:
			prev.left = cur
		else:
			prev.right = cur
		
		while left is not None and right is not None:
			if left.rank >= right.rank:
				while True:
					prev = left
					left = left.right
					if left is None or left.rank < right.rank:
						break
				prev.right = right
			else:
				while True:
					prev = right
					right = right.left
					if right is None or left.rank >= right.rank:
						break
				prev.left = left


	def find(self, key: KeyType) -> ValType:
		return self._find(self.root, key)

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