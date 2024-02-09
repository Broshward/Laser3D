#!/usr/bin/python2

import sys,os
help='''
usage: %s [--laser-on cmd] [--laser-off cmd] [--layers-count N] [--height-bias H] file.gcode
    
    This program translating 3D printer gcode for laser engraving module.

    Options:
        --laser-on cmd      Determine the laser module switch on gcode command. 
                            Default it desribes the "laser_on" variable (See source below).
        --laser-off cmd     Similarly --laser-on, but for switch off laser module.
        --layers-count N    Leaves only N top Layers from file.
                            Default value on the layers_count variable.
        -h H                It lifts laser module to H millimeters from bot for begin engraving height. Default 40.
                            Default value is described the "engraving_height_bias" variable.
        -o file             Output gcode filename. Defaulting add "_laser" to input filename.
''' %(sys.argv[0])

engraving_height_bias = 40  # mm. Height laser tool upon engaving surface. It Height of laser focus point
layers_count=1
laser_on='M106 S0'
laser_of='M106 S255'


if '--laser-on' in sys.argv:
    ind=sys.argv.index('--laser-on')
    laser_on = sys.argv[ind+1]
    sys.argv = sys.argv[:ind]+sys.argv[ind+2:]
if '--laser-off' in sys.argv:
    ind=sys.argv.index('--laser-off')
    laser_off = sys.argv[ind+1]
    sys.argv = sys.argv[:ind]+sys.argv[ind+2:]
if '--layers-count' in sys.argv:
    ind=sys.argv.index('--layers-count')
    layers_count = int(sys.argv[ind+1])
    sys.argv = sys.argv[:ind]+sys.argv[ind+2:]
if '-h' in sys.argv:
    ind=sys.argv.index('-h')
    engraving_height_bias = eval(sys.argv[ind+1])
    sys.argv = sys.argv[:ind]+sys.argv[ind+2:]
else:
    engraving_height_bias = 40
if '-o' in sys.argv:
    ind=sys.argv.index('-o')
    output = sys.argv[ind+1]
    sys.argv = sys.argv[:ind]+sys.argv[ind+2:]
if '--help' in sys.argv:
    print help
    exit(0)


print_gcode_beg = '; Filament gcode'
print_gcode_end = ';END gcode for filament'
h_mark = ';Z:'

begin_actions = '''G21 ;metric values
G90 ;absolute positioning
M117 Homing X/Y ...
G28 X0 Y0 ; Home X,Y 
M117 Homing Height ...
G28 Z0 ; Home height
'''
end_actions='''%s
G90 ;Absolute positionning
G1 Y200 F3000 ;Present print
M84 ;steppers off
;M300 P300 S4000
M117 Finished.
''' %(laser_of)

def off(): #laser on function
    global laser_of, on_off
    on_off=0
    return laser_of+'\n'

def on(): #laser on function
    global laser_on, on_off
    on_off=1
    return laser_on+'\n'

print_gcode = open(sys.argv[1]).read()
print_gcode = print_gcode.split(print_gcode_beg,1)[1].split(print_gcode_end,1)[0]
print_gcode = print_gcode.split('\n')
lines_count = len(print_gcode)
laser_layers = [''] # list of strings for laser engraving layers. One string for one layer
on_off=0 #Disabling laser in launch
#import pdb; pdb.set_trace()
count=0
layer=0
for i in print_gcode:
    if i.startswith('M107') or i.startswith('M106'): # Ignoring fan 
        continue 
    elif i.startswith(h_mark): #The layer change
        laser_layers.insert(0,'') # When your print is printing, his extruder tool moving from bottom to top layer by layer. And when your 3D printer is engraving by laser module, his engrave tool are moving from top to bottom ;)
        layer+=1
    elif i.startswith('G1'):
        if 'E' in i: # The extruder are working, this is print
            if on_off == 0: # The laser is off
                laser_layers[0] += on()
            i = i.split('E',1)[0].strip() # Remove Extruder moving
        else: # This is moving without print
            if on_off == 1: 
                laser_layers[0] += off()
        if 'Z' in i: # Add biasing for height
            g1 = i.split('Z',1)
            try:
                h,g1[1] = g1[1].split(None,1)
            except:
                h=g1[1]
                g1[1]=''
            h = eval(h) + engraving_height_bias
            i = g1[0] + 'Z%.2f ' %(h) + g1[1]

    
    print '\rContinuing: %d%%' %(100*count/lines_count),
    laser_layers[0] += i+'\n'
    count+=1
    if 'layers_count' in globals():
        if layer>layers_count:
            break
    #import pdb; pdb.set_trace()

laser_layers.insert(0,off()+begin_actions)
laser_layers.append(off()+end_actions)

laser_gcode = '\n'.join(laser_layers) 
if 'output' in globals():
    outfile=open(output,'w')
else:
    outfile=open(sys.argv[1].rsplit('.',1)[0]+'_laser.'+sys.argv[1].rsplit('.',1)[1], 'w')
outfile.write(laser_gcode)
outfile.close()



        

