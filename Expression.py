import re
from objects.Array import Array
from objects.Variable import Variable
from structures.Stack import Stack

delims = "\\t|\\*|\\+|-|/|\\(|\\)|\\[|\\]| "

##
#   Populates the vars list with simple variables, and arrays lists with arrays
#   in the expression. For every variable (simple or array), a SINGLE instance is created 
#   and stored, even if it appears more than once in the expression.
#   At this time, values for all variables and all array items are set to
#   zero - they will be loaded from a file in the loadVariableValues method.
# 
#   @param expr The expression
#   @param vars The variables array list - already created by the caller
#   @param arrays The arrays array list - already created by the caller
##
def makeVariableLists(expr, vars, arrays):
    # Split expr with above delimiters
    splitItems = re.split(delims, expr)
    exprItems = []
    # Place non-null-character items from splitItems to exprItems
    for item in splitItems:
        if item != '':
            exprItems.append(item)
    # Indicates the last scanned character in the Turing Machine-esque algorithm
    parsePointer = 0
    for item in exprItems:
        indexOfItem = expr.index(item, parsePointer)
        # try-except block for handling errors when determining if item is an array
        try:
            if expr[indexOfItem + len(item)] == '[' and Array(item) not in arrays:
                # Check: char immediately after item in expr is a '[' => item is Array
                #        AND arrays does not contain Array object w/name item
                # Action: Intialize Array object w/name item & append to arrays list
                arrays.append(Array(item))
            elif not item.isdigit() and Variable(item) not in vars:
                # Check: item is not a number => item is Variable
                #        AND vars does not contain Variable object w/name item
                # Action: Intialize Variable object w/name item & append to vars list
                vars.append(Variable(item))
        # IndexError exception expected when scanning for [ goes outside str boundary
        except IndexError:
            # if exception is caught => item not an Array, still need Variable check
            if not item.isdigit() and Variable(item) not in vars:
                # Check: item is not a number => item is Variable
                #        AND vars does not contain Variable object w/name item
                # Action: Intialize Variable object w/name item & append to vars list
                vars.append(Variable(item))
        # update parsePointer to last scanned character of item
        parsePointer = indexOfItem + len(item)
##
#   Loads values for variables and arrays in the expression
#
#   @throws IOException If there is a problem with the input --- Java version
#   @param sc Scanner for values input
#   @param vars The Variables list - previously populated by makeVariableLists
#   @param arrays The Arrays list - previously populated by makeVariableLists
##
def loadVariableValues(file, vars, arrays):
    for line in file:
        tokenizer = re.split(" ", line.strip())
        # Assume that an Object with name tokenizer[0] DNE in vars & arrays at first
        varIndex = -1
        arrIndex = -1
        for vari in range(0, len(vars)):
            # Linear scan thru vars comparing Variable names w/input file names
            if vars[vari].name == tokenizer[0]:
                varIndex = vari
                break
        if varIndex == -1:
            # Only linear scan thru arrays if the Variable linear scan failed
            for arri in range(0, len(arrays)):
                if arrays[arri].name == tokenizer[0]:
                    arrIndex = arri
                    break
        if varIndex == -1 and arrIndex == -1:
            # Variable & Array linear scans failed => continue to next line in file
            continue
        if len(tokenizer) == 2:
            # Check: tokenizer containing 2 elements => item is a Variable
            # Action: Update var.value in vars
            vars[varIndex].value = tokenizer[1]
        else:
            # Otherwise: tokenizer contains >2 elements => item is an Array
            # arr is a *pointer* to the wanted Array Object in arrays!!
            arr = arrays[arrIndex]
            arr.values = [0] * int(tokenizer[1])
            for i in range(2, len(tokenizer)):
                # Scan thru input file (index,value) pairs
                arrTokenizer = re.split(" |\\(|\\,|\\)", tokenizer[i])
                arrItems = []
                # Transfer non-'' elements to arrItems - a (index,value) pair
                for item in arrTokenizer:
                    if item != '':
                        arrItems.append(item)
                # Transfer value in arrItems to index specified by arrItems
                arr.values[int(arrItems[0])] = int(arrItems[1])
##
#   Evaluates the expression.
# 
#   @param vars The variables array list, with values for all variables in the expression
#   @param arrays The arrays array list, with values for all array items
#   @return Result of evaluation
##
def evaluate(expr, vars, arrays):
    # expr = "3+(4*5)"
    # PMDAS
    #operationStack = Stack()
    #valueStack = Stack()
    closedParenthesis = []
    openParenthesis = []
    # Parenthesis Turing-Machine-Style scan
    parsePointer = 0
    direction = "right"
    while 0 <= parsePointer < len(expr):
        if direction == "right":
            if expr[parsePointer] == ')' and parsePointer not in closedParenthesis:
                closedParenthesis.append(parsePointer)
                direction = "left"
                parsePointer -= 1
            else:
                parsePointer += 1
        elif direction == "left":
            if expr[parsePointer] == '(' and parsePointer not in openParenthesis:  
                openParenthesis.append(parsePointer)
                direction = "right"
                parsePointer += 1
            else:
                parsePointer -= 1
        
    print(closedParenthesis)
    print(openParenthesis)
