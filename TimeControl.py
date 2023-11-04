import bpy
import blf
from threading import Timer
from math import floor

bl_info = {
    "name": "Time Control",
    "description": "A Tool That Tracks the Time you have a Blender File Open",
    "author": "Blendercontrol - Blendercontrol@gmail.com",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "Will automatically be triggered when Blender Starts",
    "category": "Time"
}

timerFunction = None
timerDrawHandler = None
area3D = None


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
    bpy.context.preferences.addons[__name__].preferences.totalOpenTime += 1.0
    bpy.context.scene.timecontrol_timer += 1.0
    # print("TICK TOTAL" + str(bpy.context.preferences.addons[__name__].preferences.totalOpenTime))
    # print("TICK SCENE" + str(bpy.context.scene.timecontrol_timer))

    global area3D
    if area3D == None:
        area3D = getFirst3DArea(bpy.context)
    else:
        area3D.tag_redraw()

    return 1.0

def drawTimeNumber(context:bpy.types.Context):
    font_id: int = 0
    textTotalTime = secondsToHMS(context.preferences.addons[__name__].preferences.totalOpenTime)
    textSceneTime= secondsToHMS(context.scene.timecontrol_timer)
    blf.color(font_id, 1.0, 1.0, 1.0, 1.0)

    position = (5.0,10.0)
    size = 10
    blf.size = size
    blf.position(font_id, position[0],position[1], 0.0)
    blf.draw(font_id, textTotalTime)
    blf.position(font_id, position[0],position[1] + size+5, 0.0)
    blf.draw(font_id, textSceneTime)

def StartTimerWrapper():
    bpy.ops.timecontrol.start_timer()

class TIMECONTORL_start_timer(bpy.types.Operator):
    bl_idname = "timecontrol.start_timer"
    bl_label = "Start Time Control Timer"


    def execute(self, context):
        global timerDrawHandler
        if timerDrawHandler == None:
            args = (bpy.context,)
            timerDrawHandler = bpy.types.SpaceView3D.draw_handler_add(drawTimeNumber, args, 'WINDOW', 'POST_PIXEL')

        global timerFunction
        if bpy.app.timers.is_registered(timerFunction): # return if already registered
            return {'FINISHED'}
        
        if "timecontrol_timer" not in context.scene.keys():
            bpy.types.Scene.timecontrol_timer = bpy.props.FloatProperty(name="timecontrol_timer", description="Mouse Position when Pie Menu was Initialized",default=0.0)
            context.scene["timecontrol_timer"] = 0.0

        timerFunction = InfiniteTimer
        bpy.app.timers.register(timerFunction)
        return {'FINISHED'}

class TIMECONTORL_stop_timer(bpy.types.Operator):
    bl_idname = "timecontrol.stop_timer"
    bl_label = "Stop Time Control Timer"

    def execute(self, context):
        global timerFunction
        if bpy.app.timers.is_registered(timerFunction):
            bpy.app.timers.unregister(timerFunction)
        return {'FINISHED'}

class TIMECONTROL_Addon_Preferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__
            
    totalOpenTime: bpy.props.FloatProperty(
        name="File Open Time",
        description="Time this Blender is Open",
        default=0.0
    )

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout
        layout.label(text="Blender is open for: " + str(self.totalOpenTime) + " Seconds since registration of this Addon")



#################################################################
####################### REGISTRATION ############################
#################################################################

classes = [TIMECONTORL_start_timer, TIMECONTORL_stop_timer, TIMECONTROL_Addon_Preferences]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    Timer(1, StartTimerWrapper, ()).start()

def unregister():
    global timerFunction
    if bpy.app.timers.is_registered(timerFunction):
        bpy.app.timers.unregister(timerFunction)

    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    global timerDrawHandler
    if timerDrawHandler != None:
        bpy.types.SpaceView3D.draw_handler_remove(timerDrawHandler, 'WINDOW')