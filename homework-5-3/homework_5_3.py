# Time Complexity : O(n)
# Space Complexity : O(1)


class Node:
    # функция для инициализации объекта элемента
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    # фукция инициализации
    def __init__(self):
        self.head = None

    # функция для перестроения связанного списка
    def reverse(self):
        prev = None
        current = self.head
        while current is not None:
            next = current.next
            current.next = prev
            prev = current
            current = next
        self.head = prev

    # фунуция для вставки нового элемента в начале
    def push(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node

    # функция для печати связанного списка
    def print_list(self):
        temp = self.head
        while temp:
            print(temp.data, end=' ')
            temp = temp.next

# Пример
llist = LinkedList()
llist.push(1)
llist.push(2)
llist.push(3)
llist.push(4)

print("Given Linked List")
llist.print_list()
llist.reverse()
print("\nReversed Linked List")
llist.print_list()
