import json
import tkinter as tk
import tkinter.ttk as ttk

sets = {}

class Expression:
    def eval(self) -> set:
        raise NotImplementedError("Pure virtual method called.")
    
class Set(Expression):
    def __init__(self,set_name):
        super().__init__()
        self.set: set = sets[set_name]
        
    def eval(self):
        return self.set
    
class Union(Expression):
    def __init__(self,left:Expression, right:Expression):
        super().__init__()
        self.left:Expression = left
        self.right:Expression = right
        
    def eval(self):
        return self.left.eval() | self.right.eval()
    
class Intersection(Expression):
    def __init__(self,left:Expression, right:Expression):
        super().__init__()
        self.left:Expression = left
        self.right:Expression = right
        
    def eval(self):
        return self.left.eval() & self.right.eval()
    
class Difference(Expression):
    def __init__(self,left:Expression, right:Expression):
        super().__init__()
        self.left:Expression = left
        self.right:Expression = right
        
    def eval(self):
        return self.left.eval() - self.right.eval()
    
class SymmetricDifference(Expression):
    def __init__(self,left:Expression, right:Expression):
        super().__init__()
        self.left:Expression = left
        self.right:Expression = right
        
    def eval(self):
        return self.left.eval() ^ self.right.eval()
    
class LegendFrame(tk.Frame):
    
    def __init__(self,master):
        super().__init__(master)
        self.l0 = tk.Label(self,text="Set operations")
        self.l1 = tk.Label(self,text="a | b - union")
        self.l2 = tk.Label(self,text="a & b - intersection")
        self.l3 = tk.Label(self,text="a - b - difference")
        self.l4 = tk.Label(self,text="a ^ b - symmetric difference")
        
        self.l0.grid(row=0,column=0,padx=2,pady=2,sticky='ew')
        self.l1.grid(row=1,column=0,padx=2,pady=2,sticky='w')
        self.l2.grid(row=2,column=0,padx=2,pady=2,sticky='w')
        self.l3.grid(row=3,column=0,padx=2,pady=2,sticky='w')
        self.l4.grid(row=4,column=0,padx=2,pady=2,sticky='w')
        
        
class InputFrame(tk.Frame):
    
    def __init__(self,master,input_var,button_command,verbs):
        super().__init__(master)
        self.label = tk.Label(self,text="Input expression:")
        self.input = tk.Entry(self,textvariable=input_var)
        self.input_var:tk.StringVar = input_var
        self.verb_var = tk.StringVar(self)
        self.verb_cbox = ttk.Combobox(self,textvariable=self.verb_var,values=verbs,state='readonly')
        self.verb_cbox.current(0)
        self.verb_button = ttk.Button(self,text="Add verb",command=self.add_verb)
        self.eval_button = ttk.Button(self,text="Evaluate expression",command=button_command)

        self.columnconfigure([0,1], weight=1)
        self.label.grid(row=0,column=0,columnspan=2,padx=2,pady=2)
        self.input.grid(row=1,column=0,columnspan=2,padx=10,pady=2,sticky='ew')
        self.verb_cbox.grid(row=2,column=0,padx=2,pady=2,sticky='e')
        self.verb_button.grid(row=2,column=1,padx=2,pady=2,sticky='w')
        self.eval_button.grid(row=3,column=0,columnspan=2,padx=2,pady=2)
    
    def add_verb(self):
        self.input_var.set(self.input_var.get()+self.verb_var.get())

class ResultFrame(tk.Frame):
    
    def __init__(self,master):
        super().__init__(master)
        self.label = tk.Label(self,text="Result:")
        self.result = tk.Text(self,state='disabled')
        self.scroll = ttk.Scrollbar(self,command=self.result.yview)
        self.result['yscrollcommand'] = self.scroll.set
        
        self.rowconfigure(1,weight=1)
        self.label.grid(row=0,column=0,columnspan=2,padx=2,pady=2)
        self.result.grid(row=1,column=0,padx=2,pady=2)
        self.scroll.grid(row=1,column=1,sticky='ns')
        
    def show_result(self,result):
        self.result.config(state='normal')
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.INSERT, result)
        self.result.config(state='disabled')
        

def tokenize(s):
    tokens = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c in '()&|^-':
            tokens.append(c)
            i += 1
        elif c.isalpha():
            name = []
            while i < len(s) and s[i].isalpha():
                name.append(s[i])
                i += 1
            tokens.append(''.join(name))
        else:
            raise ValueError(f"Invalid character: {c}")
    return tokens

class ParseError(Exception):
    pass

def parse_expression(tokens):
    output = []
    op_stack = []
    precedence = {'-': 4, '&': 3, '^': 2, '|': 1}
    
    for token in tokens:
        if token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                output.append(op_stack.pop())
            if not op_stack:
                raise ParseError("Mismatched parentheses")
            op_stack.pop()
        elif token in precedence:
            while op_stack and op_stack[-1] != '(' and precedence[op_stack[-1]] >= precedence[token]:
                output.append(op_stack.pop())
            op_stack.append(token)
        else:
            output.append(token)
    
    while op_stack:
        op = op_stack.pop()
        if op == '(':
            raise ParseError("Mismatched parentheses")
        output.append(op)
    
    stack = []
    for token in output:
        if token in precedence:
            if len(stack) < 2:
                raise ParseError("Insufficient operands for operator " + token)
            right = stack.pop()
            left = stack.pop()
            if token == '&':
                node = Intersection(left, right)
            elif token == '|':
                node = Union(left, right)
            elif token == '-':
                node = Difference(left, right)
            elif token == '^':
                node = SymmetricDifference(left, right)
            else:
                raise ParseError("Unknown operator " + token)
            stack.append(node)
        else:
            stack.append(Set(token))
    
    if len(stack) != 1:
        raise ParseError("Invalid expression")
    return stack[0]

def eval_expression(expression):
    try:
        tokens = tokenize(expression)
        ast = parse_expression(tokens)
        result = ast.eval()
        return ", ".join(result)
    except Exception as e:
        return str(e)

# Przykład użycia
sets = {}
with open("verb_noun_pairs.json","r") as f:
    loaded_data = json.load(f)
    for k,v in loaded_data.items():
        sets[k] = set(v)

window = tk.Tk()
window.title("Verb analizer")

legendF = LegendFrame(window)
resultF = ResultFrame(window)
input_var = tk.StringVar(window)
inputF = InputFrame(window,input_var,lambda: resultF.show_result(eval_expression(input_var.get())),list(sets.keys()))

legendF.grid(row=0,column=0)
inputF.grid(row=1,column=0,sticky='ew')
resultF.grid(row=2,column=0)

window.mainloop()
