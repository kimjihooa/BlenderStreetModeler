import bpy
import bmesh
import math
import random
import os

if bpy.context.mode == 'EDIT_MESH':
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
elif bpy.context.mode == 'OBJECT':
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
for m in bpy.data.materials:
    bpy.data.materials.remove(m)
    
class bm_transform:
    def extrude_and_move_edge(bm, edge_min, edge_max, vector):
        '''
        extrude and translate edge.
        bm - bmesh to transform
        edge_min - minimum index of edge to extrude
        edge_max - maximum index of edge to extrude
        vector - tuple with 3 floats. Each float means x, y, z axis amount
        '''
        translate_verts = []
        for i in bm.edges:
            if i.index >= edge_min and i.index <= edge_max:
                for j in bm.verts:
                    translate_verts.append(j.index)
        vert_min = min(translate_verts)
        vert_max = max(translate_verts)

        bmesh.ops.extrude_face_region(bm, geom =  bm.edges[edge_min: edge_max + 1])
        bmesh.ops.translate(bm, verts = bm.verts[vert_min: vert_max + 1], vec = (-vector[0], -vector[1], -vector[2]))

    def branch_creator(bm, vert, length):
        '''z
        extrude and translate a verticy to create a branch. Returns list of vert's index that are created
        bm - bmesh to transform
        vert - verticy to extrude
        length - Criteria of length of each branch. It will randomly choose the length in range of (length*0.5, lenght*1.5)
        '''
        branch_num = random.randrange(2, 4)
        branch_order = 0
        new_verts = []

        if branch_num == 2:
            for i in range(0, branch_num):
                ran_length = length*random.uniform(0.5, 1.5)
                if branch_order%2 == 0:
                    h_angle = math.radians(random.uniform(45, 85))
                    b_angle = math.radians(random.uniform(210, 300))
                    branch_order += 1
                else:
                    h_angle = math.radians(random.uniform(45, 85))
                    b_angle = math.radians(random.uniform(30, 120))
                    branch_order += 1
                new_vert = bmesh.ops.extrude_face_region(bm, geom =  bm.verts[vert: vert + 1])
                bmesh.ops.translate(bm,
                                    verts = bm.verts[new_vert['geom'][0].index: new_vert['geom'][0].index +1], 
                                    vec = (ran_length*math.cos(h_angle)*math.cos(b_angle),
                                           ran_length*math.cos(h_angle)*math.sin(b_angle), 
                                           ran_length*math.sin(h_angle)))

                new_verts.append(new_vert["geom"][0].index)

        elif branch_num == 3:
            for i in range(0, branch_num):
                ran_length = length*random.uniform(0.5, 1.5)
                if branch_order%3 == 0:
                    h_angle = math.radians(random.uniform(60, 85))
                    b_angle = math.radians(random.uniform(15, 105))
                    branch_order += 1
                elif branch_order%3 == 1:
                    h_angle = math.radians(random.uniform(60, 85))
                    b_angle = math.radians(random.uniform(135, 225))
                    branch_order += 1
                else:
                    h_angle = math.radians(random.uniform(60, 85))
                    b_angle = math.radians(random.uniform(255, 345))
                    branch_order += 1

                new_vert = bmesh.ops.extrude_face_region(bm, geom =  bm.verts[vert: vert + 1])
                bmesh.ops.translate(bm, 
                                    verts = bm.verts[new_vert['geom'][0].index: new_vert['geom'][0].index +1], 
                                    vec = (ran_length*math.cos(h_angle)*math.cos(b_angle),
                                           ran_length*math.cos(h_angle)*math.sin(b_angle), 
                                           ran_length*math.sin(h_angle)))
                new_verts.append(new_vert["geom"][0].index)

        return new_verts
    
    def proportional(bm, vert, strength, radius):
        
        verts_list = []
        distance_list = []
        
        for i in bm.verts:
            if bm_transform.get_Distance(bm.verts[vert:vert+1][0], i) <= radius:
                verts_list.append(i.index)
                distance_list.append(bm_transform.get_Distance(bm.verts[vert:vert+1][0], i))
        
        for i in verts_list:
            if distance_list[verts_list.index(i)] >= radius*0.5:
                bmesh.ops.translate(bm, verts = bm.verts[i:i+1], vec = (0, 0, strength*0.01))
            elif distance_list[verts_list.index(i)] >= radius*0.25:
                bmesh.ops.translate(bm, verts = bm.verts[i:i+1], vec = (0, 0, strength*0.02))
            elif distance_list[verts_list.index(i)] >= radius*0.125:
                bmesh.ops.translate(bm, verts = bm.verts[i:i+1], vec = (0, 0, strength*0.05))
            else:
                bmesh.ops.translate(bm, verts = bm.verts[i:i+1], vec = (0, 0, strength*0.1))
        
        
    def get_Distance(one, another):
        '''
        Returns the distance between two verticies.
        one, another - BMverts to get distance
        ''' 
        result = math.sqrt((((one.co[0]-another.co[0])**2)+
                          ((one.co[1]-another.co[1])**2)+
                          ((one.co[2]-another.co[2])**2)))
                          
        return result
        
class object_transform:
    def translate(object, vector):
        '''translate object by name.
        object - object to transform
        vector - tuple with three floats. Each means x, y, z axis value
        '''
        bpy.context.view_layer.objects.active = bpy.data.objects[object]
        bpy.context.active_object.location[0] = vector[0]
        bpy.context.active_object.location[1] = vector[1]
        bpy.context.active_object.location[2] = vector[2]

    def resize(object, vector):
        '''translate object by name.
        object - object to transform
        vector - tuple with three floats. Each means x, y, z axis value
        '''
        bpy.context.view_layer.objects.active = bpy.data.objects[object]
        bpy.context.active_object.scale[0] = vector[0]
        bpy.context.active_object.scale[1] = vector[1]
        bpy.context.active_object.scale[2] = vector[2]

    def rotate(object, vector):
        '''translate object by name.
        object - object to transform
        vector - tuple with three floats. Each means x, y, z axis value
        '''
        bpy.context.view_layer.objects.active = bpy.data.objects[object]
        bpy.context.active_object.rotation_euler[0] = math.radians(vector[0])
        bpy.context.active_object.rotation_euler[1] = math.radians(vector[1])
        bpy.context.active_object.rotation_euler[2] = math.radians(vector[2])

