import bpy
import random
import numpy as np
import os
import cv2
import png
from math import pi,sqrt,asin,atan
from mathutils import Vector,Matrix
import csv
from scipy.optimize import root

#Set the camera position and poses, and set four poses randomly
def set_camera():
    i = random.randint(1,4)
    if i == 1:
        bpy.data.objects["Camera"].location = [0.6,0,0.1]
        bpy.data.objects["Camera"].rotation_euler = [(pi * 90 / 180), 0, (pi * 90 / 180)]
    elif i == 2:
        bpy.data.objects["Camera"].location = [0.5,0,0.38]
        bpy.data.objects["Camera"].rotation_euler = [(pi * 60 / 180), 0, (pi * 90 / 180)]
    elif i == 3:
        bpy.data.objects["Camera"].location = [0.28,0,0.55]
        bpy.data.objects["Camera"].rotation_euler = [(pi * 30 / 180), 0, (pi * 90 / 180)]
    elif i == 4:
        bpy.data.objects["Camera"].location = [0,0,0.6]
        bpy.data.objects["Camera"].rotation_euler = [0, 0, (pi * 90 / 180)]
    loc = bpy.data.objects["Camera"].location.copy()
    rot = bpy.data.objects["Camera"].rotation_euler.copy()
    return loc,rot

#Randomly set a shaking range for the camera
def camera_shaking(loc, rot):
    bpy.data.objects["Camera"].rotation_euler[0] = rot[0] + random.uniform(-0.02,0.02)
    bpy.data.objects["Camera"].rotation_euler[1] = rot[1] + random.uniform(-0.02,0.02)
    bpy.data.objects["Camera"].rotation_euler[2] = rot[2] + random.uniform(-0.02,0.02)
    bpy.data.objects["Camera"].location = loc + Vector((random.uniform(-0.01,0.01),random.uniform(-0.01,0.01),random.uniform(-0.01,0.01)))
    
#Select a photographic background at random
def set_background():
    for obj in bpy.context.scene.objects:
        if obj.name == 'noble_table' or obj.name == 'stone_table' or obj.name == 'wooden_table' or obj.name == 'studio_Corner' or obj.name == 'studioL':
            obj.hide_render = True
            obj.hide_viewport = True
    i = random.randint(1,5)

    if i == 1:
        bpy.data.objects['noble_table'].hide_render = False
        bpy.data.objects['noble_table'].hide_viewport = False
        bpy.data.objects['noble_table'].location[0] = random.uniform(-0.05,0.05)
        bpy.data.objects['noble_table'].location[1] = random.uniform(-0.05,0.05)
        background = 'noble_table'

    elif i == 2:
        bpy.data.objects['stone_table'].hide_render = False
        bpy.data.objects['stone_table'].hide_viewport = False
        bpy.data.objects['stone_table'].location[0] = random.uniform(-0.05,0.05)
        bpy.data.objects['stone_table'].location[1] = random.uniform(-0.05,0.05)
        background = 'stone_table'

    elif i == 3:
        bpy.data.objects['wooden_table'].hide_render = False
        bpy.data.objects['wooden_table'].hide_viewport = False
        bpy.data.objects['wooden_table'].location[0] = random.uniform(-0.05,0.05)
        bpy.data.objects['wooden_table'].location[1] = random.uniform(-0.05,0.05)
        background = 'wooden_table'

    elif i == 4:
        bpy.data.objects['studio_Corner'].hide_render = False
        bpy.data.objects['studio_Corner'].hide_viewport = False
        back_rgb = random.uniform(0.03,0.4)
        bpy.data.materials["studio_Corner_mat_clay"].node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (back_rgb, back_rgb, back_rgb, 1)
        bpy.data.objects['studio_Corner'].location[0] = random.uniform(-0.05,0.05)
        bpy.data.objects['studio_Corner'].location[1] = random.uniform(-0.05,0.05)
        background = 'studio_Corner'

    elif i == 5:
        bpy.data.objects['studioL'].hide_render = False
        bpy.data.objects['studioL'].hide_viewport = False
        back_rgb = random.uniform(0.03,0.4)
        bpy.data.materials["studioL_stoffa_bianca_stesa"].node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (back_rgb, back_rgb, back_rgb, 1)
        bpy.data.objects['studioL'].location[0] = random.uniform(-0.1,0.1)
        bpy.data.objects['studioL'].location[1] = random.uniform(-0.1,0.1)
        background = 'studioL'
    
    return background

