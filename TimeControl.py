import bpy

bl_info = {
    "name": "Time Control",
    "description": "A Tool That Tracks the Time you have a Blender File Open",
    "author": "Blendercontrol - Blendercontrol@gmail.com",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "Shortcuts : Shift E and E",
    "category": "Lighting" # TODO : Test if "Time"  is a Category
}


# def draw_popover(self,context):
#     row : bpy.types.UILayout  = self.layout.row()
#     row = row.row(align=True)
#     row.operator('lightcontrol.adjust_light', text='Edit', icon='OUTLINER_OB_LIGHT',)

class LIGHTCONTROL_Addon_Preferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    # def showEditLightButtonUpdate(self,context):
    #     bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)
    #     if self.showEditLightButtonPanel:
    #         bpy.types.VIEW3D_MT_editor_menus.append(draw_popover)
            

    currentTime: bpy.props.FloatProperty(
        name="File Open Time",
        description="Time this Blender is Open",
        default=0.0
    )

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout
        layout.label(text="File is open for: " + str(self.currentTime) + " Seconds")


#################################################################
####################### REGISTRATION ############################
#################################################################

classes = (LIGHTCONTROL_Addon_Preferences)


def register():
    print("registered")
    for cls in classes:
        bpy.utils.register_class(cls)

    #bpy.data.window_managers[0]["someProperty"]
    bpy.types.Scene.someProperty = bpy.props.FloatProperty(name="someProperty", description="bla bla", default=0.0)
    #if 'someProperty' in bpy.data.window_managers[0]:

    
    # spawnEffectTimer = 0.0
    # spawnEffectDuration = 0.4
    # spawnEffectTickTime = 0.033

    # def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
    #     # Addon Preferences
    #     preferences = context.preferences
    #     addon_prefs = preferences.addons[__name__].preferences

    #     def drawSpawnEffect():
    #         if self.spawnEffectTimer == 0:
    #             #DO SOMETHING ONCE
    #             pass

    #         #ON TICK UPDATE
    #         self.spawnEffectTimer += self.spawnEffectTickTime
    #         self.area3D.tag_redraw()

    #         if self.spawnEffectTimer >= self.spawnEffectDuration:
    #             # BREAK
    #             return None
    #         return self.spawnEffectTickTime

    #     # register drawEffect
    #     bpy.app.timers.register(drawSpawnEffect)

    #bpy.types.VIEW3D_MT_editor_menus.append(draw_popover)


def unregister():
    print("unregistered")
    for cls in classes:
        bpy.utils.unregister_class(cls)

    #bpy.types.VIEW3D_MT_editor_menus.remove(draw_popover)


if __name__ == "__main__":
    register()