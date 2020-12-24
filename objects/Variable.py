##
#   This class holds a (name, integer value) pair for a simple (non-array) variable.
#   The variable name is a sequence of one or more letters.
#
#   @author ru-nb-cs112
#   @translator Brenton Bongcaron
##
class Variable:
    ##
	#   Initializes with name, and zero value
	# 
	#   @param name Variable name
	##
    def __init__(self, name):
        #
        #   Name, sequence of letters
        #
        self.name = name
        #
        #   Integer value
        #
        self.value = 0
    
    def toString(self):
        return self.name + "=" + str(self.value)

    def equals(self, o):
        if not o or not isinstance(o, Variable):
            return False
        return self.name == o.name
