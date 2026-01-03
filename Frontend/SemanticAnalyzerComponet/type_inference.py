
import ast
from typing import Tuple, Optional
from Frontend.DataStructure import VariableType


class TypeInferencer:
    """Handles all type inference logic"""
    
    def __init__(self, symbol_table, mutated_vars):
        self.symbol_table = symbol_table
        self.mutated_vars = mutated_vars
    
    def infer_type(self, node: ast.AST) -> Tuple[VariableType, Optional[VariableType]]:
        """
        Infer type from an expression
        Returns: (type, element_type)
        """
        # Literals
        if isinstance(node, ast.Constant):
            return self._infer_constant_type(node)
        
        # Collections
        elif isinstance(node, ast.List):
            return self._infer_list_type(node)
        elif isinstance(node, ast.Dict):
            return VariableType.DICT, None
        elif isinstance(node, ast.Set):
            return VariableType.SET, None
        elif isinstance(node, ast.Tuple):
            return VariableType.TUPLE, None
        
        # Function/method calls
        elif isinstance(node, ast.Call):
            return self._infer_call_type(node)
        
        # Binary operations
        elif isinstance(node, ast.BinOp):
            left_type, _ = self.infer_type(node.left)
            return left_type, None
        
        # Variable reference
        elif isinstance(node, ast.Name):
            return self._infer_name_type(node)
        
        return VariableType.UNKNOWN, None
    
    def _infer_constant_type(self, node: ast.Constant) -> Tuple[VariableType, None]:
        """Infer type from constant literal"""
        if isinstance(node.value, bool):
            return VariableType.BOOL, None
        elif isinstance(node.value, int):
            return VariableType.INT, None
        elif isinstance(node.value, float):
            return VariableType.FLOAT, None
        elif isinstance(node.value, str):
            return VariableType.STRING, None
        elif node.value is None:
            return VariableType.NONE, None
        return VariableType.UNKNOWN, None
    
    def _infer_list_type(self, node: ast.List) -> Tuple[VariableType, Optional[VariableType]]:
        """Infer type from list literal"""
        if node.elts:
            elem_type, _ = self.infer_type(node.elts[0])
            return VariableType.LIST, elem_type
        return VariableType.LIST, VariableType.UNKNOWN
    
    def _infer_call_type(self, node: ast.Call) -> Tuple[VariableType, Optional[VariableType]]:
        """Infer return type of function calls"""
        
        # Built-in functions
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            builtin_types = {
                'input': (VariableType.STRING, None),
                'int': (VariableType.INT, None),
                'float': (VariableType.FLOAT, None),
                'str': (VariableType.STRING, None),
                'list': (VariableType.LIST, VariableType.UNKNOWN),
                'dict': (VariableType.DICT, None),
                'set': (VariableType.SET, None),
                'len': (VariableType.INT, None),
                'range': (VariableType.LIST, VariableType.INT),
            }
            
            return builtin_types.get(func_name, (VariableType.UNKNOWN, None))
        
        # Method calls
        elif isinstance(node.func, ast.Attribute):
            return self._infer_method_type(node)
        
        return VariableType.UNKNOWN, None
    
    def _infer_method_type(self, node: ast.Call) -> Tuple[VariableType, Optional[VariableType]]:
        """Infer return type of method calls"""
        method = node.func.attr
        
        # String methods
        if method == 'split':
            return VariableType.LIST, VariableType.STRING
        elif method in ['upper', 'lower', 'strip', 'replace', 'join']:
            return VariableType.STRING, None
        
        # List methods that return None (modify in-place)
        elif method in ['append', 'extend', 'remove', 'pop', 'sort', 'reverse']:
            if isinstance(node.func.value, ast.Name):
                self.mutated_vars.add(node.func.value.id)
            return VariableType.NONE, None
        
        return VariableType.UNKNOWN, None
    
    def _infer_name_type(self, node: ast.Name) -> Tuple[VariableType, Optional[VariableType]]:
        """Infer type from variable reference"""
        if node.id in self.symbol_table:
            var_info = self.symbol_table[node.id]
            return var_info.var_type, var_info.element_type
        return VariableType.UNKNOWN, None