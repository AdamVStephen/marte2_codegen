"""
Main entry point for the `marte2_codegen` command.

The code in this module is also a good example of how to use MARTe2 codegen as a
library rather than a script.
"""
import logging
import os
from marte2_codegen.marte2_codegen import codegen

def marte2_codegen():
    codegen()

