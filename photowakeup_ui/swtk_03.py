bl_info = {
    "name": "SweetK",
    "blender": (2, 90, 1),
    "category": "SweetK",
}

import bpy
import math
import numpy as np

class sweetkProcess(bpy.types.Operator):
    """Sweetk"""
    bl_idname = "object.sweetk"
    bl_label = "SweetK"
    bl_options = {'REGISTER', 'UNDO'}

    #total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)

    def execute(self, context):
        
        context = bpy.context
        for block in bpy.data.meshes:
            bpy.data.meshes.remove(block)

        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        for block in bpy.data.textures:
            if block.users == 0:
                bpy.data.textures.remove(block)

        for block in bpy.data.images:
            if block.users == 0:
                bpy.data.images.remove(block)
                
        for block in bpy.data.cameras:
            if block.users == 0:
                bpy.data.cameras.remove(block)

        #import obj
        print('------------------------------------------------------------------------------')
        file_loc = 'C:\\Users\\sweetk\\Desktop\\sweetk_blender\\hyeokmin_front_512.obj'
        texture_loc = 'C:\\Users\\sweetk\\Desktop\\sweetk_blender\\hyeokmin_front_512.png'
        data = np.load('C:\\Users\\sweetk\\Desktop\\sweetk_blender\\hyeokmin_front_joints.npy')
        for i in range(0, len(data)):
            data[i][1] += 0.11

        dat = [ [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        try:
            obj = bpy.ops.import_scene.obj(filepath=file_loc)
        except:
            pass
        if obj is None:
            self.report({"ERROR"}, "not file obj")

        for a in range(0, len(data)):
            dat[a] = [data[a][0], data[a][2], -data[a][1]]

        Pelvis = dat[0]
        L_Hip = dat[1]
        R_Hip = dat[2]
        Spine1 = dat[3]
        L_Knee = dat[4]
        R_Knee = dat[5]
        Spine2 = dat[6]
        L_Ankle = dat[7]
        R_Ankle = dat[8]
        Spine3 = dat[9]
        L_Foot = dat[10]
        R_Foot = dat[11]
        Neck = dat[12]
        L_Collar = dat[13]
        R_Collar = dat[14]
        Head = dat[15]
        L_Shoulder = dat[16]
        R_Shoulder = dat[17]
        L_Elbow = dat[18]
        R_Elbow = dat[19]
        L_Wrist = dat[20]
        R_Wrist = dat[21]
        lmiddle0 = dat[22]
        rmiddle0 = dat[23]

        anim_obj = []
        for i in bpy.context.scene.objects:
            if i.type == "ARMATURE":
                anim_obj.append(i)

        #2d frame move
        #change bone position
        #center
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = anim_obj[0]
        #anim_obj[0].select_set(True)
        #bpy.data.objects['1d23-001'] -> anim_obj[0]
        bpy.ops.object.editmode_toggle()
        anim_obj[0].data.edit_bones['Head'].head.z = Head[2]
        anim_obj[0].data.edit_bones['Neck'].tail.z = Head[2]
        anim_obj[0].data.edit_bones['Neck'].head.z = Neck[2]
        anim_obj[0].data.edit_bones['Chest4'].tail.z = L_Collar[2]
        anim_obj[0].data.edit_bones['Chest4'].head.z = Spine3[2]
        anim_obj[0].data.edit_bones['Chest3'].tail.z = Spine3[2]
        anim_obj[0].data.edit_bones['Chest3'].head.z = Spine2[2]
        anim_obj[0].data.edit_bones['Chest2'].tail.z = Spine2[2]
        anim_obj[0].data.edit_bones['Chest2'].head.z = Spine1[2]
        anim_obj[0].data.edit_bones['Chest'].tail.z = Spine1[2]
        anim_obj[0].data.edit_bones['Chest'].head.z = Pelvis[2]
        anim_obj[0].data.edit_bones['Hips'].tail.z = Pelvis[2]
        anim_obj[0].data.edit_bones['Hips'].head.z = L_Hip[2]

        #leftHip
        anim_obj[0].data.edit_bones['LeftHip'].head.x = L_Hip[0]
        anim_obj[0].data.edit_bones['LeftHip'].head.z = L_Hip[2]
        anim_obj[0].data.edit_bones['LeftHip'].tail.x = L_Knee[0]
        anim_obj[0].data.edit_bones['LeftHip'].tail.z = L_Knee[2]
        anim_obj[0].data.edit_bones['LeftKnee'].head.x = L_Knee[0]
        anim_obj[0].data.edit_bones['LeftKnee'].head.z = L_Knee[2]
        anim_obj[0].data.edit_bones['LeftKnee'].tail.x = L_Ankle[0]
        anim_obj[0].data.edit_bones['LeftKnee'].tail.z = L_Ankle[2]
        anim_obj[0].data.edit_bones['LeftAnkle'].head.x = L_Ankle[0]
        anim_obj[0].data.edit_bones['LeftAnkle'].head.z = L_Ankle[2]
        anim_obj[0].data.edit_bones['LeftAnkle'].tail.x = L_Foot[0]
        anim_obj[0].data.edit_bones['LeftAnkle'].tail.z = L_Foot[2]

        #rightHip
        anim_obj[0].data.edit_bones['RightHip'].head.x = R_Hip[0]
        anim_obj[0].data.edit_bones['RightHip'].tail.x = R_Knee[0]
        anim_obj[0].data.edit_bones['RightKnee'].head.x = R_Knee[0]
        anim_obj[0].data.edit_bones['RightKnee'].tail.x = R_Ankle[0]
        anim_obj[0].data.edit_bones['RightAnkle'].head.x = R_Ankle[0]
        anim_obj[0].data.edit_bones['RightAnkle'].tail.x = R_Foot[0]

        anim_obj[0].data.edit_bones['RightHip'].head.z = R_Hip[2]
        anim_obj[0].data.edit_bones['RightHip'].tail.z = R_Knee[2]
        anim_obj[0].data.edit_bones['RightKnee'].head.z = R_Knee[2]
        anim_obj[0].data.edit_bones['RightKnee'].tail.z = R_Ankle[2]
        anim_obj[0].data.edit_bones['RightAnkle'].head.z = R_Ankle[2]
        anim_obj[0].data.edit_bones['RightAnkle'].tail.z = R_Foot[2]

        #leftCollar
        anim_obj[0].data.edit_bones['LeftCollar'].head.x = L_Collar[0]
        anim_obj[0].data.edit_bones['LeftCollar'].tail.x = L_Shoulder[0]
        anim_obj[0].data.edit_bones['LeftShoulder'].head.x = L_Shoulder[0]
        anim_obj[0].data.edit_bones['LeftShoulder'].tail.x = L_Elbow[0]
        anim_obj[0].data.edit_bones['LeftElbow'].head.x = L_Elbow[0]
        anim_obj[0].data.edit_bones['LeftElbow'].tail.x = L_Wrist[0]
        anim_obj[0].data.edit_bones['LeftWrist'].head.x = L_Wrist[0]
        anim_obj[0].data.edit_bones['LeftWrist'].tail.x = lmiddle0[0]

        anim_obj[0].data.edit_bones['LeftCollar'].head.z = L_Collar[2]
        anim_obj[0].data.edit_bones['LeftCollar'].tail.z = L_Shoulder[2]
        anim_obj[0].data.edit_bones['LeftShoulder'].head.z = L_Shoulder[2]
        anim_obj[0].data.edit_bones['LeftShoulder'].tail.z = L_Elbow[2]
        anim_obj[0].data.edit_bones['LeftElbow'].head.z = L_Elbow[2]
        anim_obj[0].data.edit_bones['LeftElbow'].tail.z = L_Wrist[2]
        anim_obj[0].data.edit_bones['LeftWrist'].head.z = L_Wrist[2]
        anim_obj[0].data.edit_bones['LeftWrist'].tail.z = lmiddle0[2]


        #rightCollar
        anim_obj[0].data.edit_bones['RightCollar'].head.x = R_Collar[0]
        anim_obj[0].data.edit_bones['RightCollar'].tail.x = R_Shoulder[0]
        anim_obj[0].data.edit_bones['RightShoulder'].head.x = R_Shoulder[0]
        anim_obj[0].data.edit_bones['RightShoulder'].tail.x = R_Elbow[0]
        anim_obj[0].data.edit_bones['RightElbow'].head.x = R_Elbow[0]
        anim_obj[0].data.edit_bones['RightElbow'].tail.x = R_Wrist[0]
        anim_obj[0].data.edit_bones['RightWrist'].head.x = R_Wrist[0]
        anim_obj[0].data.edit_bones['RightWrist'].tail.x = rmiddle0[0]

        anim_obj[0].data.edit_bones['RightCollar'].head.z = R_Collar[2]
        anim_obj[0].data.edit_bones['RightCollar'].tail.z = R_Shoulder[2]
        anim_obj[0].data.edit_bones['RightShoulder'].head.z = R_Shoulder[2]
        anim_obj[0].data.edit_bones['RightShoulder'].tail.z = R_Elbow[2]
        anim_obj[0].data.edit_bones['RightElbow'].head.z = R_Elbow[2]
        anim_obj[0].data.edit_bones['RightElbow'].tail.z = R_Wrist[2]
        anim_obj[0].data.edit_bones['RightWrist'].head.z = R_Wrist[2]
        anim_obj[0].data.edit_bones['RightWrist'].tail.z = rmiddle0[2]

        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.armature.calculate_roll(type='VIEW')
        bpy.ops.object.editmode_toggle()
            
        #DecimateApply
        obj_object = bpy.data.objects['hyeokmin_front_512']
        obj_object.scale = (0.01, 0.01, 0.01)
        obj_object.rotation_euler = (0, 0, 0)

        if(obj_object.type=="MESH"):
            modifier=obj_object.modifiers.new(obj_object.name, 'DECIMATE')
            modifier.ratio = 0.1
            modifier.use_collapse_triangulate = True
            
        bpy.context.view_layer.objects.active = obj_object 
        bpy.ops.object.modifier_apply(modifier=obj_object.name)

        #RemeshApply
        bpy.ops.object.select_all(action='DESELECT')
        obj_object.select_set(True)
        if(obj_object.type=="MESH"):
            modifier=obj_object.modifiers.new(obj_object.name, 'REMESH')
            modifier.voxel_size = 1.5
            
        bpy.context.view_layer.objects.active = obj_object
        bpy.ops.object.modifier_apply(modifier=obj_object.name)

        #DecimateApply
        bpy.ops.object.select_all(action='DESELECT')
        obj_object.select_set(True)
        if(obj_object.type=="MESH"):
            modifier=obj_object.modifiers.new(obj_object.name, 'DECIMATE')
            modifier.ratio = 0.8
            modifier.use_collapse_triangulate = True
            
        bpy.context.view_layer.objects.active = obj_object
        bpy.ops.object.modifier_apply(modifier=obj_object.name)

        #Project from view
        bpy.ops.object.select_all(action='DESELECT')
        cam = bpy.data.objects['Camera'].select_set(True)
        bpy.context.view_layer.objects.active = cam
        bpy.ops.view3d.object_as_camera()
        #bpy.context.area.ui_type = 'VIEW_3D'
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj_object
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.project_from_view(camera_bounds=True, correct_aspect=False, scale_to_bounds=False)
        bpy.ops.object.editmode_toggle()

        #node connect
        nodes = context.active_object.active_material.node_tree.nodes
        links = context.active_object.active_material.node_tree.links

        importTex = bpy.ops.image.open(filepath=texture_loc, relative_path=True, show_multiview=False)
        mat = bpy.context.view_layer.objects.active.active_material
        tex = bpy.data.images.get('hyeokmin_front_512.png')
        imgnode = nodes.new('ShaderNodeTexImage')
        imgnode.location = (200, 800)
        imgnode.image = tex
        matnode = nodes["Material Output"]
        links.new(imgnode.outputs[0], matnode.inputs[0])

        #with automatic weights (animobj[0])
        bpy.ops.object.select_all(action='DESELECT')
        obj_object.select_set(True)
        bpy.context.view_layer.objects.active = anim_obj[0]
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')

        #modify A to T
        #angle of 3 point
        def cal(P1X, P1Y, P2X, P2Y, P3X, P3Y):
            numerator = P2Y*(P1X-P3X) + P1Y*(P3X-P2X) + P3Y*(P2X-P1X)
            denominator = (P2X-P1X)*(P1X-P3X) + (P2Y-P1Y)*(P1Y-P3Y)
            ratio = numerator/denominator
            angleRad = math.atan(ratio)
            angleDeg = (angleRad*180)/math.pi
            return -angleDeg

        #divisionRadio (using in elbow)
        def divisionRadio(p1x, p1y, p2x, p2y):
            if(p2x > p1x):
                x = 2*p2x - p1x
                y = 2*p2y - p1y
            else:
                x = 2*p1x - p2x
                y = 2*p1y - p2y
            
            return x, y
        
        #length point to point
        def lengthPtoP(p1x, p1y, p2x, p2y):
            a = p2x - p1x
            b = p2y - p1y
            c = math.sqrt((a * a) + (b * b))
            return c
        
        #calc length
        R_Shoulder_length = lengthPtoP(R_Shoulder[0], R_Shoulder[2], R_Elbow[0], R_Elbow[2])
        L_Shoulder_length = lengthPtoP(L_Shoulder[0], L_Shoulder[2], L_Elbow[0], L_Elbow[2])
        R_Elbow_length = lengthPtoP(R_Elbow[0], R_Elbow[2], R_Wrist[0], R_Wrist[2])
        L_Elbow_length = lengthPtoP(L_Elbow[0], L_Elbow[2], L_Wrist[0], L_Wrist[2])
        R_Wrist_length = lengthPtoP(R_Wrist[0], R_Wrist[2], rmiddle0[0], rmiddle0[2])
        L_Wrist_length = lengthPtoP(L_Wrist[0], L_Wrist[2], lmiddle0[0], lmiddle0[2])
            
        #calc angle
        R_Shoulder_Angle = cal(R_Shoulder[0], R_Shoulder[2], R_Elbow[0], R_Elbow[2], R_Shoulder[0]+0.1, R_Shoulder[2])
        L_Shoulder_Angle = cal(L_Shoulder[0], L_Shoulder[2], L_Elbow[0], L_Elbow[2], L_Shoulder[0]+0.1, L_Shoulder[2])

        ratR = divisionRadio(R_Shoulder[0], R_Shoulder[2], R_Elbow[0], R_Elbow[2])
        ratL = divisionRadio(L_Shoulder[0], L_Shoulder[2], L_Elbow[0], L_Elbow[2])

        R_Elbow_Angle = cal(R_Elbow[0], R_Elbow[2], R_Wrist[0], R_Wrist[2], ratR[0], ratR[1])
        L_Elbow_Angle = cal(L_Elbow[0], L_Elbow[2], L_Wrist[0], L_Wrist[2], ratL[0], ratL[1])

        #modify
        bpy.context.view_layer.objects.active = anim_obj[0]
        bpy.context.object.pose.bones["LeftShoulder"].rotation_euler[2] = math.radians(L_Shoulder_Angle)
        bpy.context.object.pose.bones["RightShoulder"].rotation_euler[2] = math.radians(R_Shoulder_Angle)
        bpy.context.object.pose.bones["LeftElbow"].rotation_euler[2] = math.radians(L_Elbow_Angle)
        bpy.context.object.pose.bones["RightElbow"].rotation_euler[2] = math.radians(R_Elbow_Angle)

        #apply and clear parent
        bpy.context.view_layer.objects.active = obj_object
        bpy.ops.object.modifier_apply(modifier="Armature")
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        
        #anim[1] set bone length Order important
        bpy.context.view_layer.objects.active = anim_obj[1]
        bpy.ops.object.editmode_toggle()
        anim_obj[1].data.edit_bones['LeftShoulder'].length = L_Shoulder_length
        anim_obj[1].data.edit_bones['RightShoulder'].length = R_Shoulder_length
        anim_obj[1].data.edit_bones['LeftElbow'].head = anim_obj[1].data.edit_bones['LeftShoulder'].tail
        anim_obj[1].data.edit_bones['RightElbow'].head = anim_obj[1].data.edit_bones['RightShoulder'].tail
        anim_obj[1].data.edit_bones['LeftElbow'].length = L_Elbow_length
        anim_obj[1].data.edit_bones['RightElbow'].length = R_Elbow_length
        anim_obj[1].data.edit_bones['LeftWrist'].head = anim_obj[1].data.edit_bones['LeftElbow'].tail
        anim_obj[1].data.edit_bones['RightWrist'].head = anim_obj[1].data.edit_bones['RightElbow'].tail
        anim_obj[1].data.edit_bones['LeftWrist'].length = L_Wrist_length
        anim_obj[1].data.edit_bones['RightWrist'].length = R_Wrist_length
        bpy.ops.object.editmode_toggle()
        
        #with automatic weights (animobj[1])
        bpy.ops.object.select_all(action='DESELECT')
        obj_object.select_set(True)
        bpy.context.view_layer.objects.active = anim_obj[1]
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        
        #export verge3d
        bpy.context.scene.camera = bpy.data.objects["cam_web"]
        #bpy.context.scene.v3d_export.lzma_enabled = False
        bpy.ops.v3d.export_gltf(filepath="C:\\Users\\sweetk\\verge3d_blender\\applications\\SweetK\\SweetK")

        print("OK")

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(sweetkProcess.bl_idname)

addon_keymaps = []


def register():
    bpy.utils.register_class(sweetkProcess)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(idname="object.sweetk", type='K', value='PRESS', shift=False)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(sweetkProcess)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
