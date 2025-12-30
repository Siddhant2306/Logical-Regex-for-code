"""
Mutation and aliasing tracking
"""

import ast
from typing import Dict, Set


class MutationTracker:
    """Tracks mutations and aliasing"""
    
    def __init__(self, symbol_table, mutated_vars, aliases):
        self.symbol_table = symbol_table
        self.mutated_vars = mutated_vars
        self.aliases = aliases
    
    def track_alias(self, target: str, source: str):
        """Track when variables become aliases"""
        if source not in self.aliases:
            self.aliases[source] = {source}
        if target not in self.aliases:
            self.aliases[target] = set()
        
        self.aliases[source].add(target)
        self.aliases[target] = self.aliases[source]
        
        if target in self.symbol_table:
            self.symbol_table[target].aliases = self.aliases[target]
        if source in self.symbol_table:
            self.symbol_table[source].aliases = self.aliases[source]
    
    def has_aliases(self, var_name: str) -> bool:
        """Check if variable has aliases"""
        return var_name in self.aliases and len(self.aliases[var_name]) > 1
    
    def handle_method_call(self, node: ast.Call):
        """Track mutations from method calls"""
        if isinstance(node.func, ast.Attribute):
            method = node.func.attr
            
            # Mutating methods
            if method in ['append', 'extend', 'remove', 'pop', 'sort', 'reverse', 'clear']:
                if isinstance(node.func.value, ast.Name):
                    var_name = node.func.value.id
                    self.mutated_vars.add(var_name)
                    
                    if var_name in self.symbol_table:
                        self.symbol_table[var_name].mutations.append(method)


