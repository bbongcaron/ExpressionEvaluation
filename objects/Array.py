##
#   This class holds a (name, array of integers values) pair for an array.
#   The name is a sequence of one or more letters.
#
#   @author ru-nb-cs112
#   @translator Brenton Bongcaron
##
class Array:
    ##
    #   Initializes with name, and sets values to null.
    #
    #   @param name Name of array
    ##
    def __init__(self, name):
        ##
        #   Name, sequence of letters
        ##
        self.name = name
        ##
        #   Array of integer values
        ##
        self.values = []
    
    def toString(self):
        if not self.values:
            return self.name + "=[ ]"
        arrayStr = ""
        arrayStr += self.name
        arrayStr += "=["
        arrayStr += str(self.values[0])
        for i in range(1, len(self.values)):
            arrayStr += ","
            arrayStr += str(self.values[i])
        arrayStr += "]"
        return arrayStr

    def equals(self, o):
        if not o or not isinstance(o, Array):
            return False
        return self.name == o.name
