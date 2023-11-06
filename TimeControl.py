import bpy
import blf
from threading import Timer
from math import floor
import os
import json
from bpy.app.handlers import persistent

bl_info = {
    "name": "Time Control",
    "description": "A Tool That Tracks the Time you have a Blender File Open",
    "author": "Blendercontrol - Blendercontrol@gmail.com",
    "version": (0, 8, 0),
    "blender": (3, 6, 0),
    "location": "Will automatically be triggered when Blender Starts",
    "category": "Time"
}

timerFunction = None
timerDrawHandler = None
area3D = None


def initializeTimeDataFile(context: bpy.types.Context):
    filepath = str(os.path.dirname(__file__)) + "\\timeData.json"

    if not os.path.exists(filepath):
        #file doesnt exist, create empty data
        data = {}
    else:
        #files does exist, read it
        with open(filepath, "r") as jsonFile:
            data = json.load(jsonFile)
        # If there is no data in the file
        if len(data) == 0:
            # create empty data
            data = {}

    #If current Scene is saved
    if bpy.data.is_saved:
        #If there is no current Scene time, create current Scene time
        currentFileName = str(bpy.path.basename(bpy.context.blend_data.filepath))
        if currentFileName in data:
            context.scene["timecontrol_timer"] = data[currentFileName]

    with open(filepath, "w") as jsonFile:
        json.dump(data,jsonFile)

def updateTimeDataFile(context: bpy.types.Context):
    filepath = str(os.path.dirname(__file__)) + "\\timeData.json"

    if os.path.exists(filepath):
        with open(filepath, "r") as jsonFile:
            data = json.load(jsonFile)

        data[str(bpy.path.basename(bpy.context.blend_data.filepath))] = context.scene["timecontrol_timer"]

        with open(filepath, "w") as jsonFile:
            json.dump(data,jsonFile)

def sumTimeDataFile() -> float:
    filepath = str(os.path.dirname(__file__)) + "\\timeData.json"

    if os.path.exists(filepath):
        with open(filepath, "r") as jsonFile:
            data = json.load(jsonFile)
        timeDataSum = 0.0
        for filename in data:
            timeDataSum += data[filename]
        return timeDataSum
    else:
        return 0.0

def secondsToHMS(seconds:float) -> str:
    secondsString:str = str(floor(seconds%60))
    minuitesString:str = str(floor((seconds/60)%60))
    hoursString:str = str(floor(seconds/3600))
    return hoursString + " h " + minuitesString + " m " + secondsString + " s"

def getFirst3DArea(context:bpy.types.Context) ->bpy.types.Area:
    if context == None:
        return None
    
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            return area
    return None

def InfiniteTimer():
    if "timecontrol_timer" in bpy.context.scene.keys():
        bpy.context.scene["timecontrol_timer"] += 1.0

    if bpy.data.is_saved:
        updateTimeDataFile(bpy.context)

    global area3D
    if area3D == None:
        area3D = getFirst3DArea(bpy.context)
    else:
        area3D.tag_redraw()

    return 1.0

def drawTimeNumber():
    font_id: int = 0
    position = (5.0,10.0)
    size = 10
    blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
    blf.size(font_id,size)
    
    textTotalTime = secondsToHMS(sumTimeDataFile())
    blf.position(font_id, position[0],position[1], 0.0)
    blf.draw(font_id, textTotalTime)
    if "timecontrol_timer" in bpy.context.scene.keys():
        textSceneTime = secondsToHMS(bpy.context.scene["timecontrol_timer"]) # TODO: Scene has no Attribute ?!
        blf.position(font_id, position[0], position[1] + size + 5, 0.0)
        blf.draw(font_id, textSceneTime)

def StartTimerWrapper():
    bpy.ops.timecontrol.start_timer()

class TIMECONTORL_start_timer(bpy.types.Operator):
    bl_idname = "timecontrol.start_timer"
    bl_label = "Start Time Control Timer"


    def execute(self, context):
        global timerDrawHandler
        if timerDrawHandler == None:
            args = ()
            timerDrawHandler = bpy.types.SpaceView3D.draw_handler_add(drawTimeNumber, args, 'WINDOW', 'POST_PIXEL')

        if "timecontrol_timer" not in context.scene.keys():
            bpy.types.Scene.timecontrol_timer = bpy.props.FloatProperty(name="timecontrol_timer", description="Mouse Position when Pie Menu was Initialized",default=0.0)
            context.scene["timecontrol_timer"] = 0.0

        initializeTimeDataFile(context)

        global timerFunction
        if bpy.app.timers.is_registered(timerFunction): # return if already registered
            return {'FINISHED'}

        timerFunction = InfiniteTimer
        bpy.app.timers.register(function=timerFunction,persistent=True)
        return {'FINISHED'}

class TIMECONTORL_stop_timer(bpy.types.Operator):
    bl_idname = "timecontrol.stop_timer"
    bl_label = "Stop Time Control Timer"

    def execute(self, context):
        global timerFunction
        if bpy.app.timers.is_registered(timerFunction):
            bpy.app.timers.unregister(timerFunction)
        return {'FINISHED'}

# TODO: Reload when Opening a new file.
class TIMECONTROL_Addon_Preferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__
            
    timeData: bpy.props.StringProperty(
        name="",
        description="",
        subtype="DIR_PATH",
        default= str(os.path.dirname(__file__)) + "\\timeData.json"
    )

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout
        layout.label(text="Directory to Time Data Save File")
        layout.prop(self, "timeData")


#################################################################
####################### REGISTRATION ############################
#################################################################
classes = [TIMECONTORL_start_timer, TIMECONTORL_stop_timer, TIMECONTROL_Addon_Preferences]
# TODO: When using Save as, reset Timer - Dont use Scene Property, make global variable and only store by Filename.

@persistent
def unregisterHandlers(dummy):
    print("unregister Handler:", bpy.data.filepath)
    global timerFunction
    if bpy.app.timers.is_registered(timerFunction):
        bpy.app.timers.unregister(timerFunction)
        timerFunction = None

    global timerDrawHandler
    if timerDrawHandler != None:
       bpy.types.SpaceView3D.draw_handler_remove(timerDrawHandler, 'WINDOW')
       timerDrawHandler = None
    global area3D
    area3D = None

@persistent
def registerHandlers(dummy):
    print("register Handler:", bpy.data.filepath)
    Timer(1, StartTimerWrapper, ()).start()

def register():
    bpy.app.handlers.load_pre.append(unregisterHandlers)
    bpy.app.handlers.load_post.append(registerHandlers)
    for cls in classes:
        bpy.utils.register_class(cls)
    Timer(1, StartTimerWrapper, ()).start()
    print("registered")


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    unregisterHandlers()
