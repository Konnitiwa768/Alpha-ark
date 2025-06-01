import bpy
import math

# すべてのオブジェクトを削除
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# トーラス（足元）
bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0))

# 体（台形：円錐 frustum風）
bpy.ops.mesh.primitive_cone_add(
    vertices=4,
    radius1=1.0,  # 下の半径
    radius2=0.5,  # 上の半径
    depth=2.0,
    location=(0, 0, 1.5)
)

# 手（棒）
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.1,
    depth=1.5,
    location=(-1.1, 0, 1.5)
)
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.1,
    depth=1.5,
    location=(1.1, 0, 1.5)
)

# 頭（立方体）
bpy.ops.mesh.primitive_cube_add(
    size=0.8,
    location=(0, 0, 3.0)
)

# FBXとしてエクスポート
bpy.ops.export_scene.fbx(filepath="cinder.fbx")
