# Frontend/SemanticAnalyzer/__init__.py
"""
Semantic Analyzer - Main Entry Point
"""

import ast
from typing import Dict, List, Set, Optional

from Frontend.DataStructure import (
    VariableInfo, FunctionInfo, TypeConstraint,
    VariableType, MemoryEffect
)
from .type_inference import TypeInferencer
from .variable_tracker import VariableTracker
from .function_analyzer import FunctionAnalyzer
from .control_flow_analyzer import ControlFlowAnalyzer
from .mutation_tracker import MutationTracker
from .memory_analyzer import MemoryAnalyzer
from Explain.Report import ReportGenerator


class SemanticAnalyzer(ast.NodeVisitor):
    """Main semantic analyzer"""
    
    def __init__(self):
        # Data storage
        self.symbol_table: Dict[str, VariableInfo] = {}
        self.functions: Dict[str, FunctionInfo] = {}
        self.type_constraints: List[TypeConstraint] = []
        self.mutated_vars: Set[str] = set()
        self.aliases: Dict[str, Set[str]] = {}
        self.loop_variables: Set[str] = set()
        
        # Context
        self.current_scope_name = "global"
        self.current_function: Optional[str] = None
        self.scope_stack: List[str] = ["global"]
        
        # Initialize all components
        self.type_inferencer = TypeInferencer(self.symbol_table, self.mutated_vars)
        
        self.variable_tracker = VariableTracker(
            self.symbol_table,
            self.type_constraints,
            lambda: self.current_scope_name,
            self.type_inferencer
        )
        
        self.function_analyzer = FunctionAnalyzer(
            self.symbol_table,
            self.functions,
            self.mutated_vars
        )
        
        self.control_flow_analyzer = ControlFlowAnalyzer(
            self.symbol_table,
            self.loop_variables
        )
        
        self.mutation_tracker = MutationTracker(
            self.symbol_table,
            self.mutated_vars,
            self.aliases
        )
        
        self.memory_analyzer = MemoryAnalyzer(
            self.symbol_table,
            self.mutated_vars,
            self.loop_variables,
            lambda var: self.mutation_tracker.has_aliases(var)
        )
        
        self.report_generator = ReportGenerator(
            self.symbol_table,
            self.functions,
            self.aliases,
            self.mutated_vars,
            self.type_constraints
        )
    
    # Visitor methods
    def visit_Assign(self, node: ast.Assign):
        self.variable_tracker.handle_assign(node, self.mutation_tracker)
        self.generic_visit(node)
    
    def visit_AugAssign(self, node: ast.AugAssign):
        self.variable_tracker.handle_aug_assign(node, self.mutated_vars)
        self.generic_visit(node)
    
    def visit_Name(self, node: ast.Name):
        self.variable_tracker.handle_name_usage(node)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        func_name = node.name
        self.current_function = func_name
        self.current_scope_name = f"function:{func_name}"
        self.scope_stack.append(self.current_scope_name)
        
        self.function_analyzer.handle_function_def(
            node, lambda: self.current_scope_name, self.type_inferencer
        )
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.function_analyzer.finalize_function(func_name)
        
        self.scope_stack.pop()
        self.current_scope_name = self.scope_stack[-1]
        self.current_function = None
    
    def visit_Return(self, node: ast.Return):
        self.function_analyzer.handle_return(
            node, self.current_function, self.type_inferencer
        )
        self.generic_visit(node)
    
    def visit_For(self, node: ast.For):
        self.control_flow_analyzer.handle_for_loop(
            node, lambda: self.current_scope_name, self.type_inferencer
        )
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.control_flow_analyzer.exit_loop()
    
    def visit_While(self, node: ast.While):
        self.control_flow_analyzer.handle_while_loop(node)
        self.generic_visit(node)
        self.control_flow_analyzer.exit_loop()
    
    def visit_If(self, node: ast.If):
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call):
        self.function_analyzer.handle_call(node, self.current_function)
        self.mutation_tracker.handle_method_call(node)
        self.generic_visit(node)
    
    # PUBLIC API - These are the methods users call
    def analyze_memory_effects(self):
        """Analyze memory effects for all variables"""
        self.memory_analyzer.analyze_all()
    
    def generate_report(self) -> str:
        """Generate analysis report"""
        return self.report_generator.generate_report()