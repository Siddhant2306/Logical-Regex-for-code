from Frontend.IR.Ir_nodes import *

class IRPrinter:
    def __init__(self):
        self.indent = 0

    def _p(self, text):
        print("  " * self.indent + text)

    def visit(self, node):
        if node is None:
            return
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        self._p(f"<unknown {node.__class__.__name__}>")

    # -------------------------
    # Module
    # -------------------------
    def visit_IRModule(self, node):
        for stmt in node.body:
            self.visit(stmt)

    # -------------------------
    # Function
    # -------------------------
    def visit_IRFunction(self, node):
        params = ", ".join(node.params)
        self._p(f"func {node.func_name}({params})")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1

    # -------------------------
    # Statements
    # -------------------------
    def visit_IRAssign(self, node):
        self._p(f"{self.expr(node.target)} = {self.expr(node.value)}")

    def visit_IRReturn(self, node):
        self._p(f"return {self.expr(node.value)}")

    def visit_IRIf(self, node):
        self._p(f"if {self.expr(node.test)}")
        self.indent += 1
        for stmt in node.then_body:
            self.visit(stmt)
        self.indent -= 1

        if node.else_body:
            self._p("else")
            self.indent += 1
            for stmt in node.else_body:
                self.visit(stmt)
            self.indent -= 1

    def visit_IRFor(self, node):
        self._p(f"for {self.expr(node.target)} in {self.expr(node.it)}")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1

    # -------------------------
    # Expressions
    # -------------------------
    def expr(self, node):
        if isinstance(node, IRVar):
            return node.name
        if isinstance(node, IRConst):
            return repr(node.value)
        if isinstance(node, IRBinary):
            return f"({self.expr(node.left)} {node.op} {self.expr(node.right)})"
        return "<expr>"
