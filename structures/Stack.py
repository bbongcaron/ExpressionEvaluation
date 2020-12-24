##
#   A generic stack implementation.
#   
#   @author ru-nb-cs112
#   @translator Brenton Bongcaron
##
class Stack:

    ##
    #   Initializes stack to empty.
    ##
    def __init__(self):
        #
        #   Items in the stack.
        #
        self.__items = []

    ##
    #   Pushes a new item on top of stack
    #
    #   @param item Item to push.
    ##
    def push(self, item):
        self.__items.append(item)

    ##
    #   Pops item at top of stack and returns it.
    #
    #   @return Popped item
    ##
    def pop(self):
        if not self.__items:
            raise Exception("Can't pop from an empty stack")
        return self.__items.pop()

    ##
    #   Returns item on top of stack, without popping it.
    #
    #   @return Item at top of stack.
    ##
    def peek(self):
        if not self.__items:
            raise Exception("Can't peek on an empty stack")
        return self.__items[-1]
    
    ##
    #   Tells if stack is empty
    #
    #   @return True if stack is empty, False if not
    ##
    def isEmpty(self):
        if not self.__items:
            return True
        return False

    ##
    #   Returns number of items in stack.
    #
    #   @return Number of items in stack.
    ##
    def size(self):
        return len(self.__items)

    ##
    #   Empties the stack.
    ##
    def clear(self):
        self.__items.clear()