#Random combination and brightness adjustment of photographic lights
def set_light(background):
    for obj in bpy.context.scene.objects:
        if obj.name == 'umbrella_white' or obj.name == 'umbrella_yellow' or obj.name == 'beam_light' or obj.name == 'softbox' or obj.name == 'Spot':
            obj.hide_render = True
            obj.hide_viewport = True
    if background == 'studio_Corner' or background == 'studioL':
        i = random.randint(1,2)
    else:
        i = random.randint(1,3)
    if i == 1:
        bpy.data.objects['softbox'].hide_viewport=False
        bpy.data.objects['softbox'].hide_render=False
        softbox0 = bpy.data.objects['softbox']
        softbox0.active_material = softbox0.data.materials[softbox0.name+'_emission']
        softbox1 = softbox0.copy()
        softbox1.data = softbox0.data.copy()
        softbox1.active_material = softbox0.active_material.copy()
        bpy.data.collections["Collection"].objects.link(softbox1)
        softbox2 = softbox0.copy()
        softbox2.data = softbox0.data.copy()
        softbox2.active_material = softbox0.active_material.copy()
        bpy.data.collections["Collection"].objects.link(softbox2)
        softbox0.location = [-0.1,0,0.7]
        softbox0.rotation_euler = [(pi * 90 / 180), (-pi * 90 / 180), (pi * 90 / 180)]
        random_rotate = random.uniform(-15,0)
        softbox1.location = [-0.1,0.55,0.3]
        softbox1.rotation_euler = [(pi * 90 / 180), (pi * random_rotate / 180), (pi * 90 / 180)]
        softbox2.location = [-0.1,-0.55,0.3]
        softbox2.rotation_euler = [(pi * 90 / 180), (pi * random_rotate / 180), (pi * -90 / 180)]
        t = random.randint(1,2)
        if t == 1:
            softbox0.active_material.node_tree.nodes["Emission"].inputs[1].default_value = random.uniform(3,5)
            softbox1.active_material.node_tree.nodes["Emission"].inputs[1].default_value = random.uniform(2,5)
            softbox2.active_material.node_tree.nodes["Emission"].inputs[1].default_value = random.uniform(2,5)
        elif t == 2:
            pow = random.uniform(3,5)
            softbox0.active_material.node_tree.nodes["Emission"].inputs[1].default_value = pow
            softbox1.active_material.node_tree.nodes["Emission"].inputs[1].default_value = pow
            softbox2.active_material.node_tree.nodes["Emission"].inputs[1].default_value = pow
        return [softbox0.name, softbox1.name, softbox2.name]
    elif i == 2:
        left_light = bpy.data.objects[random.choice(['umbrella_white','beam_light','softbox'])]
        left_light.hide_viewport = False
        left_light.hide_render = False
        left_light.active_material = left_light.data.materials[left_light.name+'_emission']
        right_light = left_light.copy()
        right_light.data = left_light.data.copy()
        right_light.active_material = left_light.active_material.copy()
        x_location = random.uniform(0.2,0.5)
        y_location = sqrt(0.5-x_location**2)
        z_location = random.uniform(0.5,0.8)
        left_light.location = (x_location, y_location, z_location)
        left_light.rotation_euler = (0, -asin((z_location-0.4)/sqrt(0.5)), atan(y_location/x_location))
        right_light.location = (x_location, -y_location, z_location)
        right_light.rotation_euler = (0, -asin((z_location-0.4)/sqrt(0.5)), -atan(y_location/x_location))
        bpy.data.collections["Collection"].objects.link(right_light)
        t = random.randint(1,2)
        if t == 1:
            if left_light.name == 'beam_light':
                left_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = random.uniform(50,100)
                right_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = random.uniform(50,100)
            elif left_light.name == 'softbox':
                left_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = random.uniform(5,15)
                right_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = random.uniform(5,15)
            elif left_light.name == 'umbrella_white':
                left_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = random.uniform(300,600)
                right_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = random.uniform(300,600)
        elif t == 2:
            if left_light.name == 'beam_light':
                pow = random.uniform(50,100)
                left_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = pow
                right_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = pow
            elif left_light.name == 'softbox':
                pow = random.uniform(5,15)
                left_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = pow
                right_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = pow
            elif left_light.name == 'umbrella_white':
                pow = random.uniform(300,600)
                left_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = pow
                right_light.active_material.node_tree.nodes["Emission"].inputs[1].default_value = pow
        return [left_light.name, right_light.name]
    elif i == 3:
        spot = bpy.data.objects['Spot']
        spot.hide_viewport=False
        spot.hide_render=False
        spot.data.color = (0.9, 0.85, 0.8)
        spot.data.energy = random.randint(150,250)
        aux = bpy.data.objects[random.choice(['umbrella_white','umbrella_yellow','softbox'])]
        aux.hide_viewport = False
        aux.hide_render = False
        aux.active_material = aux.data.materials[aux.name+'_emission']
        if aux.name == 'softbox':
            aux.active_material.node_tree.nodes["Emission"].inputs[1].default_value = 10
        else:
            aux.active_material.node_tree.nodes["Emission"].inputs[1].default_value = 600
        if bpy.data.objects['softbox'].hide_viewport:
            spot.location = [random.choice([-0.5,0.5]), random.choice([-0.8,0.8]), 0.6]
        else:
            spot.location = [0.5, random.choice([-0.8,0.8]), 0.6]
        spot.rotation_euler = [(pi * 45 / 180) * (-spot.location[1]/abs(spot.location[1])),(pi * 45 / 180) * (spot.location[0]/abs(spot.location[0])), 0]
        aux.location = [spot.location[0], -(spot.location[1]+0.1), 0.6]
        aux.rotation_euler = [0, (-pi * 30 / 180), ((aux.location[1]/abs(aux.location[1])) * pi * (90 + 45 * (-aux.location[0]/abs(aux.location[0]))) / 180)]
        return [spot.name, aux.name]

