import re
from objects.Array import Array
from objects.Variable import Variable

delims = "\\t|\\*|\\+|-|/|\\(|\\)|\\[|\\]| "

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
        var = Variable(tokenizer[0])
        arr = Array(tokenizer[0])
        varIndex = -1
        arrIndex = -1
        for vari in range(0, len(vars)):
            if vars[vari].name == tokenizer[0]:
                varIndex = vari
                break
        if varIndex == -1:
            for arri in range(0, len(arrays)):
                if arrays[arri].name == tokenizer[0]:
                    arrIndex = arri
                    break
        if varIndex == -1 and arrIndex == -1:
            continue

        if len(tokenizer) == 2:
            # Check: tokenizer containing 2 elements => item is a Variable
            # Action: Update var.value in vars
            vars[varIndex].value = tokenizer[1]
        else:
            # Otherwise: tokenizer contains >2 elements => item is an Array
            arr = arrays[arrIndex]
            arr.values = [0] * int(tokenizer[1])
            for i in range(2, len(tokenizer)):
                arrTokenizer = re.split(" |\\(|\\,|\\)", tokenizer[i])
                arrItems = []
                for item in arrTokenizer:
                    if item != '':
                        arrItems.append(item)
                arr.values[int(arrItems[0])] = int(arrItems[1])


