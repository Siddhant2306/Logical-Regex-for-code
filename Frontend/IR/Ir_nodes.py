class IRnode():
    pass

class IRModule(IRnode):
    def __init__(self, body):
        self.body = body

class IRFunction(IRnode):
    def __init__(self, func_name , params , body):
        self.func_name = func_name
        self.params = params
        self.body = body

class IRAssign(IRnode):
    def __init__(self, target , value):
        self.target = target
        self.value = value

class IRVar(IRnode):
    def __init__(self, name):
        self.name = name  

class IRConst(IRnode):
    def __init__(self, value):
        self.value = value

class IRBinary(IRnode):
    def __init__(self,op, left, right):
        self.op = op
        self.left = left
        self.right = right

class IRFor(IRnode):
    def __init__(self, target , it , body):
        self.target = target
        self.it = it
        self.body = body

class IRIf(IRnode):
    def __init__(self, test, then_body, else_body):
        self.test = test
        self.then_body = then_body
        self.else_body = else_body

class IRReturn(IRnode):
    def __init__(self, value):
        self.value = value
