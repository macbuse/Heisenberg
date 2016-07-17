
import bpy
import numpy as np

from mathutils import Matrix

#make horizontal distribution
#Blender 2.7*
    
def gs_3D(X):
    '''custom Gram-Schmidt'''
    A = X/np.linalg.norm(X)
    B = np.array([-X[1],X[0],0])
    if np.linalg.norm(B) < .001:
        B = np.array([1,0,0])
    else:
        B = B/np.linalg.norm(B)    
    C = np.cross(A,B)
    
    return np.array([A,B,C])
    

zs = np.linspace(-5,3,4)
xs = np.linspace(-5,5, 5)
ys = xs
#np.linspace(-10,10,10)



X,Y,Z = np.meshgrid(xs,ys,zs)

X = X.ravel()
Y = Y.ravel()
Z = Z.ravel()

centers = zip(X,Y,Z)
    
ex = np.array([1,0,0])
ey = np.array([0,1,0])

rr = .75
for cc in centers:
    x,y,z = cc
    vv = [x,y,z]
    ehn = np.array([.5*y,-.5*x,1])
    
    bpy.ops.mesh.primitive_plane_add(location = vv[:]) 
    bb = bpy.context.scene.objects.active
    
    X = np.array([ehn,ex,ey])
    X = gs_3D(ehn)
    X = Matrix([X[k] for k in [1,2,0]])
    X.transpose()
    bb.scale = [rr,rr,rr]
    bb.rotation_euler = X.to_euler()[:]

     

