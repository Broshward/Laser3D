# Laser3D
3D printer + Laser tree engraving module = PCB prototype machine.
This is project for add laser module to 3D printer without disassemble extruder for making PCB.
It contains shematics, pcb, 3D models and some utility for gcode 3D to laser translating.
Shematics and pcb has developed in Lepton EDA electronics softvare.
At the beginning of laser engraving make I try to follow of this instruction https://www.instructables.com/3D-Printer-Laser-Modification/
But it worked partially for me. Therefore I make as other :)

Laser_interfacer contains simple pcb for control Laser module throught the cooler model fan of 3D printer.
The Laser Holder 3D model you can find in 3D models repository: https://github.com/Broshward/3D_models

Approximate PCB prototyping process:
1. PCB develop in EDA.
2. Export cooper layers to pdf.
3. Convert pdf to svg.
4. Importing svg by openscad and making PCB 3D model for cooper image. Save to stl.
5. Slicing by Prusa-slicer cooper stl.
6. Using "to_laser_gcode.py" utility for converting filament gcode to Laser engraving gcode.
7. Using engraving gcode for engraving painted glass textolite on 3D printer.
8.  Pickling in ferric chloride or hydrogen peroxide.


License: Harmonies Worlds
