# TODO: Get rid of all flake8 warnings -- that means adding docstrings
#      to the file, classes, and methods.

DELETED = (-1, -1)


class SinglyLinkedNode(object):
    def __init__(self, item=None, next_link=None):
        """
        >>> node = SinglyLinkedNode((5,"five"), None)
        """
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        """
        >>> node = SinglyLinkedNode((5,"five"), None)
        >>> node.item
        (5, 'five')
        """
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        """
        >>> node2 = SinglyLinkedNode((5,"five"), None)
        >>> node = SinglyLinkedNode((4,"four"), node2)
        >>> node.next
        (5, 'five')
        """
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        """
        >>> node = SinglyLinkedNode((4,"four"), None)
        >>> node.__repr__()
        "(4, 'four')"
        """
        return repr(self.item)


class SinglyLinkedList(object):
    def __init__(self):
        """
        >>> l_list = SinglyLinkedList()
        """
        super(SinglyLinkedList, self).__init__()
        self.head = None

    def __len__(self):
        """
        >>> l_list = SinglyLinkedList()
        >>> l_list.__len__()
        0
        >>> l_list.prepend(4)
        '4 inserted'
        >>> l_list.__len__()
        1
        >>> l_list.remove(4)
        1
        >>> l_list.__len__()
        0
        """
        node = self.head
        length = 0
        while node is not None:
            length += 1
            node = node.next
        return length

    def __iter__(self):
        """
        >>> l_list = SinglyLinkedList()
        >>> l_list.prepend(4)
        '4 inserted'
        >>> for item in l_list.__iter__(): print item
        4
        """
        node = self.head
        while node is not None:
            yield str(node.item)
            node = node.next

    def __contains__(self, item):
        """
        >>> l_list = SinglyLinkedList()
        >>> l_list.prepend(4)
        '4 inserted'
        >>> l_list.__contains__(4)
        True
        >>> l_list.__contains__(10)
        False
        """
        node = self.head
        contains = False
        while node is not None:
            if node.item == item:
                contains = True
                break
            else:
                node = node.next
        return contains

    def remove(self, item):
        """
        >>> l_list = SinglyLinkedList()
        >>> l_list.prepend(4)
        '4 inserted'
        >>> l_list.remove(4)
        1
        >>> l_list.remove(10)
        0
        """
        node = self.head
        if node is None:
            return 0
        elif node.item == item:
            self.head = node.next
            node.item = None
            node.next = None
            return 1
        else:
            while node.next is not None:
                if node.next.item == item:
                    break
                node = node.next
            if node.next is not None:
                temp = node.next
                node.next = temp.next
                temp.item = None
                temp.next = None
                return 1
        return 0

    def prepend(self, item):
        """
        >>> l_list = SinglyLinkedList()
        >>> l_list.prepend(4)
        '4 inserted'
        """
        node = SinglyLinkedNode(item)
        if self.head is not None:
            node.next = self.head
        self.head = node
        return str(item) + " inserted"

    def __repr__(self):
        """
        >>> l_list = SinglyLinkedList()
        >>> l_list.prepend(4)
        '4 inserted'
        >>> l_list. prepend(5)
        '5 inserted'
        >>> l_list.__repr__()
        'List:5->4'
        """
        s = "List:" + "->".join([item for item in self])
        return s


class ChainedHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        """
        >>> chained_hash = ChainedHashDict(hashfunc=terrible_hash(11))
        """
        super(ChainedHashDict, self).__init__()
        self.__bin_count = bin_count
        self.hash_table = [None] * bin_count
        self.hash_fun = hashfunc
        self.__max_load = max_load
        self.__length = 0

    @property
    def load_factor(self):
        """
        >>> chained_hash = ChainedHashDict(hashfunc=terrible_hash(11))
        >>> chained_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> chained_hash.load_factor
        0.1
        """
        return float(self.__len__()) / float(self.__bin_count)

    @property
    def bin_count(self):
        """
        >>> chained_hash = ChainedHashDict(hashfunc=terrible_hash(11))
        >>> chained_hash.bin_count
        10
        """
        return self.__bin_count

    def rebuild(self, bin_count):
        if self.load_factor > self.__max_load:
            self.__length = 0
            self.__bin_count *= 2
            old_table = self.hash_table
            self.hash_table = [None] * self.bin_count
            for index in range(len(old_table)):
                linked_list = old_table[index]
                if linked_list is not None:
                    node = linked_list.head
                    while node is not None:
                        self.__setitem__(node.item[0], node.item[1])
                        node = node.next

    def __getitem__(self, key):
        """
        >>> chained_hash = ChainedHashDict(hashfunc=terrible_hash(11))
        >>> chained_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> chained_hash.__getitem__(5)
        'five'
        >>> chained_hash.__getitem__(15)
        """
        linked_list = self.hash_table[self.hash_fun(key) % self.bin_count]
        if linked_list is not None:
            node = linked_list.head
            while node is not None:
                if node.item[0] == key:
                    return node.item[1]
                else:
                    node = node.next
        return None

    def __setitem__(self, key, value):
        """
        >>> chained_hash = ChainedHashDict(hashfunc=terrible_hash(11))
        >>> chained_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        """
        item = (key, value)
        index = self.hash_fun(key) % self.bin_count
        linked_list = self.hash_table[index]
        if linked_list is None:
            linked_list = SinglyLinkedList()
        linked_list.prepend(item)
        self.hash_table[index] = linked_list
        self.__length += 1
        self.rebuild(self.bin_count)
        return str(item) + " inserted"

    def __delitem__(self, key):
        """
        >>> chained_hash = ChainedHashDict(hashfunc=terrible_hash(11))
        >>> chained_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> chained_hash.__delitem__(5)
        item: (5, 'five') removed from hash table
        >>> chained_hash.__delitem__(6)
        No item with key =  6 found in hash table.
        """
        value = self.__getitem__(key)
        if value is not None:
            item = (key, value)
            index = self.hash_fun(key) % self.bin_count
            linked_list = self.hash_table[index]
            linked_list.remove(item)
            if linked_list.head is None:
                self.hash_table[index] = None
            self.__length -= 1
            print "item: " + str(item) + " removed from hash table"
        else:
            print "No item with key =  " + str(key) + " found in hash table."

    def __contains__(self, key):
        """
        >>> chained_hash = ChainedHashDict(hashfunc=terrible_hash(11))
        >>> chained_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> chained_hash.__contains__(5)
        True
        >>> chained_hash.__contains__(7)
        False
        """
        value = self.__getitem__(key)
        if value is not None:
            return True
        else:
            return False

    def __len__(self):
        """
        >>> chained_hash = ChainedHashDict(hashfunc=terrible_hash(11))
        >>> chained_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> chained_hash.__len__()
        1
        """
        return self.__length

    def display(self):
        """
        >>> chained_hash = ChainedHashDict(bin_count=1, hashfunc=terrible_hash(11))
        >>> chained_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> chained_hash.display()
        ---------------Display Hash Table-----------
        0 | Empty
        -----------
        1 | ->(5, 'five')
        -----------
        """

        print "---------------Display Hash Table-----------"
        for index in range(len(self.hash_table)):
            linked_list = self.hash_table[index]
            if linked_list is None:
                print str(index) + " | Empty"
                print "-----------"
            else:
                print str(index) + " | ->" + "->".join([str(item) for item in linked_list])
                print "-----------"


class OpenAddressHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        """
        >>> open_hash = OpenAddressHashDict(hashfunc=terrible_hash(10))
        """
        super(OpenAddressHashDict, self).__init__()
        self.__bin_count = bin_count
        self.__max_load = 0.7
        self.__hash_fun = hashfunc
        self.hash_table = [None] * bin_count
        self.__length = 0

    @property
    def load_factor(self):
        """
        >>> open_hash = OpenAddressHashDict(hashfunc=terrible_hash(10))
        >>> open_hash.load_factor
        0.0
        >>> open_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> open_hash.load_factor
        0.1
        """
        return float(self.__len__()) / float(self.bin_count)

    @property
    def bin_count(self):
        """
        >>> open_hash = OpenAddressHashDict(hashfunc=terrible_hash(10))
        >>> open_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> open_hash.bin_count
        10
        """
        return self.__bin_count

    def rebuild(self, bincount):
        if self.load_factor > self.__max_load:
            self.__length = 0
            bincount *= 2
            self.__bin_count = bincount
            old_table = self.hash_table
            self.hash_table = [None] * self.bin_count
            for index in range(len(old_table)):
                item = old_table[index]
                if item is not None:
                    self.__setitem__(item[0], item[1])

    def __getitem__(self, key):
        """
        >>> open_hash = OpenAddressHashDict(hashfunc=terrible_hash(10))
        >>> open_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> open_hash.__getitem__(5)
        'five'
        >>> open_hash.__getitem__(10)
        """
        i = 0
        index = (self.__hash_fun(key) + i) % self.bin_count
        item = self.hash_table[index]
        while item is not None and item[0] != key:
            i += 1
            index = (self.__hash_fun(key) + i) % self.bin_count
            item = self.hash_table[index]
        if item is not None and item != DELETED:
            return item[1]
        else:
            return None

    def __setitem__(self, key, value):
        """
        >>> open_hash = OpenAddressHashDict(hashfunc=terrible_hash(10))
        >>> open_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        """
        item = (key, value)
        i = 0
        index = (self.__hash_fun(key) + i) % self.bin_count
        while self.hash_table[index] is not None and self.hash_table[index] != DELETED:
            i += 1
            index = (self.__hash_fun(key) + i) % self.bin_count
        self.hash_table[index] = item
        self.__length += 1
        self.rebuild(self.bin_count)
        return str(item) + " inserted"

    def __delitem__(self, key):
        """
        >>> open_hash = OpenAddressHashDict(hashfunc=terrible_hash(10))
        >>> open_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> open_hash.__delitem__(10)
        item with key: 10 not found
        >>> open_hash.__delitem__(5)
        item (5, 'five') with key: 5 deleted
        """
        i = 0
        index = (self.__hash_fun(key) + i) % self.bin_count
        item = self.hash_table[index]
        while item is not None and item[0] != key:
            i += 1
            index = (self.__hash_fun(key) + i) % self.bin_count
            item = self.hash_table[index]
        if item is not None:
            self.hash_table[index] = DELETED
            self.__length -= 1
            print("item " + str(item) + " with key: " + str(key) + " deleted")
        else:
            print ("item with key: " + str(key) + " not found")

    def __contains__(self, key):
        """
        >>> open_hash = OpenAddressHashDict(hashfunc=terrible_hash(10))
        >>> open_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> open_hash.__contains__(10)
        False
        >>> open_hash.__contains__(5)
        True
        """
        value = self.__getitem__(key)
        if value is not None:
            return True
        return False

    def __len__(self):
        """
        >>> open_hash = OpenAddressHashDict(hashfunc=terrible_hash(10))
        >>> open_hash.__len__()
        0
        >>> open_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> open_hash.__len__()
        1
        """
        return self.__length

    def display(self):
        """
        >>> open_hash = OpenAddressHashDict(bin_count=2 ,hashfunc=terrible_hash(10))
        >>> open_hash.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> open_hash.display()
        0 | (5, 'five')
        -----------
        1 | Empty
        -----------
        """
        for index in range(len(self.hash_table)):
            if self.hash_table[index] is None:
                val = "Empty"
            elif self.hash_table[index] == DELETED:
                val = "Deleted"
            else:
                val = str(self.hash_table[index])
            print str(index) + " | " + val
            print "-----------"


