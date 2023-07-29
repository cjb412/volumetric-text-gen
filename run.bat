@echo off
COLOR 06

set blenderpath=C:\Program Files\Blender Foundation\Blender 3.6
echo [VTEXTGEN] Starting volumetric text generation...
start "" "%blenderpath%\blender.exe" --background --factory-startup --python volumetric_text_gen.py