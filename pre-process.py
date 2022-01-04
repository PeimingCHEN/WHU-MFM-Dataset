import bpy
import os
from mathutils import Vector, Matrix
import collections
import random
import shutil
from math import pi

def delete_objects():
    for obj in bpy.context.scene.objects:
         if obj.type == 'MESH' and obj.name != 'Camera' and obj.name != 'Camera.001' and obj.name!='Plane' and obj.name!='studio_Corner' and obj.name!='stone_table' and obj.name!='wooden_table' and obj.name!='glass_table' and obj.name!='noble_table' and obj.name!='umbrella_white' and obj.name!='umbrella_yellow' and obj.name!='beam_light' and obj.name!='softbox' and obj.name!='studioL' and obj.name!='Spot':
             obj.select_set(True)
         else:
             obj.select_set(False)
    bpy.ops.object.delete()
    for block in bpy.data.meshes:
        if not block.users:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if not block.users:
            bpy.data.materials.remove(block)
    for block in bpy.data.textures:
        if not block.users:
            bpy.data.textures.remove(block)
    for block in bpy.data.images:
        if not block.users:
            bpy.data.images.remove(block)
            
def merge_mesh():
    #Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
         if obj.type == 'MESH' and obj.name != 'Camera' and obj.name != 'Camera.001' and obj.name!='Plane' and obj.name!='studio_Corner' and obj.name!='stone_table' and obj.name!='wooden_table' and obj.name!='glass_table' and obj.name!='noble_table' and obj.name!='umbrella_white' and obj.name!='umbrella_yellow' and obj.name!='beam_light' and obj.name!='softbox' and obj.name!='studioL' and obj.name!='Spot':
             obj.select_set(True)
             bpy.context.view_layer.objects.active = obj
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    mesh = bpy.context.selected_objects
    return mesh[0]
    
def takeX(elem):
    return elem[0]

def takeY(elem):
    return elem[1]

def takeZ(elem):
    return elem[2]

def rotate_mesh(mesh):
    bpy.context.object.rotation_mode = 'XYZ'
    #rotate mesh
    #X
    box = [mesh.matrix_world @ Vector(v) for v in mesh.bound_box]
    box.sort(key=takeZ)
    Z_face = box[0:4]
    Z_face.sort(key=takeY)
    a,b = Z_face[0:2]
    X_vector = a-b
    X_axis = Vector([1.0, 0.0, 0.0])
    angle = X_vector.angle(X_axis, 0)
    axis = X_axis.cross(X_vector)
    euler = Matrix.Rotation(angle, 4, axis).to_euler()
    mesh.rotation_euler[0] += euler[0]
    mesh.rotation_euler[1] += euler[1]
    mesh.rotation_euler[2] += euler[2]
    #Y
    box = [mesh.matrix_world @ Vector(v) for v in mesh.bound_box]
    box.sort(key=takeZ)
    Z_face = box[0:4]
    Z_face.sort(key=takeX)
    a,b = Z_face[0:2]
    Y_vector = a-b
    Y_axis = Vector([0.0, 1.0, 0.0])
    angle = Y_vector.angle(Y_axis)
    axis = Y_axis.cross(Y_vector)
    euler = Matrix.Rotation(angle, 4, axis).to_euler()
    mesh.rotation_euler[0] += euler[0]
    mesh.rotation_euler[1] += euler[1]
    mesh.rotation_euler[2] += euler[2]
    #Z
    box = [mesh.matrix_world @ Vector(v) for v in mesh.bound_box]
    box.sort(key=takeX)
    X_face = box[0:4]
    X_face.sort(key=takeY)
    a,b = X_face[0:2]
    if a[2]>b[2]:
        Z_vector = a-b
    else:
        Z_vector = b-a
    Z_axis = Vector([0.0, 0.0, 10.0])
    angle = Z_vector.angle(Z_axis, 0)
    print(angle)
    mesh.rotation_euler[2] += (pi * angle / 180)
    return mesh

def move_mesh(mesh):
    #move mesh
    box = [mesh.matrix_world @ Vector(v) for v in mesh.bound_box]
    box.sort(key=takeZ)
    a,b,c,d = box[0:4]
    bottom = (a+b+c+d)/4
    mesh.location -= bottom
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    return mesh

def scale_mesh(mesh):
    #adjust scale
    s = random.uniform(0.15, 0.2) / mesh.dimensions[2]
    mesh.scale = mesh.scale*s
    return mesh
                

file_path = "./mesh/"
unprocessed = 0
for file in os.listdir(file_path):
    if 'unprocessed' in file:
         unprocessed += 1

file_num = len(os.listdir(file_path)) - unprocessed

for file in os.listdir(file_path):
    if 'unprocessed' in file:
        lst_ply = os.listdir(file_path + file)
        for item in lst_ply:
            fileName, fileExtension = os.path.splitext(item)
            if fileExtension == ".gltf":
                flag = False
                bpy.ops.import_scene.gltf(filepath=os.path.join(file_path , file , item))
                mesh = merge_mesh()
                if len(mesh.data.materials[0].node_tree.links)==1:
                    flag = True
                else:
                   for i in range(len(mesh.data.materials[0].node_tree.links)):
                       flag = True
                       if mesh.data.materials[0].node_tree.links[i].to_node.name == 'Principled BSDF':
                           flag = False
                           break
                for i in range(len(mesh.data.materials)):                                      
                    for j in range(len(mesh.data.materials[i].node_tree.nodes)):
                        if mesh.data.materials[i].node_tree.nodes[j].name == 'Emission':
                            flag = True
                            break
                    if flag:
                        break
                if flag:
                    shutil.rmtree(os.path.join(file_path , file))
                    break
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                
                mesh = rotate_mesh(mesh)
                mesh = move_mesh(mesh)
                mesh = scale_mesh(mesh)
                mesh.name = str(file_num)
                mesh.data.name = str(file_num)
                for obj in bpy.context.scene.objects:
                    obj.select_set(False)
                bpy.data.objects[str(file_num)].select_set(True)
                bpy.ops.export_scene.gltf(export_format='GLTF_EMBEDDED', export_selected=True, use_selection=True, filepath=os.path.join(file_path , file , item))
                os.rename(os.path.join(file_path, file),os.path.join(file_path,str(file_num)))
                file_num += 1
        delete_objects()
