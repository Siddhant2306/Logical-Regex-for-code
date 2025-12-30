"""
Memory effect analysis
Determines memory management strategy
"""

from Frontend.DataStructure import MemoryEffect, VariableType


class MemoryAnalyzer:
    """Analyzes memory effects and determines management strategy"""
    
    def __init__(self, symbol_table, mutated_vars, loop_variables, alias_checker):
        self.symbol_table = symbol_table
        self.mutated_vars = mutated_vars
        self.loop_variables = loop_variables
        self.alias_checker = alias_checker
    
    def analyze_all(self):
        """Analyze memory effects for all variables"""
        for var_name, var_info in self.symbol_table.items():
            memory_effect = self._determine_memory_effect(var_name, var_info)
            var_info.memory_effect = memory_effect
    
    def _determine_memory_effect(self, var_name: str, var_info) -> MemoryEffect:
        """Determine how this variable should be managed in C++"""
        
        # Check for aliasing (multiple references)
        if self.alias_checker(var_name):
            return MemoryEffect.HEAP_SHARED
        
        # Check if parameter that gets mutated
        if var_info.is_parameter and var_name in self.mutated_vars:
            return MemoryEffect.REFERENCE
        
        # Simple primitive types on stack
        if var_info.var_type in [VariableType.INT, VariableType.FLOAT, 
                                  VariableType.BOOL, VariableType.STRING]:
            return MemoryEffect.STACK
        
        # Loop variables on stack
        if var_name in self.loop_variables:
            return MemoryEffect.STACK
        
        # Complex types without aliases
        if var_info.var_type in [VariableType.LIST, VariableType.DICT, VariableType.SET]:
            if not self.alias_checker(var_name):
                return MemoryEffect.STACK
        
        return MemoryEffect.HEAP_GC

