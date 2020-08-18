from Tree import Tree
from Readfile import readText

class TruthTable(Tree):
    def __init__(self,expression):
        self.expression = expression
        self.operant = {}
        self.expression_tree = None
        self.operator_step = []
        super().__init__(self.expression)


    def calculateRecursive(self,node,col = 0):
     

        if type(node) == str :
            return node
        else:
            a,b,out  = None ,None,None
            if node.left :
                a = self.calculateRecursive(node.left) 
            
            if node.right:
                b  =self.calculateRecursive(node.right) 

            if a and b:
                if (node.root == '+'):
                    out = str(int(a) |  int(b))

                elif (node.root == '&'):
                    out = str(int(a) &  int(b))
                
                self.operator_step.append(out)
                return out
            elif a:
                out = str(self.notBitwise(int(a)))
                self.operator_step.append(out)
                return out
            elif b :
                out = str(self.notBitwise(int(b)))
                self.operator_step.append(out)
                return out

    

    def calculateFormatRecursive(self,node):
        if type(node) == str :
            return node
        else:
            a,b = None ,None
            if node.left :
                a = self.calculateFormatRecursive(node.left) 
            
            if node.right:
                b  =self.calculateFormatRecursive(node.right) 

            if a and b:
                out = a+node.root+b
                self.operator_step.append(out)
                return out
            elif a:
                out = node.root+a
                self.operator_step.append(node.root+a)
                return out
            elif b :
                out = node.root+b
                self.operator_step.append(node.root+b)
                return out
            

    def notBitwise(self,input_value):
        if input_value == 0:
            return 1
        else:
            return 0

    def isOperator(self, c):
        return (c == '&') or (c == '+') or (c == '!')


                
    def showTable(self):
        postfix_list = self.infixToPostfix()
        for node in postfix_list:
            if not self.isOperator(node) and node not in self.operant and node not in '01' :
                self.operant[node] = None
        
        prob = 2**len(self.operant)

        self.expression_tree = self.postfixToExpressionTree(postfix_list)
        self.calculateFormatRecursive(self.expression_tree)


        eqnlen_list = []

        for keys in self.operant:
            print("| "+keys+" |",end = '')

        for eqn in self.operator_step:
            print("| "+eqn+" |",end = '')
            eqnlen_list.append( len(eqn) +1)

        # print(eqnlen_list)

        for rows in range (prob):
            self.operator_step = []
            truth_list = postfix_list.copy()
            index_dict = 1
            print()
            for keys in self.operant:
                
                self.operant[keys] = str((rows >> len(self.operant) - index_dict) % 2)
                for index_list in range(len(truth_list)):
                    if keys == truth_list[index_list]:
                        truth_list[index_list]  = self.operant[keys] 
                
                print('|  ' + self.operant[keys] +' |',end = '')
                index_dict +=1
         
            self.expression_tree = self.postfixToExpressionTree(truth_list)

           
            self.calculateRecursive(self.expression_tree)


            for index_eqn in range(len(self.operator_step)):
                    front = eqnlen_list[index_eqn] //2
                    back = (eqnlen_list[index_eqn]-front)
                    front_space,back_space = ' '*front,' '* back
                    print('|'+front_space + self.operator_step[index_eqn] + back_space+'|',end = '')
              
            



if __name__ == "__main__":

    text_addr = r"D:\Desktop_D\Kmutnb_Cpre\Software\2020-08-05\problem2\Expression.txt"
    expression = readText(text_addr)
    
    print("\n"+"-"*150)
    print("\n"+"-"*150)
    

    for string in expression:
        print("Expression : "+ string)
        print()
        Table = TruthTable(string)
        Table.showTable()
        print("\n"+"-"*150)
        print("\n"+"-"*150)
        print() 