class object_Gen: 
    def Street_Lamp():
        '''
        Create street lamp at location. Origin of the object is at middle of the bottom
        '''
        if "Street_Lamp" not in bpy.context.scene.objects:
            Street_Lamp_verts = []    
            Street_Lamp_vert_txt = open("Modeling/Street Lamp verts.txt", 'r')
            reading = 0
            for line in Street_Lamp_vert_txt:
                if reading%3 == 0:
                    x = float(line.strip())
                elif reading%3 == 1:
                    y = float(line.strip())
                elif reading%3 == 2:
                    z = float(line.strip())
                    Street_Lamp_verts.append((x, y, z))
                reading += 1
            Street_Lamp_vert_txt.close()

            Street_Lamp_faces = []
            Street_Lamp_face_txt = open("Modeling/Street Lamp faces.txt", "r")
            reading = 0
            for line in Street_Lamp_face_txt:
                if reading%4 == 0:
                    vert1 = int(line.strip())
                elif reading%4 == 1:
                    vert2 = int(line.strip())
                elif reading%4 == 2:
                    vert3 = int(line.strip())
                elif reading%4 == 3:
                    vert4 = int(line.strip())
                    Street_Lamp_faces.append((vert1, vert2, vert3, vert4))
                reading += 1
            Street_Lamp_face_txt.close()
            
            Street_Lamp_data = bpy.data.meshes.new("Street_Lamp")
            Street_Lamp_data.from_pydata(Street_Lamp_verts, [], Street_Lamp_faces)
            Street_Lamp_bm = bmesh.new()
            Street_Lamp_bm.from_mesh(Street_Lamp_data)
            Street_Lamp_bm.to_mesh(Street_Lamp_data)
            Street_Lamp_bm.free()
            Street_Lamp_obj = bpy.data.objects.new("Street_Lamp", Street_Lamp_data)
            bpy.context.collection.objects.link(Street_Lamp_obj)


            if "Street_Lamp_mat_Body" not in bpy.data.materials:
            
                Street_Lamp_mat_Body = bpy.data.materials.new(name = 'Street_Lamp_mat_Body')
                Street_Lamp_mat_Body.use_nodes = True
                Street_Lamp_mat_Body_nodes = Street_Lamp_mat_Body.node_tree.nodes
                Street_Lamp_mat_Body_nodes.clear()
                SLB_node_Output = Street_Lamp_mat_Body_nodes.new(type = 'ShaderNodeOutputMaterial')
                SLB_node_PrinBSDF = Street_Lamp_mat_Body_nodes.new(type = 'ShaderNodeBsdfPrincipled')
                SLB_node_PrinBSDF.inputs[0].default_value = (0.6, 0.17, 0.1, 1)   #BaseColor
                SLB_node_PrinBSDF.inputs[6].default_value = 0.9                  #Metalic
                SLB_node_PrinBSDF.inputs[9].default_value =  0.2                #Roughness
                SLB_node_Bump = Street_Lamp_mat_Body_nodes.new(type = 'ShaderNodeBump')
                SLB_node_Bump.inputs[0].default_value = 0.02    #Strength
                SLB_node_NoiseTex = Street_Lamp_mat_Body_nodes.new(type = 'ShaderNodeTexNoise')
                SLB_node_NoiseTex.inputs[2].default_value = 50    #Scale
                SLB_node_Mapping = Street_Lamp_mat_Body_nodes.new(type = 'ShaderNodeMapping')
                SLB_node_TexCoord = Street_Lamp_mat_Body_nodes.new(type = 'ShaderNodeTexCoord')

                Street_Lamp_mat_Body_nodes_links = Street_Lamp_mat_Body.node_tree.links
                Street_Lamp_mat_Body_nodes_links.new(SLB_node_PrinBSDF.outputs[0], 
                                                     SLB_node_Output.inputs[0])
                Street_Lamp_mat_Body_nodes_links.new(SLB_node_Bump.outputs[0], 
                                                     SLB_node_PrinBSDF.inputs[22])
                Street_Lamp_mat_Body_nodes_links.new(SLB_node_NoiseTex.outputs[0], 
                                                     SLB_node_Bump.inputs[2])
                Street_Lamp_mat_Body_nodes_links.new(SLB_node_Mapping.outputs[0], 
                                                     SLB_node_NoiseTex.inputs[0])
                Street_Lamp_mat_Body_nodes_links.new(SLB_node_TexCoord.outputs[3], 
                                                     SLB_node_Mapping.inputs[0])

                Street_Lamp_obj.data.materials.append(Street_Lamp_mat_Body)
            
            else:
                SLB_mat = bpy.data.materials['Street_Lamp_mat_Body']
                Street_Lamp_obj.data.materials.append(SLB_mat)

            if "Street_Lamp_mat_Glass" not in bpy.data.materials:

                Street_Lamp_mat_Glass = bpy.data.materials.new(name = 'Street_Lamp_mat_Glass')
                Street_Lamp_mat_Glass.use_nodes = True
                Street_Lamp_mat_Glass_nodes = Street_Lamp_mat_Glass.node_tree.nodes
                Street_Lamp_mat_Glass_nodes.clear()
                SLG_node_Output = Street_Lamp_mat_Glass_nodes.new(type = 'ShaderNodeOutputMaterial')
                SLG_node_GlassBSDF = Street_Lamp_mat_Glass_nodes.new(type = 'ShaderNodeBsdfGlass')
                SLG_node_GlassBSDF.inputs[0].default_value = (1, 0.84, 0.33, 1)    #Base Color
                SLG_node_GlassBSDF.inputs[1].default_value = 0.7                    #Roughness
    
                Street_Lamp_mat_Glass_nodes_links = Street_Lamp_mat_Glass.node_tree.links
                Street_Lamp_mat_Glass_nodes_links.new(SLG_node_GlassBSDF.outputs[0], 
                                                      SLG_node_Output.inputs[0])        
    
                Street_Lamp_obj.data.materials.append(Street_Lamp_mat_Glass)
                for i in range(584,592):
                    Street_Lamp_obj.data.polygons[i].material_index = 1
                for i in range(1328,1336):
                    Street_Lamp_obj.data.polygons[i].material_index = 1
            
            else:
                SLG_mat = bpy.data.materials['Street_Lamp_mat_Glass']
                Street_Lamp_obj.data.materials.append(SLG_mat)
                
                for i in range(584,592):
                    Street_Lamp_obj.data.polygons[i].material_index = 1
                for i in range(1328,1336):
                    Street_Lamp_obj.data.polygons[i].material_index = 1

            if "Street_Lamp_mat_Light" not in bpy.data.materials:
            
                Street_Lamp_mat_Light = bpy.data.materials.new(name = 'Street_Lamp_mat_Light')
                Street_Lamp_mat_Light.use_nodes = True
                Street_Lamp_mat_Light_nodes = Street_Lamp_mat_Light.node_tree.nodes
                Street_Lamp_mat_Light_nodes.clear()
                SLL_node_Output = Street_Lamp_mat_Light_nodes.new(type = 'ShaderNodeOutputMaterial')
                SLL_node_Emission = Street_Lamp_mat_Light_nodes.new(type = 'ShaderNodeEmission')
                SLL_node_Emission.inputs[1].default_value = 10

                Street_Lamp_mat_Light_nodes_links = Street_Lamp_mat_Light.node_tree.links
                Street_Lamp_mat_Light_nodes_links.new(SLL_node_Emission.outputs[0], 
                                                      SLL_node_Output.inputs[0])

                Street_Lamp_obj.data.materials.append(Street_Lamp_mat_Light)
                for i in range(544, 548):
                    Street_Lamp_obj.data.polygons[i].material_index = 2
                for i in range(1288, 1292):
                    Street_Lamp_obj.data.polygons[i].material_index = 2
                for i in range(2144, 2160):
                    Street_Lamp_obj.data.polygons[i].material_index = 2
                for i in range(2168, 2176):
                    Street_Lamp_obj.data.polygons[i].material_index = 2
            else:
                SLL_mat = bpy.data.materials['Street_Lamp_mat_Light']
                Street_Lamp_obj.data.materials.append(SLL_mat)
                for i in range(544, 548):
                    Street_Lamp_obj.data.polygons[i].material_index = 2
                for i in range(1288, 1292):
                    Street_Lamp_obj.data.polygons[i].material_index = 2
                for i in range(2144, 2160):
                    Street_Lamp_obj.data.polygons[i].material_index = 2
                for i in range(2168, 2176):
                    Street_Lamp_obj.data.polygons[i].material_index = 2

            bpy.context.view_layer.objects.active = bpy.data.objects["Street_Lamp"]
            for f in bpy.context.object.data.polygons:
                if f.index not in range(584,592):
                    if f.index not in range(1328,1336):
                        f.use_smooth = True
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].segments = 1

        else:
            bpy.data.objects["Street_Lamp"].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects["Street_Lamp"]
            bpy.ops.object.duplicate(linked=False)
            Street_Lamp_new = bpy.context.selected_objects[0].name
            
        for i in bpy.data.objects:
            i.select_set(False)

    def Land():
        '''
        Create land
        '''
        if "Land" not in bpy.context.scene.objects:
            Land_bm = bmesh.new()
            Land_data = bpy.data.meshes.new('Land')

            bmesh.ops.create_grid(Land_bm, size = 2, x_segments = 20, y_segments = 20)
            bmesh.ops.create_grid(Land_bm, size = 2, x_segments = 20, y_segments = 20)
            bmesh.ops.translate(Land_bm, verts = Land_bm.verts[441:882], vec = (0, 4, 0.05))
            vert = 0
            for i in range(0, 100):
                vert = random.randrange(0, 882)
                if vert not in range(378, 504):
                    bm_transform.proportional(Land_bm, vert, random.uniform(0.2, 0.5), 0.5)
            for i in range(0, 100):
                vert = random.randrange(0, 882)
                if vert not in range(378, 504):
                    bm_transform.proportional(Land_bm, vert, -random.uniform(0.3, 0.5), 0.5)

            Land_bm.to_mesh(Land_data)
            Land_bm.free()
            Land_obj = bpy.data.objects.new(Land_data.name, Land_data)
            bpy.context.collection.objects.link(Land_obj)

            for i in bpy.data.objects:
                if i.name.startswith("Land"):
                    bpy.context.view_layer.objects.active = bpy.data.objects[i.name]
                    for f in bpy.context.object.data.polygons:
                        f.use_smooth = True
                
                if len(Land_obj.data.materials) == 0:
                    if "forest_leaves_03" not in bpy.data.materials:
                        Land_mat1 = Image_Tex_Loader("forest_leaves_03", 2, False)
                        Land_obj.data.materials.append(Land_mat1)
                    else:
                        Land_mat1 = Image_Tex_Loader("forest_leaves_03", 2, False)
                        Land_obj.data.materials.append(Land_mat1)
                        
                    if "blue_floor_tiles_01" not in bpy.data.materials:
                        Land_mat2 = Image_Tex_Loader("blue_floor_tiles_01", 2, True)
                        Land_obj.data.materials.append(Land_mat2)
                        for i in range(0, 400):
                            Land_obj.data.polygons[i].material_index = 1
                    else:
                        Land_mat2 = Image_Tex_Loader("blue_floor_tiles_01", 2, True)
                        Land_obj.data.materials.append(Land_mat2)
                    
                        
        for i in bpy.data.objects:
            i.select_set(False)
            
    def Rock():
        '''
        Create Rock
        '''
        if "Rock" not in bpy.context.scene.objects:
            Rock_bm = bmesh.new()
            Rock_data = bpy.data.meshes.new('Rock')
            
            bmesh.ops.create_cube(Rock_bm, size = 0.1)
            bmesh.ops.translate(Rock_bm, verts = Rock_bm.verts[0:4], vec = (-2, 0, 0))
            bmesh.ops.translate(Rock_bm, verts = Rock_bm.verts[4:8], vec = (2, 0, 0))
            
            Rock_bm.to_mesh(Rock_data)
            Rock_bm.free()
            Rock_obj = bpy.data.objects.new(Rock_data.name, Rock_data)
            bpy.context.collection.objects.link(Rock_obj)
            
            if "Rock" not in bpy.data.materials:
                Rock_mat = Image_Tex_Loader("aerial_beach_02", 4.2, True)
                Rock_obj.data.materials.append(Rock_mat)
            
        for i in bpy.data.objects:
            i.select_set(False)
            

    def Tree(position):
        '''
        Create Tree
        position - tuple with three floats. Each means x, y, z axis position
        '''

        Tree_bm = bmesh.new()
        Tree_data = bpy.data.meshes.new('Tree')

        bmesh.ops.create_vert(Tree_bm, co = (0, 0, 0))
        bmesh.ops.extrude_face_region(Tree_bm, geom = Tree_bm.verts[0:1])
        Plank_Length = random.uniform(3, 4)
        Plank_angle_h = math.radians(random.randrange(80, 90))
        Plank_angle_b = math.radians(random.randrange(0, 360))
        bmesh.ops.translate(Tree_bm, verts = Tree_bm.verts[1:2], vec = (Plank_Length*math.cos(Plank_angle_h)*math.cos(Plank_angle_b),
                                                                        Plank_Length*math.cos(Plank_angle_h)*math.sin(Plank_angle_b),
                                                                        Plank_Length*math.sin(Plank_angle_h)))
        verts_per_branch = []
        new_verts_list = [[1]]
        new_verts = bm_transform.branch_creator(Tree_bm, 1, 2)
        verts_per_branch.append(len(new_verts))
        new_verts_list.append(new_verts)
        for i in range(2, 2 + len(new_verts_list[1])):
            new_verts = bm_transform.branch_creator(Tree_bm, Tree_bm.verts[i:i+1][0].index, 1.5)
            new_verts_list.append(new_verts)
        for i in range(2, len(new_verts_list)):
            for j in new_verts_list[i]:
                new_verts = bm_transform.branch_creator(Tree_bm, Tree_bm.verts[j:j+1][0].index, 1)
                new_verts_list.append(new_verts)

        Tree_bm.to_mesh(Tree_data)
        Tree_bm.free()
        Tree_obj = bpy.data.objects.new(Tree_data.name, Tree_data)
        bpy.context.collection.objects.link(Tree_obj)

        for i in bpy.data.objects:
            if i.name.startswith("Tree"):
                bpy.context.view_layer.objects.active = bpy.data.objects[i.name]
                if not bpy.context.object.modifiers:
                    bpy.ops.object.modifier_add(type='SKIN')
                    bpy.data.objects[i.name].data.skin_vertices[0].data[0].radius = (0.7, 0.7)
                    bpy.data.objects[i.name].data.skin_vertices[0].data[1].radius = (0.2, 0.2)
                    for j in new_verts_list[1]:
                        bpy.data.objects[i.name].data.skin_vertices[0].data[j].radius = (0.15, 0.15)
                    for j in range(0, len(new_verts_list[1])):
                        for k in new_verts_list[j+2]:
                            bpy.data.objects[i.name].data.skin_vertices[0].data[k].radius = (0.05, 0.05)

                    if len(new_verts_list[1]) == 2:
                        for j in range(0, len(new_verts_list[2]) + len(new_verts_list[3])):
                            for k in new_verts_list[j+4]:
                                bpy.data.objects[i.name].data.skin_vertices[0].data[k].radius = (0.01, 0.01)
                    if len(new_verts_list[1]) == 3:
                        for j in range(0, len(new_verts_list[2]) + len(new_verts_list[3]) + len(new_verts_list[4])):
                            for k in new_verts_list[j+5]:
                                bpy.data.objects[i.name].data.skin_vertices[0].data[k].radius = (0.05,  0.05)

                    bpy.ops.object.modifier_add(type='SUBSURF')
                    bpy.context.object.modifiers["Subdivision"].levels = 2
                    tex = bpy.data.textures.new("Clouds", 'CLOUDS')
                    bpy.ops.object.modifier_add(type='DISPLACE')
                    bpy.context.object.modifiers["Displace"].texture = bpy.data.textures['Clouds']
                    bpy.context.object.modifiers["Displace"].strength = 0.1
                    Displace_Vertext_Group = bpy.context.active_object.vertex_groups.new(name = 'Stump')
                    Displace_Vertext_Group.add([0, 1, 2, 3, 4], 1, 'ADD')
                    bpy.context.object.modifiers["Displace"].vertex_group = "Stump"
                    Branch_Group = bpy.context.active_object.vertex_groups.new(name = 'Branch')
                    Branch_Group.add([0, 1], 1, 'ADD')
                    bpy.ops.object.modifier_apply(modifier = "Skin")
                    
                    object_transform.resize(i.name, (0.25, 0.25, 0.25))
                    object_transform.translate(i.name, position)   
                    for f in bpy.context.object.data.polygons:
                        f.use_smooth = True            
                               
                    if len(Tree_obj.data.materials) == 0:
                        if "bark_brown_02" not in bpy.data.materials:
                            Tree_mat1 = Image_Tex_Loader("bark_brown_02", 1, True)
                            Tree_obj.data.materials.append(Tree_mat1)
                        else:
                            Tree_mat1 = bpy.data.materials["bark_brown_02"]
                            Tree_obj.data.materials.append(Tree_mat1)
                        
                               
        for i in bpy.data.objects:
            i.select_set(False)
            
    def Branch():
        '''
        Create a branch
        '''
        if "Small_Branch" not in bpy.context.scene.objects:
            Small_Branch_verts = []    
            Small_Branch_vert_txt = open("Modeling/Small Branch verts.txt", 'r')
            reading = 0
            for line in Small_Branch_vert_txt:
                if reading%3 == 0:
                    x = float(line.strip())
                elif reading%3 == 1:
                    y = float(line.strip())
                elif reading%3 == 2:
                    z = float(line.strip())
                    Small_Branch_verts.append((x, y, z))
                reading += 1
            Small_Branch_vert_txt.close()

            Small_Branch_faces = []
            Small_Branch_face_txt = open("Modeling/Small Branch faces.txt", "r")
            reading = 0
            for line in Small_Branch_face_txt:
                if reading%4 == 0:
                    vert1 = int(line.strip())
                elif reading%4 == 1:
                    vert2 = int(line.strip())
                elif reading%4 == 2:
                    vert3 = int(line.strip())
                elif reading%4 == 3:
                    vert4 = int(line.strip())
                    Small_Branch_faces.append((vert1, vert2, vert3, vert4))
                reading += 1
            Small_Branch_face_txt.close()

            Small_Branch_data = bpy.data.meshes.new("Small_Branch")
            Small_Branch_data.from_pydata(Small_Branch_verts, [], Small_Branch_faces)
            Small_Branch_bm = bmesh.new()
            Small_Branch_bm.from_mesh(Small_Branch_data)
            Small_Branch_bm.to_mesh(Small_Branch_data)
            Small_Branch_bm.free()
            Small_Branch_obj = bpy.data.objects.new("Small_Branch", Small_Branch_data)
            bpy.context.collection.objects.link(Small_Branch_obj)
            
            for i in bpy.data.objects:
                if i.name.startswith("Small_Branch"):
                    object_transform.translate(i.name, (0, 0, -10))
            if len(Small_Branch_obj.data.materials) == 0:
                Small_Branch_obj.data.materials.append(bpy.data.materials["bark_brown_02"])
                    
        for i in bpy.data.objects:
            i.select_set(False)
            
    
    def Branch_Leaves():
        '''
        Create a branch with leaves
        '''
        if "Branch_leaves" not in bpy.context.scene.objects:
            Small_Branch_verts = []    
            Small_Branch_vert_txt = open("Modeling/Small branch leaf verts.txt", 'r')
            reading = 0
            for line in Small_Branch_vert_txt:
                if reading%3 == 0:
                    x = float(line.strip())
                elif reading%3 == 1:
                    y = float(line.strip())
                elif reading%3 == 2:
                    z = float(line.strip())
                    Small_Branch_verts.append((x, y, z))
                reading += 1
            Small_Branch_vert_txt.close()

            Small_Branch_faces = []
            Small_Branch_face_txt = open("Modeling/Small branch leaf faces.txt", "r")
            reading = 0
            for line in Small_Branch_face_txt:
                if reading%4 == 0:
                    vert1 = int(line.strip())
                elif reading%4 == 1:
                    vert2 = int(line.strip())
                elif reading%4 == 2:
                    vert3 = int(line.strip())
                elif reading%4 == 3:
                    vert4 = int(line.strip())
                    Small_Branch_faces.append((vert1, vert2, vert3, vert4))
                reading += 1
            Small_Branch_face_txt.close()

            Small_Branch_data = bpy.data.meshes.new("Branch_leaves")
            Small_Branch_data.from_pydata(Small_Branch_verts, [], Small_Branch_faces)
            Small_Branch_bm = bmesh.new()
            Small_Branch_bm.from_mesh(Small_Branch_data)
            Small_Branch_bm.to_mesh(Small_Branch_data)
            Small_Branch_bm.free()
            Small_Branch_obj = bpy.data.objects.new("Branch_leaves", Small_Branch_data)
            bpy.context.collection.objects.link(Small_Branch_obj)
            
            for i in bpy.data.objects:
                if i.name.startswith("Branch_leaves"):
                    object_transform.translate(i.name, (0, 0, -10))
            
            if len(Small_Branch_obj.data.materials) == 0:
                
                Small_Branch_obj.data.materials.append(bpy.data.materials["bark_brown_02"])
                
                path = os.getcwd()
                if "Leaf" not in bpy.data.materials:
                    Leaf_mat = bpy.data.materials.new(name = 'Leaf')
                    Leaf_mat.use_nodes = True
                    Leaf_mat_nodes = Leaf_mat.node_tree.nodes
                    Leaf_mat_nodes.clear()
                    Leaf_node_Output = Leaf_mat_nodes.new(type = 'ShaderNodeOutputMaterial')
                    Leaf_node_PrinBSDF = Leaf_mat_nodes.new(type = 'ShaderNodeBsdfPrincipled')
                    Leaf_node_PrinBSDF.inputs[9].default_value = 0.1
                    Leaf_node_MixRGB = Leaf_mat_nodes.new(type = 'ShaderNodeMixRGB')
                    Leaf_node_MixRGB.inputs[2].default_value = (0.09, 0.09, 0.09, 1)
                    Leaf_node_Image = Leaf_mat_nodes.new(type = 'ShaderNodeTexImage')
                    Leaf_node_Image.image = bpy.data.images.load(path + "\\Textures\\Leaf.png")

                    
                    Leaf_links = Leaf_mat.node_tree.links
                    Leaf_links.new(Leaf_node_Output.inputs[0],
                                   Leaf_node_PrinBSDF.outputs[0])
                    Leaf_links.new(Leaf_node_PrinBSDF.inputs[0],
                                   Leaf_node_MixRGB.outputs[0])
                    Leaf_links.new(Leaf_node_MixRGB.inputs[1],
                                   Leaf_node_Image.outputs[0])
                    
                    Small_Branch_obj.data.materials.append(Leaf_mat)
                else:
                    Small_Branch_obj.data.materials.append(bpy.data.materials["Leaf"])
                                
                for i in range(50, 110):
                    Small_Branch_obj.data.polygons[i].material_index = 1
                    
            uv_txt = open("Modeling/Small branch leaf uv.txt", "r")
            reading = 0
            x_list = []
            y_list = []
            
            for line in uv_txt:
                if reading%2 == 0:
                    x_list.append(float(line.strip()))
                elif reading%2 == 1:
                    y_list.append(float(line.strip()))
                reading += 1
            uv_txt.close()
            
            bpy.context.view_layer.objects.active = bpy.data.objects["Branch_leaves"]
            uv = bpy.context.active_object.data.uv_layers.new()
            
            for loop in range(len(bpy.context.object.data.loops)):
                bpy.context.object.data.uv_layers.active.data[loop].uv = (x_list[loop], y_list[loop])
                    
        for i in bpy.data.objects:
            i.select_set(False)
            
    def Rain_Emitter():
        '''
        Create Rain Emitter
        '''
        if "Emitter_Rain" not in bpy.context.scene.objects:
            Rain_Emitter_bm = bmesh.new()
            Rain_Emitter_data = bpy.data.meshes.new('Emitter_Rain')
            
            bmesh.ops.create_grid(Rain_Emitter_bm, size = 1)
            
            Rain_Emitter_bm.to_mesh(Rain_Emitter_data)
            Rain_Emitter_bm.free()
            Rain_Emitter_obj = bpy.data.objects.new(Rain_Emitter_data.name, Rain_Emitter_data)
            bpy.context.collection.objects.link(Rain_Emitter_obj)
            
            for i in bpy.data.objects:
                if i.name.startswith("Emitter_Rain"):
                    object_transform.translate(i.name, (0.5, 2, 5))
                    object_transform.rotate(i.name, (0, 180, 0))
                    
            Zero_Alpha_mat = bpy.data.materials.new(name = 'Zero Alpha')
            Zero_Alpha_mat.use_nodes = True
            Zero_Alpha_mat_nodes = Zero_Alpha_mat.node_tree.nodes
            Zero_Alpha_mat_nodes.clear()
            ZA_node_Output = Zero_Alpha_mat_nodes.new(type = 'ShaderNodeOutputMaterial')
            ZA_node_PrinBSDF = Zero_Alpha_mat_nodes.new(type = 'ShaderNodeBsdfPrincipled')
            ZA_node_PrinBSDF.inputs[21].default_value = 0
            
            Zero_Alpha_mat_nodes_links = Zero_Alpha_mat.node_tree.links
            Zero_Alpha_mat_nodes_links.new(ZA_node_PrinBSDF.outputs[0], 
                                           ZA_node_Output.inputs[0])        
            Rain_Emitter_obj.data.materials.append(Zero_Alpha_mat)
            
        for i in bpy.data.objects:
            i.select_set(False)
            
    def Rain():
        '''
        Create Rain
        '''
        if "Rain" not in bpy.context.scene.objects:
            Rain_bm = bmesh.new()
            Rain_data = bpy.data.meshes.new('Rain')
            
            bmesh.ops.create_cube(Rain_bm, size = 1)
            
            Rain_bm.to_mesh(Rain_data)
            Rain_bm.free()
            Rain_obj = bpy.data.objects.new(Rain_data.name, Rain_data)
            bpy.context.collection.objects.link(Rain_obj)
            
            for i in bpy.data.objects:
                if i.name.startswith("Rain"):
                    object_transform.translate(i.name, (0, 0, -10))
                    bpy.context.view_layer.objects.active = bpy.data.objects[i.name]
                    bpy.ops.object.modifier_add(type='SUBSURF')
                    
                    
            Water = bpy.data.materials.new(name = 'Water')
            Water.use_nodes = True
            Water_nodes = Water.node_tree.nodes
            Water_nodes.clear()
            Water_nodes_Output = Water_nodes.new(type = 'ShaderNodeOutputMaterial')
            Water_nodes_GlassBSDF = Water_nodes.new(type = 'ShaderNodeBsdfGlass')
            Water_nodes_GlassBSDF.inputs[2].default_value = 1.333
            
            
            Water_nodes_links = Water.node_tree.links
            Water_nodes_links.new(Water_nodes_GlassBSDF.outputs[0], 
                                  Water_nodes_Output.inputs[0])        
            Rain_obj.data.materials.append(Water)
            
        for i in bpy.data.objects:
            i.select_set(False)
                                
