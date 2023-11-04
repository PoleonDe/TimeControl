import bpy
from threading import Timer

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

def InfiniteTimer():
    bpy.context.preferences.addons[__name__].preferences.totalOpenTime += 1.0
    bpy.context.scene.timecontrol_timer += 1.0
    print("TICK TOTAL" + str(bpy.context.preferences.addons[__name__].preferences.totalOpenTime))
    print("TICK SCENE" + str(bpy.context.scene.timecontrol_timer))
    return 1.0


def StartTimerWrapper():
    print("START WRAPPER")
    bpy.ops.timecontrol.start_timer()

class TIMECONTORL_start_timer(bpy.types.Operator):
    bl_idname = "timecontrol.start_timer"
    bl_label = "Start Time Control Timer"


    def execute(self, context):
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

# def draw_popover(self,context):
#     row : bpy.types.UILayout  = self.layout.row()
#     row = row.row(align=True)
#     row.operator('lightcontrol.adjust_light', text='Edit', icon='OUTLINER_OB_LIGHT',)

class TIMECONTROL_Addon_Preferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    # def showEditLightButtonUpdate(self,context):
    #     bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)
    #     if self.showEditLightButtonPanel:
    #         bpy.types.VIEW3D_MT_editor_menus.append(draw_popover)
            
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
    print("registered")
    for cls in classes:
        bpy.utils.register_class(cls)

    Timer(1, StartTimerWrapper, ()).start()

def unregister():
    global timerFunction
    if bpy.app.timers.is_registered(timerFunction):
        bpy.app.timers.unregister(timerFunction)

    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("unregistered")

    #bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)