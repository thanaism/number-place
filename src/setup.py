import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32" : base = "Win32GUI"

exe = Executable(script = "main.py", base= base)

setup(
    name = 'np_maker',
    version = '0.1', 
    description = 'converter',
    executables = [exe]
)