class environment:            
    
    def Tree_Branch(Bool):
        '''
        Add particle system to tree to make small branches
        Bool - Booleen wether you want to create leaves
        '''
        if Bool == False:
            for i in bpy.data.objects:
                if i.name.startswith("Small_Branch"):
                    Branch = i
                    
            for i in bpy.data.objects:
                if i.name.startswith("Tree"):
                    bpy.context.view_layer.objects.active = bpy.data.objects[i.name]
                                                        
                    if len(bpy.context.active_object.particle_systems) == 0:
                        bpy.context.active_object.modifiers.new("Leaf", type='PARTICLE_SYSTEM')
                        settings = bpy.context.active_object.particle_systems[0].settings
                        settings.type = "HAIR"
                        settings.render_type = "OBJECT"
                        settings.instance_object = Branch
                        settings.count = 20
                        bpy.data.objects[i.name].particle_systems["Leaf"].vertex_group_density = "Branch"
                        bpy.data.objects[i.name].particle_systems["Leaf"].invert_vertex_group_density = True
                        settings.use_advanced_hair = True
                        settings.use_rotations = True
                        settings.rotation_mode = "NOR"
                        settings.rotation_factor_random = 0.7
                        settings.particle_size = 0.07
                        settings.size_random = 1
                        
        if Bool == True:
            for i in bpy.data.objects:
                if i.name.startswith("Branch_leaves"):
                    Branch = i
                
            for i in bpy.data.objects:
                if i.name.startswith("Tree"):
                    bpy.context.view_layer.objects.active = bpy.data.objects[i.name]
                                                        
                    if len(bpy.context.active_object.particle_systems) == 0:
                        bpy.context.active_object.modifiers.new("Leaf", type='PARTICLE_SYSTEM')
                        settings = bpy.context.active_object.particle_systems[0].settings
                        settings.type = "HAIR"
                        settings.render_type = "OBJECT"
                        settings.instance_object = Branch
                        settings.count = 20
                        bpy.data.objects[i.name].particle_systems["Leaf"].vertex_group_density = "Branch"
                        bpy.data.objects[i.name].particle_systems["Leaf"].invert_vertex_group_density = True
                        settings.use_advanced_hair = True
                        settings.use_rotations = True
                        settings.rotation_mode = "NOR"
                        settings.rotation_factor_random = 0.7
                        settings.particle_size = 0.07
                        settings.size_random = 1
                                            
    def Rain(amount):
        for i in bpy.data.objects:
            if i.name.startswith("Rain"):
                Rain = i
                
        for i in bpy.data.objects:
            if i.name.startswith("Emitter_Rain"):
                bpy.context.view_layer.objects.active = bpy.data.objects[i.name]
                                                    
                if len(bpy.context.active_object.particle_systems) == 0:
                    bpy.context.active_object.modifiers.new("Rain", type='PARTICLE_SYSTEM')
                    settings = bpy.context.active_object.particle_systems[0].settings
                    settings.type = "EMITTER"
                    settings.render_type = "OBJECT"
                    settings.instance_object = Rain
                    settings.count = int(3000*amount)
                    settings.normal_factor = 10
                    settings.frame_start = -10
                    settings.frame_end = 10
                    settings.lifetime = 10
                    settings.particle_size = 0.025
                    settings.size_random = 1
                    
        if amount != 0:
            bpy.ops.mesh.primitive_plane_add(size = 4)
            for i in bpy.data.objects:
                if i.name.startswith("Plane"):
                    object_transform.translate(i.name, (0, 0, -0.005))
                    i.data.materials.append(bpy.data.materials["Water"])
                    
        if amount >= 0.7:
            bpy.ops.mesh.primitive_cube_add(size = 4)
            for i in bpy.data.objects:
                if i.name.startswith("Cube"):
                    fog = i
            object_transform.translate(fog.name, (0, 1.5, 0))
            if "Fog" not in bpy.data.materials:
                Fog_mat = bpy.data.materials.new(name = 'Fog')
                Fog_mat.use_nodes = True
                Fog_mat_nodes = Fog_mat.node_tree.nodes
                Fog_mat_nodes.clear()
                Fog_Output = Fog_mat_nodes.new(type = 'ShaderNodeOutputMaterial')
                Fog_Volume = Fog_mat_nodes.new(type = 'ShaderNodeVolumePrincipled')
                Fog_Volume.inputs[2].default_value = amount*0.4
                
                Fog_links = Fog_mat.node_tree.links
                Fog_links.new(Fog_Output.inputs[1], 
                              Fog_Volume.outputs[0])        
                bpy.data.objects["Cube"].data.materials.append(Fog_mat)
                
                
                    
    def Sun(Time):            
            
            light_data = bpy.data.lights.new(name="Sun_data", type='SUN')
            light_data.energy = ((Time-12)**2)/36*(-1) + 5
            if 4<=Time<=6 or 17<=Time<=19:
                light_data.color = (1, 0.227, 0.011)
                bpy.data.materials["Street_Lamp_mat_Light"].node_tree.nodes["Emission"].inputs[1].default_value = 0
            elif 6<Time<17:
                light_data.color = (1, 1, 1)
                bpy.data.materials["Street_Lamp_mat_Light"].node_tree.nodes["Emission"].inputs[1].default_value = 0
            else:
                light_data.color = (0.5, 0.732, 1)

            light_object = bpy.data.objects.new(name="Sun", object_data=light_data)
            bpy.context.collection.objects.link(light_object)
            
            for i in bpy.data.objects:
                if i.name.startswith("Sun"):
                    i.rotation_euler[1] = math.radians((Time - 12)*80/12)
            
            for i in bpy.data.objects:
                i.select_set(False)
                
    def World(time ,amount):
        path = os.getcwd()
        
        World_tree = bpy.context.scene.world.node_tree
        World_node = World_tree.nodes
        World_node.clear()
        
        World_Output = World_node.new(type= "ShaderNodeOutputWorld")
        World_Back = World_node.new(type = "ShaderNodeBackground")
        World_MixRGB = World_node.new(type = "ShaderNodeMixRGB")
        World_Environ = World_node.new(type = "ShaderNodeTexEnvironment")
        World_Mapping = World_node.new(type = "ShaderNodeMapping")
        World_TexCoor = World_node.new(type = "ShaderNodeTexCoord")
        World_MixRGB.inputs[0].default_value = amount*0.7
        World_MixRGB.inputs[2].default_value = (0, 0, 0, 1)
        
        if 6<time<17:
            World_Environ.image = bpy.data.images.load(path + "\\Textures\\delta_2_2k.exr")
            World_Mapping.inputs[2].default_value = (0, 0, -math.radians(70))
        elif 4<=time<=6 or 17<=time<=19:
            World_Environ.image = bpy.data.images.load(path + "\\Textures\\kiara_1_dawn_2k.exr")
            World_Mapping.inputs[2].default_value = (0, 0, -math.radians(70))
        else:
            World_Environ.image = bpy.data.images.load(path + "\\Textures\\satara_night_no_lamps_2k.exr")
            World_Mapping.inputs[2].default_value = (0, 0, -math.radians(70))
            
            
        
        links = World_tree.links
        links.new(World_Output.inputs[0], World_Back.outputs[0])
        links.new(World_Back.inputs[0], World_MixRGB.outputs[0])
        links.new(World_MixRGB.inputs[1], World_Environ.outputs[0])
        links.new(World_Environ.inputs[0], World_Mapping.outputs[0])
        links.new(World_Mapping.inputs[0], World_TexCoor.outputs[0])
        
        
            

