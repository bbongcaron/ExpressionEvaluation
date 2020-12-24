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
def evaluate(expression, vars, arrays):
    # Remove spaces from expression
    expr = expression.replace(" ", "")
    # PMDAS
    # Separate expr into a list of operators and FULL variable/array names
    tokenizedExpr = __tokenizeExpression(expr)

    # 
    # Attempt to scan for the deepest ()/[] pair and solve deepest ()/[] expression
    # 
    grouperPair = ()
    while __findGrouperPair(tokenizedExpr) is not None:
        # @grouperPair Tuplet representing indexOf start grouper ( | [ and end grouper ) | ]
        grouperPair = __findGrouperPair(tokenizedExpr)
        # @solvedExpr The solution to the deepest ()/[] expression w/__basicSolve()
        solvedExpr = __basicSolve(tokenizedExpr[grouperPair[0]+1:grouperPair[1]], vars, arrays)
        newTokenizedExpr = []
        substituted = False
        # Omit brackets & parenthesis when substituting (array indexes will be in position n+1),
        # where n is the index of the array name!)
        for i in range(0, len(tokenizedExpr)):
            if grouperPair[0] <= i <= grouperPair[1]:
                if not substituted:
                    newTokenizedExpr.append(str(solvedExpr))
                    substituted = True
            else:
                newTokenizedExpr.append(tokenizedExpr[i])
        tokenizedExpr = newTokenizedExpr

    # Basic solve of expression with no parenthesis & simplified bracket expressions
    return __basicSolve(tokenizedExpr, vars, arrays)
##
#   Basic solve of expression with no parenthesis & simplified bracket expressions
#
#   @param tokenizedExpr The tokenized expression
#   @param vars The list of Variable objects
#   @param arrays The list of Array objects
#   @return The solution to the basic expression
##
def __basicSolve(tokenizedExpr, vars, arrays):
    # No parenthesis are left: straight solve the expression
    # Create operator and value stacks
    operationStack = Stack()
    valueStack = Stack()
    for index, element in enumerate(tokenizedExpr):
        try:
            # try to straight push the element => works if element is an integer
            valueStack.push(int(element))
        except ValueError:
            # catching ValueError => element is either an Array/Variable Object or None
            if element is None:
                continue
            elif element in ('+', '-', '*', '/'):
                operationStack.push(element)
            else:
                # element is an Array or Variable
                found = False
                for var in vars:
                    if element == var.name:
                        valueStack.push(int(var.value))
                        found = True
                        break
                if not found:
                    for arr in arrays:
                        if element == arr.name:
                            # Element after Array name will be the index needed from Array Object
                            arrIndex = int(tokenizedExpr[index+1])
                            valueStack.push(int(arr.values[arrIndex]))
                            # Remove Array Object index so the index is not pushed into valueStack
                            tokenizedExpr[index+1] = None
                            found = True
                            break
    # Start popping operator stack and determining values
    while not operationStack.isEmpty():
        currentOp = operationStack.pop()
        num1 = valueStack.pop()
        while currentOp in ('+','-') and not operationStack.isEmpty() and operationStack.peek() in ('-','*','/'):
            num2 = valueStack.pop()
            num3 = valueStack.pop()
            if operationStack.peek() == '*':
                valueStack.push(num3 * num2)
            elif operationStack.peek() == '-':
                valueStack.push(num3 - num2)
            else: # operationStack.peek() == '/'
                valueStack.push(num3 / num2)
            operationStack.pop()
        num2 = valueStack.pop()
        if currentOp == '+':
            valueStack.push(num2 + num1)
        elif currentOp == '-':
            valueStack.push(num2 - num1)
        elif currentOp == '*':
            valueStack.push(num2 * num1)
        else:# currentOp == '/':
            valueStack.push(num2 / num1)
    return valueStack.pop()
##
#   Parenthesis/Bracket Turing Machine-Style scan to a single parenthesis pair
#
#   @param tokenizedExpr The tokenized expression
#   @return - None if no parenthesis are left in the expression
#           - otherwise a tuple representing a '(' ')' pair 
##
def __findGrouperPair(tokenizedExpr):
    closedGrouper = -1
    openGrouper = -1
    parsePointer = 0
    direction = "right"
    lastFound = ''
    # Turing machine halts when a single parenthesis/bracket pair is found
    while 0 <= parsePointer < len(tokenizedExpr) and direction != "halt":
        if direction == "right":
            if tokenizedExpr[parsePointer] == ')' or tokenizedExpr[parsePointer] == ']':
                closedGrouper = parsePointer
                direction = "left"
                lastFound = tokenizedExpr[parsePointer]
                parsePointer -= 1
            else:
                parsePointer += 1
        elif direction == "left":
            if lastFound == ')' and tokenizedExpr[parsePointer] == '(':  
                openGrouper = parsePointer
                direction = "halt"
                parsePointer += 1
            elif lastFound == ']' and tokenizedExpr[parsePointer] == '[':
                openGrouper = parsePointer
                direction = "halt"
                parsePointer += 1
            else:
                parsePointer -= 1
    if closedGrouper == -1 and openGrouper == -1:
        return None       
    return (openGrouper, closedGrouper)
##
#   Separate the expression into a list of operators and *full* variable names:
#   expr = variableX + (variableY) would be tokenized to:
#           ['variableX', '+', '(', 'variableY', ')']
#
#   @param expr The expression to be evaluated
#   @return The list containing tokenized expression
#
##
def __tokenizeExpression(expr):
    tokenizedExpr = []
    parsePointer = 0
    currentItem = ""
    while parsePointer < len(expr):
        if expr[parsePointer] in ('+', '-', '*', '/', '[', ']', '(', ')'):
            if currentItem:
                tokenizedExpr.append(currentItem)
            tokenizedExpr.append(expr[parsePointer])
            currentItem = ""
        else:
            currentItem += expr[parsePointer]
        parsePointer += 1
        if currentItem and parsePointer == len(expr):
            tokenizedExpr.append(currentItem)
    return tokenizedExpr