#Object placement, including normal placement, enlarged display of details and random placement of multiple objects
def set_object(object_num,type):
    in_dir_ply =  r"../dataset_create/mesh/"+ object_num +"/"
    lst_ply = os.listdir(in_dir_ply)
    for item in lst_ply:
        fileName, fileExtension = os.path.splitext(item)
        if fileExtension == ".gltf":
            bpy.ops.import_scene.gltf(filepath=os.path.join(in_dir_ply,item))
    for obj in bpy.context.scene.objects:
        if obj.name.split('.')[0] == object_num:
            bpy.context.object.rotation_mode = 'XYZ'
            obj.rotation_euler[2]=random.uniform(0, 6.28)
            if type == 'general':
                obj.location= [random.uniform(0,0.05),0,0]
                # obj.scale=obj.scale*random.uniform(1, 1.3)
    if type == 'detail':
        s=random.uniform(1.8, 2.5)
        obj = bpy.context.selected_objects
        for obj in bpy.context.scene.objects:
            if obj.name.split('.')[0] == object_num:
                obj.scale=obj.scale*s
                obj.location= [random.uniform(-0.1,0.1),random.uniform(-0.1,0.1),random.uniform(-0.05,0.05)]
    elif type == 'multi':
        for obj in bpy.context.scene.objects:
            if obj.name.split('.')[0] == object_num:
                obj.location=[random.uniform(-0.1,0.1),random.uniform(-0.1,0.1),0]
                
#Object deletion
def delete_objects():
    for obj in bpy.context.scene.objects:
         if obj.type == 'MESH' and obj.name != 'Camera' and obj.name!='Plane' and obj.name!='studio_Corner' and obj.name!='stone_table' and obj.name!='wooden_table' and obj.name!='noble_table' and obj.name!='umbrella_white' and obj.name!='umbrella_yellow' and obj.name!='beam_light' and obj.name!='softbox' and obj.name!='studioL' and obj.name!='Spot':
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
            
