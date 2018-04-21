import sys
import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\Susan\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Susan\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

cx_Freeze.setup(
    name = "Catapult Simulator",
    options = { "build_exe": {
                "packages": ["pygame"], 
                "include_files": [],
            } },
    executables = [cx_Freeze.Executable("CatapultSimulator.py")]
)