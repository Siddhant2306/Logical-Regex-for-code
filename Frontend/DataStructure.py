from dataclasses import dataclass, field
from typing import List, Set, Optional
from enum import Enum

class VariableType(Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    LIST = "list"
    DICT = "dict"
    SET = "set"
    TUPLE = "tuple"
    BOOL = "bool"
    NONE = "none"
    CUSTOM_CLASS = "custom"
    UNKNOWN = "unknown"
    FUNCTION = "function"

class MemoryEffect(Enum):
    STACK = "stack"              
    HEAP_UNIQUE = "heap_unique"  
    HEAP_SHARED = "heap_shared"  
    HEAP_GC = "heap_gc"          
    REFERENCE = "reference"

@dataclass
class VariableInfo:
 
    name: str
    var_type: VariableType
    element_type: Optional[VariableType] = None 
    scope: str = "global"
    is_mutable: bool = True
    is_parameter: bool = False
    is_reassigned: bool = False
    first_assignment_line: Optional[int] = None
    usage_lines: List[int] = field(default_factory=list)
    aliases: Set[str] = field(default_factory=set)  
    mutations: List[str] = field(default_factory=list)


@dataclass
class FunctionInfo:
    name: str
    parameters: List[VariableInfo]
    return_type: Optional[VariableType]
    modifies_params: Set[str] = field(default_factory=set) 
    has_side_effects: bool = False
    calls_functions: List[str] = field(default_factory=list)

@dataclass
class TypeConstraint:
    variable: str
    constraint_type: VariableType
    reason: str  
    confidence: float = 1.0 