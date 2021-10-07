import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {"includes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "simple_Tkinter",
    version = "0.1",
    description = "Sample cx_Freeze Tkinter script",
    executables = [Executable("GUI.py", base = base)])