class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTreeDict(object):
    def __init__(self):
        super(BinarySearchTreeDict, self).__init__()
        self.root = None
        self.length = 0
        self.l_height = 0
        self.r_height = 0

    @property
    def height(self):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.height
        -1
        >>> binary_tree.__setitem__(1, "one")
        "(1, 'one') inserted"
        >>> binary_tree.height
        0
        """
        return self.__calculate_height(self.root)

    def __calculate_height(self, b_tree):
        if b_tree is None:
            return -1
        else:
            return 1 + max(self.__calculate_height(b_tree.left), self.__calculate_height(b_tree.right))

    def in_order_keys(self):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> binary_tree.__setitem__(3, "Three")
        "(3, 'Three') inserted"
        >>> binary_tree.__setitem__(7, "seven")
        "(7, 'seven') inserted"
        >>> binary_tree.in_order_keys()
        In-order tree traversal keys: 3->5->7
        """
        print "In-order tree traversal keys: " + "->".join([str(item[0]) for item in self.__in_order_print(self.root)])

    def __in_order_print(self, b_tree):
        if b_tree is None:
            StopIteration()
        else:
            for data in self.__in_order_print(b_tree.left):
                yield data
            yield b_tree.data
            for data in self.__in_order_print(b_tree.right):
                yield data

    def post_order_keys(self):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> binary_tree.__setitem__(3, "Three")
        "(3, 'Three') inserted"
        >>> binary_tree.__setitem__(7, "seven")
        "(7, 'seven') inserted"
        >>> binary_tree.post_order_keys()
        Post-order tree traversal keys: 3->7->5
        """
        print "Post-order tree traversal keys: " + "->".join(
            [str(item[0]) for item in self.__post_order_print(self.root)])

    def __post_order_print(self, b_tree):
        if b_tree is not None:
            for data in self.__post_order_print(b_tree.left):
                yield data
            for data in self.__post_order_print(b_tree.right):
                yield data
            yield b_tree.data
        else:
            StopIteration()

    def pre_order_keys(self):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> binary_tree.__setitem__(3, "Three")
        "(3, 'Three') inserted"
        >>> binary_tree.__setitem__(7, "seven")
        "(7, 'seven') inserted"
        >>> binary_tree.pre_order_keys()
        Pre-order tree traversal keys: 5->3->7
        """
        print "Pre-order tree traversal keys: " + "->".join(
            [str(item[0]) for item in self.__pre_order_print(self.root)])

    def __pre_order_print(self, b_tree):
        if b_tree is not None:
            yield b_tree.data
            for data in self.__pre_order_print(b_tree.left):
                yield data
            for data in self.__pre_order_print(b_tree.right):
                yield data
        else:
            StopIteration()

    def items(self):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> binary_tree.__setitem__(3, "Three")
        "(3, 'Three') inserted"
        >>> binary_tree.__setitem__(7, "seven")
        "(7, 'seven') inserted"
        >>> binary_tree.items()
        Values : Three -> five -> seven
        """
        print "Values : " + " -> ".join([str(item[1]) for item in self.__in_order_print(self.root)])

    def __getitem__(self, key):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> binary_tree.__getitem__(5)
        'five'
        >>> binary_tree.__getitem__(10)
        """
        b_tree = self.root
        while b_tree is not None:
            if b_tree.data[0] == key:
                return b_tree.data[1]
            elif key < b_tree.data[0]:
                b_tree = b_tree.left
            else:
                b_tree = b_tree.right
        return None

    def __setitem__(self, key, value):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        """
        data = (key, value)
        b_tree_node = BinaryTreeNode(data)
        if self.root is None:
            self.root = b_tree_node
            self.length += 1
        else:
            traverse = self.root
            self.__insert_node(traverse, b_tree_node)
        return str(data) + " inserted"

    def __insert_node(self, traverse, b_tree_node):
        if b_tree_node.data[0] < traverse.data[0]:
            if traverse.left is None:
                traverse.left = b_tree_node
                b_tree_node.parent = traverse
                self.length += 1
            else:
                self.__insert_node(traverse.left, b_tree_node)
        else:
            if traverse.right is None:
                traverse.right = b_tree_node
                b_tree_node.parent = traverse
                self.length += 1
            else:
                self.__insert_node(traverse.right, b_tree_node)

    def __delitem__(self, key):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> binary_tree.__delitem__(10)
        key: 10 not found
        >>> binary_tree.__delitem__(5)
        Item: (5, 'five') with key: 5 deleted.
        """
        self.__del_item_recursive(self.root, key)

    def __del_item_recursive(self, b_tree, key):
        if b_tree is None:
            print "key: " + str(key) + " not found"
            return b_tree
        if key < b_tree.data[0]:
            b_tree.left = self.__del_item_recursive(b_tree.left, key)
        elif key > b_tree.data[0]:
            b_tree.right = self.__del_item_recursive(b_tree.right, key)
        else:
            if b_tree.left is None and b_tree.right is None:
                print "Item: " + str(b_tree.data) + " with key: " + str(key) + " deleted."
                b_tree = None
            elif b_tree.left is not None and b_tree.right is None:
                temp = b_tree
                b_tree = b_tree.left
                print "Item: " + str(temp.data) + " with key: " + str(key) + " deleted."
                del temp
            elif b_tree.left is not None and b_tree.right is None:
                temp = b_tree
                b_tree = b_tree.right
                print "Item: " + str(temp.data) + " with key: " + str(key) + " deleted."
                del temp
            else:
                print "Item: " + str(b_tree.data) + " with key: " + str(key) + " deleted."
                curr = self.__min_value(b_tree.right)
                b_tree.data = curr.data
                if b_tree.right == curr:
                    b_tree.right = None
                else:
                    curr.parent.left = curr.right
        return b_tree

    def __min_value(self, b_tree):
        if b_tree.left is None:
            return b_tree
        else:
            return self.__min_value(b_tree.left)

    def __contains__(self, key):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> binary_tree.__contains__(1)
        False
        >>> binary_tree.__contains__(5)
        True
        """
        return self.__contains_key(self.root, key)

    def __contains_key(self, b_tree, key):
        if b_tree is None:
            return False
        elif key < b_tree.data[0]:
            return self.__contains_key(b_tree.left, key)
        elif key > b_tree.data[0]:
            return self.__contains_key(b_tree.right, key)
        else:
            return True

    def __len__(self):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__len__()
        0
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> binary_tree.__len__()
        1
        """
        return self.length

    def display(self):
        """
        >>> binary_tree = BinarySearchTreeDict()
        >>> binary_tree.__setitem__(5, "five")
        "(5, 'five') inserted"
        >>> binary_tree.__setitem__(3, "Three")
        "(3, 'Three') inserted"
        >>> binary_tree.__setitem__(7, "seven")
        "(7, 'seven') inserted"
        >>> binary_tree.display()
        In-order tree traversal keys: 3->5->7
        Pre-order tree traversal keys: 5->3->7
        """
        self.in_order_keys()
        self.pre_order_keys()