def Image_Tex_Loader(Tex, scale, ver):
    '''
    Create material with image texure. Returns created material as Material type.
    Tex - file name.
    scale - Scale of mapping node
    ver - Booleen which version to use.
    '''
    path = os.getcwd()
    diff = path + "\\Textures\\" + Tex + "_2k\\" + Tex + "_diff_2k.jpg"
    disp = path + "\\Textures\\" + Tex + "_2k\\" + Tex + "_disp_2k.png"
    nor = path + "\\Textures\\" + Tex + "_2k\\" + Tex + "_nor_gl_2k.exr"
    if ver == True:
        rough = path + "\\Textures\\" + Tex + "_2k\\" + Tex + "_rough_2k.jpg"
    elif ver == False:
        rough = path + "\\Textures\\" + Tex + "_2k\\" + Tex + "_rough_2k.exr"
        
    Mat = bpy.data.materials.new(name = Tex)
    Mat.use_nodes = True
    Mat_nodes = Mat.node_tree.nodes
    Mat_nodes.clear()
    Mat_nodes_Output = Mat_nodes.new(type = 'ShaderNodeOutputMaterial')
    Mat_nodes_PrinBSDF = Mat_nodes.new(type = 'ShaderNodeBsdfPrincipled')
    Mat_nodes_diff = Mat_nodes.new(type = 'ShaderNodeTexImage')
    Mat_nodes_disp = Mat_nodes.new(type = 'ShaderNodeTexImage')
    Mat_nodes_nor = Mat_nodes.new(type = 'ShaderNodeTexImage')
    Mat_nodes_rough = Mat_nodes.new(type = 'ShaderNodeTexImage')
    Mat_nodes_normap = Mat_nodes.new(type = 'ShaderNodeNormalMap')
    Mat_nodes_mapping = Mat_nodes.new(type = 'ShaderNodeMapping')
    Mat_nodes_texcoor = Mat_nodes.new(type = 'ShaderNodeTexCoord')
    
    Mat_nodes_mapping.inputs[3].default_value = (scale, scale, scale)
    
    Mat_nodes_diff.image = bpy.data.images.load(diff, check_existing=True)
    Mat_nodes_disp.image = bpy.data.images.load(disp)
    Mat_nodes_nor.image = bpy.data.images.load(nor)
    Mat_nodes_rough.image = bpy.data.images.load(rough)
    
    Mat_links = Mat.node_tree.links
    Mat_links.new(Mat_nodes_Output.inputs[0],
                  Mat_nodes_PrinBSDF.outputs[0])
    Mat_links.new(Mat_nodes_PrinBSDF.inputs[0],
                  Mat_nodes_diff.outputs[0])
    Mat_links.new(Mat_nodes_PrinBSDF.inputs[9],
                  Mat_nodes_rough.outputs[0])
    Mat_links.new(Mat_nodes_PrinBSDF.inputs[22],
                  Mat_nodes_nor.outputs[0])
    Mat_links.new(Mat_nodes_Output.inputs[2],
                  Mat_nodes_normap.outputs[0])
    Mat_links.new(Mat_nodes_normap.inputs[0],
                  Mat_nodes_disp.outputs[0])
    Mat_links.new(Mat_nodes_diff.inputs[0],
                  Mat_nodes_mapping.outputs[0])
    Mat_links.new(Mat_nodes_disp.inputs[0],
                  Mat_nodes_mapping.outputs[0])
    Mat_links.new(Mat_nodes_nor.inputs[0],
                  Mat_nodes_mapping.outputs[0])
    Mat_links.new(Mat_nodes_rough.inputs[0],
                  Mat_nodes_mapping.outputs[0])
    Mat_links.new(Mat_nodes_mapping.inputs[0],
                  Mat_nodes_texcoor.outputs[3])
                  
    return Mat
                    
            
