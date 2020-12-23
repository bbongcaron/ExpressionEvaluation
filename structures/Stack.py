
class Stack:
    def __init__(self):
        self.__items = []
    
    def push(self, item):
        self.__items.append(item)
    
    def pop(self):
        if not self.__items:
            raise Exception("Can't pop from an empty stack")
        return self.__items.pop()

    def peek(self):
        if not self.__items:
            raise Exception("Can't peek on an empty stack")
        return self.__items[-1]
    
    def isEmpty(self):
        if not self.__items:
            return False
        return True

    def size(self):
        return len(self.__items)

    def clear(self):
        self.__items.clear()


#stack = Stack()
#stack.push(2)
#stack.push(12)
#stack.push(12)
#print(stack.pop())
#print(stack.size())
#print(stack.peek())
#stack.clear()
#print(stack.size())
#print(stack.peek())