#Depth map and mask rendering
def reder_depth(path, num, background):
    bpy.data.objects["Camera"].data.dof.use_dof=False
    bpy.context.scene.use_nodes = True
    RL=bpy.data.scenes['Scene'].node_tree.nodes["Render Layers"].outputs[2]
    IMG=bpy.data.scenes['Scene'].node_tree.nodes["Composite"].inputs[0]
    Alpha=bpy.data.scenes['Scene'].node_tree.nodes["Composite"].inputs[1]
    Z=bpy.data.scenes['Scene'].node_tree.nodes["Composite"].inputs[2]
    bpy.data.scenes['Scene'].node_tree.links.new(RL,IMG)
    bpy.data.scenes['Scene'].node_tree.links.new(RL,Alpha)
    bpy.data.scenes['Scene'].node_tree.links.new(RL,Z)
    for obj in bpy.context.scene.objects:
        if obj.name != 'Camera' and obj.name!='Plane' and obj.name!='studio_Corner' and obj.name!='stone_table' and obj.name!='wooden_table' and obj.name!='noble_table' and obj.name!='umbrella_white' and obj.name!='umbrella_yellow' and obj.name!='beam_light' and obj.name!='softbox' and obj.name!='studioL' and obj.name!='Spot':
            for j in range(len(obj.data.materials)):
                obj.data.materials[j].use_nodes=False
    #render depth
    bpy.context.scene.render.image_settings.file_format = "OPEN_EXR"
    bpy.context.scene.render.image_settings.color_mode = 'RGB'
    bpy.context.scene.render.image_settings.color_depth = '32'
    bpy.context.scene.render.use_file_extension = False
    bpy.context.scene.render.image_settings.use_zbuffer = True
    for scene in bpy.data.scenes:
        scene.cycles.device = 'GPU'
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = "OPTIX"
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print('Depth render device:', bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
    bpy.context.scene.render.filepath =path+'depth_'+str(num)+'.exr'
    bpy.ops.render.render( write_still=True )   
    #mask
    for obj in bpy.context.scene.objects:
        if obj.name == background or obj.name == 'Plane':
            obj.hide_render = True
            obj.hide_viewport = True
    bpy.context.scene.render.filepath =path+'mask_'+str(num)+'.exr'
    bpy.ops.render.render( write_still=True )
    mask = cv2.imread(path+'mask_'+str(num)+'.exr', cv2.IMREAD_UNCHANGED)
    mask = mask[:,:,0]
    closest=mask.min()
    for i in range(15, 30):
        farest=mask[mask <= 1.5].max()
        if farest != i/10:
            mask[mask <= i/10] = 1
            mask[mask > i/10] = 0
            break
    dMap = (mask*(pow(2,8)-1)).astype(np.uint8)
    savepath = path+'mask_'+str(num)+'.png'
    with open(savepath, 'wb') as f:
        writer = png.Writer(width=dMap.shape[1], height=dMap.shape[0], bitdepth=8, greyscale=True)
        zgray2list = dMap.tolist()
        writer.write(f, zgray2list)
    for obj in bpy.context.scene.objects:
        if obj.name == background or obj.name == 'Plane':
            obj.hide_render = False
            obj.hide_viewport = False
    bpy.context.scene.use_nodes = False
    for obj in bpy.context.scene.objects:
        if obj.name != 'Camera' and obj.name!='Plane' and obj.name!='studio_Corner' and obj.name!='stone_table' and obj.name!='wooden_table' and obj.name!='noble_table' and obj.name!='umbrella_white' and obj.name!='umbrella_yellow' and obj.name!='beam_light' and obj.name!='softbox' and obj.name!='studioL' and obj.name!='Spot':
            for j in range(len(obj.data.materials)):
                obj.data.materials[j].use_nodes=True
    return closest,farest
    
#All-in-focus images rendering
def reder_allinfocus(path,num):
    bpy.data.objects["Camera"].data.dof.use_dof=False
    bpy.context.scene.use_nodes = False
    bpy.context.scene.render.image_settings.file_format = "TIFF"
    bpy.context.scene.render.image_settings.color_mode = 'RGB'
    bpy.context.scene.render.image_settings.color_depth = '16'
    bpy.context.scene.render.image_settings.tiff_codec = 'NONE'
    bpy.context.scene.render.use_file_extension = False
    bpy.context.scene.render.filepath =path+'all_in_focus_'+str(num)+'.tif'
    for scene in bpy.data.scenes:
        scene.cycles.device = 'GPU'
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = "OPTIX"
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print('Aif render device:', bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
    bpy.ops.render.render( write_still=True )

#defocus images rendering
def render_focal_stack(path,distance,num):
    bpy.data.objects["Camera"].data.dof.use_dof=True
    bpy.context.scene.use_nodes = False
    bpy.context.scene.render.image_settings.file_format = "TIFF"
    bpy.context.scene.render.image_settings.color_mode = 'RGB'
    bpy.context.scene.render.image_settings.color_depth = '16'
    bpy.context.scene.render.image_settings.tiff_codec = 'NONE'
    bpy.context.scene.render.use_file_extension = False
    bpy.data.objects["Camera"].data.dof.focus_distance = distance
    bpy.context.scene.render.filepath =path+'defocus_'+str(num)+'.tif'
    for scene in bpy.data.scenes:
        scene.cycles.device = 'GPU'
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = "OPTIX"
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print('focus stack render device:',bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
    bpy.ops.render.render( write_still=True )
    
#set up path
def mkdir(path):
    path=path.strip()
    path=path.rstrip("/")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        
#defocus map rendering
def COC(path,focus_distance,num,N,F):
    depthimage = cv2.imread(path+'depth_'+str(num)+'.exr', cv2.IMREAD_UNCHANGED)
    savepath=path+'defocusmap_'+str(num)+'.exr'
    savepath2=path+'defocusmap_'+str(num)+'.png'
    depth=1000*depthimage[:,:,1] #distance  from the lens to the object
    S1=1000*focus_distance #focus distance
    defocus=(F**2/ (N * (S1 - F))) * (abs(depth - S1) / depth)
    cv2.imwrite(savepath, defocus)
    dMap = ((defocus-np.min(defocus))*(pow(2,8)-1)/(np.max(defocus)-np.min(defocus))).astype(np.uint8)
    with open(savepath2, 'wb') as f:
        writer = png.Writer(width=dMap.shape[1], height=dMap.shape[0], bitdepth=8, greyscale=True)
        zgray2list = dMap.tolist()
        writer.write(f, zgray2list)
        
#Calculate focal distance according to the depth of field formula
def compute_focal_distance(F, f, theta, closest, farest, focal_stack_count, focal_stack):
    def func(x2,F=F,f=f,theta=theta,closest=closest,farest=farest):
        focal_distance = [closest,x2]
        for i in range(focal_stack_count-2):
            DOF1_back = (F*theta*focal_distance[i]**2)/(f**2-F*theta*focal_distance[i])
            DOF2_flont = (F*theta*focal_distance[i+1]**2)/(f**2+F*theta*focal_distance[i+1])
            DOF2_back = (F*theta*focal_distance[i+1]**2)/(f**2-F*theta*focal_distance[i+1])
            t = focal_distance[i+1]+DOF2_back-(DOF2_back/DOF1_back)*(focal_distance[i]+DOF1_back-focal_distance[i+1]+DOF2_flont)
            focal_distance.append(t*f**2/(f**2-t*F*theta))
        return t*f**2/(f**2-t*F*theta) - farest
    x2 = root(func,closest).x[0]
    per = (closest+(F*theta*(closest**2))/(f**2-F*theta*closest) - x2+(F*theta*x2**2)/(f**2+F*theta*x2)) / ((F*theta*closest**2)/(f**2-F*theta*closest))
    if focal_stack == 0 :
        return closest/1000,per
    elif focal_stack ==1:
        return x2/1000,per
    elif focal_stack == focal_stack_count-1:
        return farest/1000,per
    else:
        focal_distance = [closest,x2]
        for i in range(focal_stack-1):
            DOF1_back = (F*theta*focal_distance[i]**2)/(f**2-F*theta*focal_distance[i])
            DOF2_flont = (F*theta*focal_distance[i+1]**2)/(f**2+F*theta*focal_distance[i+1])
            DOF2_back = (F*theta*focal_distance[i+1]**2)/(f**2-F*theta*focal_distance[i+1])
            t = focal_distance[i+1]+DOF2_back-(DOF2_back/DOF1_back)*(focal_distance[i]+DOF1_back-focal_distance[i+1]+DOF2_flont)
            focal_distance.append(t*f**2/(f**2-t*F*theta))
        return focal_distance[-1]/1000, per
    
        
# BKE_camera_sensor_size
def get_sensor_size(sensor_fit, sensor_x, sensor_y):
    if sensor_fit == 'VERTICAL':
        return sensor_y
    return sensor_x

# BKE_camera_sensor_fit
def get_sensor_fit(sensor_fit, size_x, size_y):
    if sensor_fit == 'AUTO':
        if size_x >= size_y:
            return 'HORIZONTAL'
        else:
            return 'VERTICAL'
    return sensor_fit

# Build intrinsic camera parameters from Blender camera data
#
# See notes on this in 
# blender.stackexchange.com/questions/15102/what-is-blenders-camera-projection-matrix-model
# as well as
# https://blender.stackexchange.com/a/120063/3581
def get_calibration_matrix_K_from_blender(camd):
    scene = bpy.context.scene
    f_in_mm = camd.lens
    scale = scene.render.resolution_percentage / 100
    resolution_x_in_px = scale * scene.render.resolution_x
    resolution_y_in_px = scale * scene.render.resolution_y
    sensor_size_in_mm = get_sensor_size(camd.sensor_fit, camd.sensor_width, camd.sensor_height)
    sensor_fit = get_sensor_fit(
        camd.sensor_fit,
        scene.render.pixel_aspect_x * resolution_x_in_px,
        scene.render.pixel_aspect_y * resolution_y_in_px
    )
    pixel_aspect_ratio = scene.render.pixel_aspect_y / scene.render.pixel_aspect_x
    if sensor_fit == 'HORIZONTAL':
        view_fac_in_px = resolution_x_in_px
    else:
        view_fac_in_px = pixel_aspect_ratio * resolution_y_in_px
    pixel_size_mm_per_px = sensor_size_in_mm / f_in_mm / view_fac_in_px
    s_u = 1 / pixel_size_mm_per_px
    s_v = 1 / pixel_size_mm_per_px / pixel_aspect_ratio

    # Parameters of intrinsic calibration matrix K
    u_0 = resolution_x_in_px / 2 - camd.shift_x * view_fac_in_px
    v_0 = resolution_y_in_px / 2 + camd.shift_y * view_fac_in_px / pixel_aspect_ratio
    skew = 0 # only use rectangular pixels

    K = Matrix(
        ((s_u, skew, u_0, 0),
        (   0,  s_v, v_0, 0),
        (   0,    0,   1, 0),
        (0,0,0,1)))
    KK = [list(K[0]),list(K[1]),list(K[2]),list(K[3])]
    return KK

def get_RT_matrix_from_blender(cam):
    # bcam stands for blender camera
    R_bcam2cv = Matrix(
        ((1, 0,  0),
         (0, -1, 0),
         (0, 0, -1)))
    # Transpose since the rotation is object rotation, 
    # and we want coordinate rotation
    # R_world2bcam = cam.rotation_euler.to_matrix().transposed()
    # T_world2bcam = -1*R_world2bcam * location
    #
    # Use matrix_world instead to account for all constraints
    location, rotation = cam.matrix_world.decompose()[0:2]
    R_world2bcam = rotation.to_matrix().transposed()
    # Convert camera location to translation vector used in coordinate changes
    # T_world2bcam = -1*R_world2bcam*cam.location
    # Use location from matrix_world to account for constraints:     
    T_world2bcam = -1*R_world2bcam @ location
    # Build the coordinate transform matrix from world to computer vision camera
    # NOTE: Use * instead of @ here for older versions of Blender
    # TODO: detect Blender version
    R_world2cv = R_bcam2cv@R_world2bcam
    T_world2cv = R_bcam2cv@T_world2bcam
    # put into 3x4 matrix
    RT = Matrix((
        R_world2cv[0][:] + (T_world2cv[0],),
        R_world2cv[1][:] + (T_world2cv[1],),
        R_world2cv[2][:] + (T_world2cv[2],),
        (0,0,0,1)
         ))
    R = [list(RT[0]),list(RT[1]),list(RT[2]),list(RT[3])]
    return R
        
if __name__=='__main__':
    obj_count = 1000 #obj total count
    scene_num =  300#target dataset count
    focal_stack_count = 5 #focal stack in the scene
    
    N=2.8 #aperture F
    F=50.0 #focal length
    theta = 0.11 #limit defocus
    
    #Depth of field overlap of two adjacent focus stacks
    DOF_overlap_min = 0.4
    DOF_overlap_max = 0.8
    
    #output path
    path_big = "../dataset_create/test/dataset_960x720/"
    path_small = "../dataset_create/test/dataset_480x360/"
    mkdir(path_big)
    mkdir(path_small)
    
    #render device
    bpy.context.preferences.addons['cycles'].preferences.devices[0].use = False
    bpy.context.preferences.addons['cycles'].preferences.devices[1].use = True
    
    for n in range(scene_num):
        path1 = path_big + str(n)+"/"
        path2 = path_small + str(n)+"/"
        mkdir(path1)
        mkdir(path2)
        FLAG = True
        count=0
        while FLAG:
            delete_objects()
            count += 1
            loc, rot = set_camera()
            background = set_background()
            light = set_light(background)
            if n < scene_num/3:
                type = 'general'
                obj = str(n%obj_count)
                set_object(obj, type)
            elif n >= 2*scene_num/3:
                type = 'multi'
                obj=[]
                for i in range(random.randint(2,4)):
                    obj.append(str(random.randint(0, obj_count-1)))
                    set_object(obj[-1], type)
            else:
                type = 'detail'
                obj = str(n%obj_count)
                set_object(obj, type)
                
            for focal_stack in range(focal_stack_count):
                if focal_stack != 0:
                    camera_shaking(loc, rot)
                for path in (path1, path2):
                    if path == path1:
                        bpy.context.scene.render.resolution_x = 960
                        bpy.context.scene.render.resolution_y = 720
                        f = open(path + '/info_' + str(focal_stack) + '.csv','w',newline='')
                    elif path == path2:
                        bpy.context.scene.render.resolution_x = 480
                        bpy.context.scene.render.resolution_y = 360
                        f = open(path + '/info_' + str(focal_stack) + '.csv','w',newline='')
                    closest, farest = reder_depth(path, focal_stack, background)
                    focus_distance, DOF_overlap = compute_focal_distance(N, F, theta, closest*1000, farest*1000, focal_stack_count, focal_stack)
                    print('DOF_overlap',DOF_overlap)
                    if DOF_overlap > DOF_overlap_min and DOF_overlap < DOF_overlap_max:
                        FLAG = False
                    else:
                        FLAG = True
                        f.close()
                        break
                    reder_allinfocus(path, focal_stack)
                    render_focal_stack(path, focus_distance, focal_stack)
                    COC(path, focus_distance, focal_stack, N, F)
                    K = get_calibration_matrix_K_from_blender(bpy.data.objects["Camera"].data)
                    RT = get_RT_matrix_from_blender(bpy.data.objects["Camera"])
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(["K",K])
                    csv_writer.writerow(["RT",RT])
                    csv_writer.writerow(["closest",closest])
                    csv_writer.writerow(["farest",farest])
                    csv_writer.writerow(["DOF_overlap",DOF_overlap])
                    csv_writer.writerow(["focus_distance",focus_distance])
                    csv_writer.writerow(["background",[background]])
                    csv_writer.writerow(["light",light])
                    f.close()
                if FLAG:
                    break
            delete_objects()
            if count == 100:
                FLAG = False
                with open("../dataset_create/fail_eg.txt","a") as f:
                    f.write(str(n)+',')