import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    'python3',
    '-m', 'PyInstaller',
    'src/native.py', # your main file with ui.run()
    '--name', 'sonoscontroller', # name of your app
    # '--onefile',
    '--windowed', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    '--strip'
]
subprocess.call(cmd)
