"""
Configuration Scopes.
"""
from enum import Enum

class ConfigScope(str, Enum):
    GLOBAL = "GLOBAL"
    ENVIRONMENT = "ENVIRONMENT"
    MODULE = "MODULE"
    EXECUTION = "EXECUTION"
    EXPERIMENT = "EXPERIMENT"
    DEVELOPER = "DEVELOPER"
    OVERRIDE = "OVERRIDE"
