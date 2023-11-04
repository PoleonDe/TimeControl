import bpy
from threading import Timer
import random

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
    item = bpy.context.preferences.addons[__name__].preferences.sceneTimes.add()
    item.name = "randomName"
    item.id = "someID"
    item.time = 1231.2
    print("NEW ELEMENT " + str(item.time) + str(item.id))

    #something: bpy.types.FloatProperty = bpy.props.FloatProperty(name="")
    #something.g
    print([method_name for method_name in dir(bpy.context.preferences.addons[__name__].preferences.sceneTimes[0].time.__getattribute__)if callable(getattr(bpy.context.preferences.addons[__name__].preferences.sceneTimes[0].time.__getattribute__, method_name))])
    print(bpy.context.preferences.addons[__name__].preferences.sceneTimes[0].time.__getattribute__)

    # if "randomName" in bpy.context.preferences.addons[__name__].preferences.sceneTimes:
    #     print("IS FOUND")
    #     bpy.context.preferences.addons[__name__].preferences.sceneTimes["randomName"].time.set(1.0)
    #     print(bpy.context.preferences.addons[__name__].preferences.sceneTimes["randomName"].time)

    #     print("ACCESS " + str(bpy.context.preferences.addons[__name__].preferences.sceneTimes["randomName"].time))
    # else:
    #     print("NOT FOUND")

    # print("Scene Time Group = " + str(bpy.context.preferences.addons[__name__].preferences.sceneTimes))

    # for element in bpy.context.preferences.addons[__name__].preferences.sceneTimes:
    #     print(element)
    #     print(element.time)

    # someL : CustomGroup = None
    # someL.

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

class CustomGroup(bpy.types.PropertyGroup):
    id = bpy.props.StringProperty(name="someID", default="")
    time = bpy.props.FloatProperty(name = "someTime", default=0.0)

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
    
    sceneTimes: bpy.props.CollectionProperty(
        type = CustomGroup,
        name = "Scene Times", 
        description = "Saves all Scene Times"
    )
    

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout
        layout.label(text="Blender is open for: " + str(self.totalOpenTime) + " Seconds since registration of this Addon")
        for e in self.sceneTimes:
            layout.label(text=str(e.time))



#################################################################
####################### REGISTRATION ############################
#################################################################

classes = [CustomGroup,TIMECONTROL_Addon_Preferences]

def register():
    print("registered")
    for cls in classes:
        bpy.utils.register_class(cls)
    Timer(1, StartTimerFunc, ()).start()

def unregister():
    Timer(1, StopTimerFunc, ()).start()
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("unregistered")

    #bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)

if __name__ == "__main__":
    register()