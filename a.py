import bpy
import math

# --- 初期化 ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# --- トーラス（土台） ---
bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), major_radius=0.8, minor_radius=0.2)
torus = bpy.context.object
torus.name = "Torus"

# --- 体（台形） ---
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=1.0, radius2=0.5, depth=2.0, location=(0, 0, 1.5))
body = bpy.context.object
body.name = "Body"

# --- 手（左右） ---
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.5, location=(-1.1, 0, 1.5))
left_arm = bpy.context.object
left_arm.name = "Left_Arm"
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.5, location=(1.1, 0, 1.5))
right_arm = bpy.context.object
right_arm.name = "Right_Arm"

# --- 頭（キューブ） ---
bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0, 0, 3.0))
head = bpy.context.object
head.name = "Head"

# --- ヒットボックス（攻撃判定） ---
bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, 0.7, 2.0))
hitbox = bpy.context.object
hitbox.name = "Hitbox"
hitbox.display_type = 'WIRE'
hitbox.show_in_front = True

# --- すべて選択して統合 ---
for obj in [torus, body, left_arm, right_arm, head, hitbox]:
    obj.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.join()
mesh = bpy.context.object
mesh.name = "CinderMesh"

# --- アーマチュア（ボーン）作成 ---
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
armature = bpy.context.object
armature.name = "CinderRig"
arm = armature.data

# ボーンを定義（トーラス→体→頭）
arm.edit_bones.remove(arm.edit_bones[0])  # デフォルトのボーン削除

# Bone1：Root（トーラス）
bone_root = arm.edit_bones.new("Root")
bone_root.head = (0, 0, 0)
bone_root.tail = (0, 0, 1)

# Bone2：Body
bone_body = arm.edit_bones.new("Body")
bone_body.head = (0, 0, 1)
bone_body.tail = (0, 0, 2)
bone_body.parent = bone_root

# Bone3：Head
bone_head = arm.edit_bones.new("Head")
bone_head.head = (0, 0, 2)
bone_head.tail = (0, 0, 3)
bone_head.parent = bone_body

bpy.ops.object.mode_set(mode='OBJECT')

# --- スキンバインド ---
mesh.select_set(True)
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# --- FBX出力（アーマチュア込み） ---
bpy.ops.export_scene.fbx(filepath="cinder.fbx", use_armature_deform_only=True)