object_Gen.Land()
object_Gen.Rock()
for i in bpy.data.objects:
    if i.name.startswith("Rock"):
        object_transform.translate(i.name, (0, 2, 0.01))
        
object_Gen.Street_Lamp()
for i in bpy.data.objects:
    if i.name.startswith("Street_Lamp"):
        object_transform.translate(i.name, (0.5, 1.5, -0.001))
        
for i in range(20):
    Tree_pos_x = random.uniform(-1, 2)
    Tree_pos_y = random.uniform(-1.75, 2)
    object_Gen.Tree((Tree_pos_x, 4 + Tree_pos_y, -0.15))
    
object_Gen.Branch()
object_Gen.Branch_Leaves()
object_Gen.Rain_Emitter()
object_Gen.Rain()

print("Base Created")

class EnvironmentOperator(bpy.types.Operator):
    bl_idname = "object.environment"
    bl_label = "Environment Settings"

    Time : bpy.props.IntProperty(name = "Time", default = 12, min = 0, max = 24)
    Rain_amount : bpy.props.FloatProperty(name = "Amount of rain", default = 0, min = 0, max = 1)
    Leaf : bpy.props.BoolProperty(name = "Create Leaf?", default = False)

    def execute(self, context):       
         
        environment.Sun(self.Time)
        environment.World(self.Time, self.Rain_amount)
        environment.Tree_Branch(self.Leaf)
        environment.Rain(self.Rain_amount)
        
        self.report({'INFO'}, "Finished")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

bpy.utils.register_class(EnvironmentOperator)

bpy.ops.object.environment('INVOKE_DEFAULT')

print("Moedling Completed")

bpy.ops.object.camera_add()
bpy.context.scene.camera = bpy.context.object

bpy.data.objects["Camera"].location[0] = 0.5
bpy.data.objects["Camera"].location[1] = -1.35
bpy.data.objects["Camera"].location[2] = 0.9
bpy.data.objects["Camera"].rotation_euler[0] = math.radians(90)

bpy.data.scenes["Scene"].render.engine = "CYCLES"
bpy.data.scenes["Scene"].render.use_motion_blur = True
bpy.data.scenes["Scene"].render.resolution_x = 1440
bpy.data.scenes["Scene"].render.resolution_y = 1920

bpy.data.scenes["Scene"].render.filepath = os.getcwd() + "\\Results"
bpy.data.scenes["Scene"].render.image_settings.file_format = "JPEG"

print("Press F12 to start rendering")