#!/usr/bin/python

import sys, io, time
import gettext
import linuxcnc, hal

# These libraries not found - copied from stdglue.py
#import emccanon
#from interpreter import *


# Magic numbers snooped from stdglue.py
# TODO replace with proper imported references
#INTERP_ERROR = 5
#INTERP_OK = 0
#
#rack_params = {
#        "RACK_POSITION_X": 0,
#        "RACK_POSITION_Y": 0,
#        "POCKET_SEPARATION_X": 75,
#        "POCKET_SEPARATION_Y": 75,
#        "ROWS": 2,
#        "COLUMNS": 7,
#        "DROP_HEIGHT": -100,
#        "GRAB_HEIGHT": -105,
#        "PDB_CODE": "P2",
#        "BLOW_CODE": "P1",
#        "Z_RETRACT_SPEED": 2000
#        }
#
#def move_to_pocket(interpreter, pocket):
#    pocket = int(pocket)
#    print 'moving to pocket %i' % pocket
#    x_pos = (pocket / rack_params["COLUMNS"])*rack_params["POCKET_SEPARATION_X"] + rack_params["RACK_POSITION_X"]
#    y_pos = (pocket % rack_params["COLUMNS"])*rack_params["POCKET_SEPARATION_Y"] + rack_params["RACK_POSITION_Y"]
#    print 'calculated coords %i, %i' % (x_pos, y_pos)
#    interpreter.execute("G53 G1 X%i Y%i F%i" % (x_pos, y_pos, rack_params["Z_RETRACT_SPEED"]))
#
#
#
#def drop_tool(interpreter, tool):
#    print 'dropping tool %i' % tool
#    move_to_pocket(intepreter, tool)
#
#def pickup_tool(interpreter, tool):
#    print 'picking up tool %i' % tool
#    move_to_pocket(interpreter, tool)
#
#    interpreter.execute("G53 G1 Z%i F%i" % (rack_params["DROP_HEIGHT"], rack_params["DROP_SPEED"]))
#    interpreter.execute("M64 %s" % (rack_params["PDB_COLD"]))
H = None
def setup_pins():
    global H
    H = hal.component("hal_racktoolchange")
    H.newpin("toolnumber", hal.HAL_S32, hal.HAL_IN)
    H.newpin("change", hal.HAL_BIT, hal.HAL_IN)
    H.newpin("changed", hal.HAL_BIT, hal.HAL_OUT)
    H.newpin("spindle_stopped", hal.HAL_BIT, hal.HAL_IN)
    H.newpin("tool_secure", hal.HAL_BIT, hal.HAL_IN)
    H.newpin("tool_released", hal.HAL_BIT, hal.HAL_IN)
    H.newpin("drawbar", hal.HAL_BIT, hal.HAL_OUT)
    H.newpin("blow", hal.HAL_BIT, hal.HAL_OUT)
    return H

#def spindle_off(interpreter):
#    print("turning spindle off")
#    interpreter.execute("M5")
#
#def quill_up(interpreter):
#    print 'executing quill up'
#    interpreter.execute("G53 G1 Z0 F%i" % rack_params["Z_RETRACT_SPEED"])
#
#def toolchange(interpreter):
#    print 'interpreter selected pocket:', interpreter.selected
#    if interpreter.selected_pocket < 0:
#        interpreter.set_errormsg("M6: No tool prepared.")
#        return INTERP_ERROR
#    if interpreter.cutter_comp_side:
#        interpreter.set_errormsg("Cannot change tools with cutter radius compensation on")
#        return INTERP_ERROR
#
#
#    spindle_off(interpreter)
#    quill_up(interpreter)
#
#    current_pos = (interpreter.current_x, interpreter.current_y,interpreter.current_z)
#    current_tool = interpreter.current_tool
#    requested_tool =  interpreter.selected_tool
#    print current_pos, current_tool, requested_tool
#
#    if current_tool >= 0:
#        drop_tool(interpreter, current_tool)
#    if(requested_tool >= 0):
#        pickup_tool(interpreter, requested_tool)
#
#    # commit change
#    intepreter.selected_pocket =
#    j
#    return 1


