import os
import sys
from distutils.core import setup
import cx_Freeze

base = "Console"

executable = [
    cx_Freeze.Executable("swapper.py", base = base)
]

build_exe_options = {"includes":[],
                     "packages":["Tkinter", "FileDialog"],
                     "include_files":[]
                     }

cx_Freeze.setup(
    name = "DatabaseSwapper",
    options = {"build_exe": build_exe_options},
    version = "0.0",
    description = "standalone",
    executables = executable
)