import ast
from Frontend.IR.Ir_nodes import *
class IRBuilder(ast.NodeVisitor):

    def build(self, tree):
        return self.visit(tree)
    
    def visit_Module(self, node):
        body = [self.visit(stmt) for stmt in node.body]
        return IRModule(body)

    def visit_FunctionDef(self, node):
        params = [arg.arg for arg in node.args.args]
        body = [self.visit(stmt) for stmt in node.body]
        return IRFunction(node.name, params, body)

    def visit_Assign(self, node):
        target = self.visit(node.targets[0])
        value = self.visit(node.value)
        return IRAssign(target, value)

    def visit_Name(self, node):
        return IRVar(node.id)

    def visit_Constant(self, node):
        return IRConst(node.value)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = type(node.op).__name__
        return IRBinary(op, left, right)

    def visit_If(self, node):
        test = self.visit(node.test)
        then_body = [self.visit(stmt) for stmt in node.body]
        else_body = [self.visit(stmt) for stmt in node.orelse]
        return IRIf(test, then_body, else_body)

    def visit_For(self, node):
        target = self.visit(node.target)
        iterable = self.visit(node.iter)
        body = [self.visit(stmt) for stmt in node.body]
        return IRFor(target, iterable, body)

    def visit_Return(self, node):
        value = self.visit(node.value) if node.value else None
        return IRReturn(value)
