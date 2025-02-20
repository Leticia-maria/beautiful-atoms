import bpy
from bpy.types import Panel
from bpy.props import (
    FloatVectorProperty,
    IntVectorProperty,
    FloatProperty,
    EnumProperty,
)
from batoms.render.render import Render
from batoms import Batoms

class Render_PT_prepare(Panel):
    bl_label = "Render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = "Batoms"
    bl_idname = "RENDER_PT_Tools"

    def draw(self, context):
        layout = self.layout
        repanel = context.scene.repanel

        layout = self.layout
        # row = col.row(align=True)
        layout.label(text="Camera")
        col = layout.column()
        col.prop(repanel, "viewport")
        col.label(text="Type")
        col.prop(repanel, "camera_type")
        if list(repanel.camera_type)[0] == 'ORTHO':
            layout.prop(repanel, "scale")
        else:
            layout.prop(repanel, "camera_lens")
            layout.prop(repanel, "distance")
        layout.prop(repanel, "resolution")
        layout.separator()
        layout.label(text="Light")
        col = layout.column()
        col.prop(repanel, "light_direction")
        layout.prop(repanel, "light_strength")



class RenderProperties(bpy.types.PropertyGroup):
    """
    """
    def Callback_modify_viewport(self, context):
        repanel = bpy.context.scene.repanel
        modify_render_attr(context, 'viewport', repanel.viewport)
    
    def Callback_modify_camera_type(self, context):
        repanel = bpy.context.scene.repanel
        modify_camera_attr(context, 'type', list(repanel.camera_type)[0])

    def Callback_modify_camera_lens(self, context):
        repanel = bpy.context.scene.repanel
        modify_camera_attr(context, 'lens', repanel.camera_lens)

    def Callback_modify_light_direction(self, context):
        repanel = bpy.context.scene.repanel
        modify_light_attr(context, 'direction', repanel.light_direction)

    def Callback_modify_light_strength(self, context):
        repanel = bpy.context.scene.repanel
        modify_light_attr(context, 'strength', repanel.light_strength)

    def Callback_modify_resolution(self, context):
        repanel = bpy.context.scene.repanel
        modify_render_attr(context, 'resolution', repanel.resolution)

    def Callback_modify_scale(self, context):
        modify_camera_attr(context, 'scale', context.scene.repanel.scale)

    def Callback_modify_distance(self, context):
        repanel = bpy.context.scene.repanel
        modify_render_attr(context, 'distance', repanel.distance)

    viewport: FloatVectorProperty(
        name="Viewport", size=3, default=(0, 0, 1),
        soft_min = -1, soft_max = 1,
        subtype = "XYZ",
        description="Miller viewport for the render", update=Callback_modify_viewport)
    
    camera_type: EnumProperty(
        name="Type",
        description="Structural models",
        items=(('ORTHO', "ORTHO", "ORTHO"),
               ('PERSP', "PERSP", "PERSP")),
        default={'ORTHO'},
        update=Callback_modify_camera_type,
        options={'ENUM_FLAG'},
    )

    resolution: IntVectorProperty(
        name="Resolution", size=2, default=(1000, 1000),
        soft_min = 100, soft_max = 2000,
        description="Miller resolution for the render", update=Callback_modify_resolution)
    
    scale: FloatProperty(
        name="Scale", default=10,
        soft_min = 1, soft_max = 100,
        description="scale", update=Callback_modify_scale)

    light_direction: FloatVectorProperty(
        name="Direction", size=3, default=(0, 0, 1),
        soft_min = -1, soft_max = 1,
        subtype = "XYZ",
        description="Light direction for the render", update=Callback_modify_light_direction)
    
    light_strength: FloatProperty(
        name="Strength", default=10,
        soft_min = 1, soft_max = 100,
        description="light_strength", update=Callback_modify_light_strength)

    distance: FloatProperty(
        name="Distance", default=3,
        description="distance from origin", update=Callback_modify_distance)

    camera_lens: FloatProperty(
        name="Lens", default=100,
        soft_min = 1, soft_max = 100,
        description="camera_lens", update=Callback_modify_camera_lens)


def modify_render_attr(context, key, value):
    from batoms.batoms import Batoms
    if context.object and context.object.batoms.type != 'OTHER':
        batoms = Batoms(label=context.object.batoms.label)
        setattr(batoms.render, key, value)
        if key not in ['distance']:
            batoms.render.init()
        context.space_data.region_3d.view_perspective = 'CAMERA'


def modify_light_attr(context, key, value):
    from batoms.batoms import Batoms
    if context.object and context.object.batoms.type != 'OTHER':
        batoms = Batoms(label=context.object.batoms.label)
        setattr(batoms.render.lights['Default'], key, value)
        batoms.render.init()
        context.space_data.region_3d.view_perspective = 'CAMERA'

def modify_camera_attr(context, key, value):
    from batoms.batoms import Batoms
    if context.object and context.object.batoms.type != 'OTHER':
        batoms = Batoms(label=context.object.batoms.label)
        if key == 'scale':
            batoms.render.camera.set_ortho_scale(value)
        elif key in ['lens']:
            setattr(batoms.render.camera, key, value)
        else:
            setattr(batoms.render.camera, key, value)
            batoms.render.init()
        context.space_data.region_3d.view_perspective = 'CAMERA'
