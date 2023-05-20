import bpy
import bmesh

#object must be a mesh and in EditMode
mesh = bpy.context.view_layer.objects.active.data

def to_txt(name):
    bm = bmesh.from_edit_mesh(mesh)
    verts = []
    faces = []

    text1 = open(name + " verts.txt", "w")
    for vert in bm.verts:
        verts.append(vert.co)
    for i in verts:
        for j in range(0, 3):
            text1.write(str(i[j]))
            text1.write('\n')
    text1.close()

    text2 = open(name + " faces.txt", "w")
    for f in bm.faces:
        for v in f.verts:
            text2.write(str(v.index))
            text2.write('\n')
    text2.close()

    print("Done")
    
to_txt("Street Lamp")