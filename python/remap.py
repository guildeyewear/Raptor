from stdglue import *
from interpreter import *
from emccanon import MESSAGE
import linuxcnc, hal
import hal_racktoolchange
import time

params = {
        "RACK_POSITION_X": 0,
        "RACK_POSITION_Y": 0,
        "POCKET_SEPARATION_X": 75,
        "POCKET_SEPARATION_Y": 75,
        "ROWS": 2,
        "COLUMNS": 7,
        "DROP_HEIGHT": -100,
        "DROP_SPEED": 500,
        "GRAB_HEIGHT": -105,
        "TRAVERSE_HEIGHT": -70,
        "PDB_CODE": "P1",
        "BLOW_CODE": "P2",
        "TOOL_RELEASE_CODE": "P1",
        "TOOL_SECURE_CODE": "P0",
        "Z_RETRACT_SPEED": 2000
        }

def spindle_off(self):
    self.execute("M5")

def quill_up(self):
    self.execute("G53 G1 Z0 F%i" % params["Z_RETRACT_SPEED"])

def move_to_pocket(self, pocket):
    pocket = int(pocket)
    print 'moving to pocket %i' % pocket
    x_pos = (pocket / params["COLUMNS"])*params["POCKET_SEPARATION_X"] + params["RACK_POSITION_X"]
    y_pos = (pocket % params["COLUMNS"])*params["POCKET_SEPARATION_Y"] + params["RACK_POSITION_Y"]
    print 'calculated coords %i, %i' % (x_pos, y_pos)
    self.execute("G53 G1 X%i Y%i F%i" % (x_pos, y_pos, params["Z_RETRACT_SPEED"]))
    print 'moved to correct pocket'

def clean_tool(self):
    print 'cleaning tool'
    self.execute("M62 %s" % (params["BLOW_CODE"]))
    time.sleep(1.5)
    self.execute("M63 %s" % (params["BLOW_CODE"]))
    print 'done cleaning'

def drop_tool(self, tool):
    print 'dropping tool %i' % tool
    move_to_pocket(self, tool)
    print 'Moving to dropoff height'
    self.execute("G53 G1 Z%i F%i" % (params["DROP_HEIGHT"], params["DROP_SPEED"]))
    print 'moved'
    # drop tool
    self.execute("M62 %s" % (params["PDB_CODE"]))
    self.execute("G53 G1 Z%i F%i" % (params["TRAVERSE_HEIGHT"], params["DROP_SPEED"]))

def pickup_tool(self, tool):
    print 'picking up tool %i' % tool
    move_to_pocket(self, tool)

    print 'Moving to pickup height'
    self.execute("G53 G1 Z%i F%i" % (params["DROP_HEIGHT"], params["DROP_SPEED"]))
    print 'moved'
    # Make sure we're open
    self.execute("M64 %s" % (params["PDB_CODE"]))
    self.execute("M64 %s" % (params["BLOW_CODE"]))
    print 'waiting for tool release'
    self.execute("M66 %s" % (params["TOOL_RELEASE_CODE"]))
    print 'released'
    time.sleep(2)
    self.execute("M65 %s" % (params["BLOW_CODE"]))
    self.execute("G53 G1 Z%i F%i" % (params["GRAB_HEIGHT"], params["DROP_SPEED"]))
    self.execute("M65 %s" % (params["PDB_CODE"]))
    print 'waiting for tool grab'
    self.execute("M66 %s" % (params["TOOL_SECURE_CODE"]))
    print 'grabbed'
    time.sleep(1)
    quill_up(self)

def toolchange(self):
    current_pos = (self.current_x, self.current_y, self.current_z)
    current_tool = self.current_tool
    requested_tool = self.selected_tool
    print "current, requested:", current_tool, requested_tool

    if self.selected_pocket < 0:
        self.set_errormsg("M6: no tool prepared")
        yield INTERP_ERROR
    if self.cutter_comp_side:
        self.set_errormsg("Cannot change tools with cutter radius compensation on")
        yield INTERP_ERROR

    spindle_off(self)
    quill_up(self)

    current_pos = (self.current_x, self.current_y, self.current_z)
    current_tool = self.current_tool
    requested_tool =  self.selected_tool
    print current_pos, current_tool, requested_tool

    if current_tool >= 0:
        drop_tool(self, current_tool)
    if(requested_tool >= 0):
        pickup_tool(self, requested_tool)


    emccanon.CHANGE_TOOL(self.selected_pocket)
    self.current_pocket = self.selected_pocket
    self.selected_pocket = -1
    self.selected_tool = -1
    self.set_tool_parameters()
    self.toolchange_flag = True
    yield INTERP_EXECUTE_FINISH


def dump(obj):
    for attr in dir(obj):
        if hasattr( obj, attr ):
            print( "obj.%s = %s" % (attr, getattr(obj, attr)))