def terrible_hash(bin):
    """
    >>> terrible_hash(10)(1)
    10
    """
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.
    """

    def hashfunc(item):
        return bin

    return hashfunc


def main():
    print "---------------Single Link node---------------------\n"

    link_node1 = SinglyLinkedNode(5, None)
    link_node2 = SinglyLinkedNode(3, link_node1)

    print "Node data is: " + str(link_node2.item)
    print "Next Node is: " + str(link_node2.next)
    print "Node representation: " + str(link_node1.__repr__())

    print "\n---------------Linked List---------------------\n"

    single_linked_list = SinglyLinkedList()
    for i in range(0, 5):
        print single_linked_list.prepend(i)
    print "After adding elements: ", single_linked_list.__repr__()
    if single_linked_list.remove(3) == 1:
        print "element 3 removed"
    print "Removing element 3 from list: ", single_linked_list.__repr__()
    if single_linked_list.remove(4) == 1:
        print "element 4 removed"
    print "Removing element 4 from list: ", single_linked_list.__repr__()
    if single_linked_list.remove(0) == 1:
        print "element 0 removed"
    print "Removing element 0 from list: ", single_linked_list.__repr__()
    print "Does the list contain element 2: ", single_linked_list.__contains__(2)
    print "Does the list contain element 100: ", single_linked_list.__contains__(100)
    print "Length of single linked list: ", single_linked_list.__len__()
    print "Iterating single linked list: " + "->".join([str(item) for item in single_linked_list.__iter__()])

    print "\n---------------Binary Search Tree---------------------\n"

    tree_dictionary = BinarySearchTreeDict()

    print tree_dictionary.__setitem__(100, "hundred")
    print tree_dictionary.__setitem__(150, "one hundred and fifty")
    print "similarly other elements are inserted"
    tree_dictionary.__setitem__(50, "fifty")
    tree_dictionary.__setitem__(75, "Seventy five")
    tree_dictionary.__setitem__(60, "sixty")
    tree_dictionary.__setitem__(70, "seventy")
    tree_dictionary.__setitem__(5, "five")
    tree_dictionary.__setitem__(3, "three")
    tree_dictionary.__setitem__(7, "seven")
    tree_dictionary.__setitem__(4, "four")
    tree_dictionary.__setitem__(2, "two")
    tree_dictionary.__setitem__(6, "six")
    tree_dictionary.__setitem__(8, "eight")
    tree_dictionary.__setitem__(1, "one")
    tree_dictionary.__setitem__(0, "zero")

    tree_dictionary.in_order_keys()
    tree_dictionary.post_order_keys()
    tree_dictionary.pre_order_keys()

    tree_dictionary.items()

    print "size of the tree: ", tree_dictionary.__len__()

    print "Does tree contain item with key 250: ", tree_dictionary.__contains__(250)

    print "Does tree contain item with key 60: ", tree_dictionary.__contains__(60)

    tree_dictionary.__delitem__(60)

    print "Does tree contain item with key 60: ", tree_dictionary.__contains__(60)

    print "height of the binary search tree: ", tree_dictionary.height

    print "item corresponding to key 50 in the BST: ", tree_dictionary.__getitem__(50)

    tree_dictionary.display()

    print "---------------Chained Hash---------------------\n"

    chained_hash = ChainedHashDict(hashfunc=terrible_hash(5))
    print chained_hash.__setitem__(5, "five")
    print chained_hash.__setitem__(15, "fifteen")
    print "before rebuild"
    chained_hash.display()
    print "similarly other items are added"
    chained_hash.__setitem__(2, "two")
    chained_hash.__setitem__(1, "one")
    chained_hash.__setitem__(10, "ten")
    chained_hash.__setitem__(9, "nine")
    chained_hash.__setitem__(8, "eight")
    chained_hash.__setitem__(7, "seven")
    print "After rebuild"
    chained_hash.display()
    chained_hash.__delitem__(7)

    print "Load factor is: ", chained_hash.load_factor

    print "value retrieved for key = 5 is ", chained_hash.__getitem__(5)

    print "does chained hash contain item with key 7: ", chained_hash.__contains__(7)

    print "length of chained hash: ", chained_hash.__len__()

    print "Bin count: ", chained_hash.bin_count

    print "\n---------------open-address hashing---------------------\n"

    open_add_hashing = OpenAddressHashDict()
    print open_add_hashing.__setitem__(5, "five")
    print open_add_hashing.__setitem__(15, "fifteen")
    print "before rebuild"
    open_add_hashing.display()
    print "adding other items similarly"
    open_add_hashing.__setitem__(2, "two")
    open_add_hashing.__setitem__(1, "one")
    open_add_hashing.__setitem__(10, "ten")
    open_add_hashing.__setitem__(9, "nine")
    open_add_hashing.__setitem__(8, "eight")
    open_add_hashing.__setitem__(8, "eight")

    print "after rebuild"

    open_add_hashing.display()

    open_add_hashing.__delitem__(5)

    print "bin count: ", open_add_hashing.bin_count

    print "load factor: ", open_add_hashing.load_factor

    print "length of open address hash: ", open_add_hashing.__len__()

    print "value of item with key = 8 is ", open_add_hashing.__getitem__(8)

    print "does the hash table contain item with key = 10: ", open_add_hashing.__contains__(10)

if __name__ == '__main__':
    main()
    import doctest
    doctest.testmod()
