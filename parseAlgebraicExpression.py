import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

class BinaryTree: 
    def __init__(self, valueExpression : str, separatorList: list[str]) -> None:

        self.value, charNumber, separatorList = parseOnce(valueExpression, separatorList)

        if charNumber != None: 
            self.type = "operand"
            self.left = BinaryTree(valueExpression[:charNumber], separatorList)
            self.right = BinaryTree(valueExpression[charNumber+1:], separatorList)
            return None

        functionName = ""
        charNumber = 0
        
        while charNumber < len(valueExpression) and valueExpression[charNumber] != "(":
            functionName += valueExpression[charNumber]
            charNumber += 1

        del charNumber

        if functionName == valueExpression:
            self.type = "immediate"
            #Can be a variable too, verify that later (Remember 0x ; 0b)
        elif not functionName: # Parentheses here 
            self.__init__(valueExpression[1:len(valueExpression)-1], ["^&|", "+-", "*%/"])

        else: # Functions here
            self.type = "function"

        if self.type in ["function", "immediate"]: # Says No sons must be created (avoid errors)
            self.left = self.right = None

def parseOnce(valueExpression: str,separatorList: list[str]):
    while separatorList:

        stringIsOpen = parenthesesIsOpen = False
        charThatOpenedString = ""
        openedParenthesesNumber = 0

        for charNumber, charValue in enumerate(valueExpression):
            
            if not stringIsOpen and charValue in ["'", '"']: #Try " \"\' "
                charThatOpenedString = charValue
                stringIsOpen = True
            
            elif stringIsOpen and charValue == charThatOpenedString: stringIsOpen = False

            if not stringIsOpen and charValue == "(":
                if parenthesesIsOpen: openedParenthesesNumber += 1
                else: parenthesesIsOpen, openedParenthesesNumber = True, 1

            elif not stringIsOpen and parenthesesIsOpen and charValue == ")":
                openedParenthesesNumber += -1
                if openedParenthesesNumber == 0: parenthesesIsOpen = False

            if not parenthesesIsOpen and not stringIsOpen and charValue in separatorList[0]:
                return charValue, charNumber, separatorList
        
        separatorList = separatorList[1:]

    return valueExpression, None, []

root = BinaryTree("5*(5+8*6)-(3+2*4-5)*4", ["^&|", "+-", "*%/"])

##############################################################
### (ChatGPT Code to show the binary tree using Matplotlib ###
##############################################################

def plot_tree(node, x, y, ax, parent=None, horizontal_pos=0, level=1, spacing=1):
    if node:
        ax.text(x, y, str(node.value), style='italic', ha='center', va='center', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 3})
        if parent is not None:
            ax.add_artist(FancyArrowPatch((parent[0], parent[1]), (x, y), arrowstyle='->', color='black'))
        next_level = level + 1
        if node.left:
            plot_tree(node.left, x - spacing, y - spacing, ax, parent=(x, y), horizontal_pos=-1, level=next_level, spacing=spacing/1.5)
        if node.right:
            plot_tree(node.right, x + spacing, y - spacing, ax, parent=(x, y), horizontal_pos=1, level=next_level, spacing=spacing/1.5)

fig, ax = plt.subplots(figsize=(10, 10))
plot_tree(root, 0, 0, ax, spacing=0.3)
ax.set_aspect('equal')
ax.axis('off')
plt.show()
