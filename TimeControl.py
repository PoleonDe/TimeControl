import bpy
import time
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
    print("TICK " + str(bpy.context.preferences.addons[__name__].preferences.totalOpenTime))
    return 1.0

def StartTimerFunc():
    print("START")
    global timerFunction
    timerFunction = InfiniteTimer
    bpy.app.timers.register(timerFunction)

def StopTimerFunc():
    print("STOP")
    global timerFunction
    print("timer function is : " + str(timerFunction))
    if bpy.app.timers.is_registered(timerFunction):
        print("is Registered")
    else:
        print("is Not Registered")
    bpy.app.timers.unregister(timerFunction)

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

def register():
    print("registered")
    bpy.utils.register_class(TIMECONTROL_Addon_Preferences)
    Timer(1, StartTimerFunc, ()).start()

def unregister():
    Timer(1, StopTimerFunc, ()).start()
    bpy.utils.unregister_class(TIMECONTROL_Addon_Preferences)
    print("unregistered")

    #bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)

if __name__ == "__main__":
    register()