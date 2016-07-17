import bpy
import numpy as np

#Blender 2.74


_weight = 1 # weight


def MakePolyLine(obj_name, 
                curve_name, 
                pts):
                    
    #this is some generic Blender tutorial code
                     
    curve_data = bpy.data.curves.new(name=curve_name, 
                                    type='CURVE')
    curve_data.dimensions = '3D'
    
    obj_data = bpy.data.objects.new(obj_name, 
                                    curve_data)
    bpy.context.scene.objects.link(obj_data)

    polyline = curve_data.splines.new('POLY')
    #add the 'empty' pts first
    polyline.points.add(len(pts)-1)
    for k,pt in enumerate(pts):
        x, y, z = pt
        polyline.points[k].co = (x, y, z, _weight)
    
    #I added the return 
    return obj_data
        
def make_spirals(num_spirals=10,
                max_z=5,
                min_radius=.5,
                max_radius=10,
                bevel_name="Bevel"):
    
    #uses numpy so bypasses Blender mathutils
    
    for rr in np.linspace(max_radius, min_radius, num_spirals):
        
        max_t = 2*max_z/rr**2
        T = np.linspace(-2*max_t, max_t, 200)
        #not very efficient but readable
        X = rr*np.cos(T)
        Y = rr*np.sin(T)
        Z = .5*(rr*rr)*T

        pts = [v[:] for v in zip(X,Y,Z)]
        
        obj = MakePolyLine("Spiral", 
                          "spiral_curve", 
                          pts)    
        add_bevel(obj)
       
        if rr > 1: 
            mk_copies_curve(obj)
            

    
def make_seg(v2,v1,npts = 20):
    '''linear interpolation v1 -> v2'''
    pts =np.zeros((3,npts))
    for k in range(3):
        pts[k] = np.linspace(v1[k],v2[k],npts)
    return pts.T


def lift(pts, 
        z0=-20):
    '''pts - list of np.array
     does  an numerical integration 
     modifying pts[][2] in place
     esult is a horizontal curve'''

    z = z0
    pts[0][2] = z
    for k,x in enumerate(pts[:-1]):
        pts[k+1][2] = z
        vv = pts[k+1] - x
        zz = -.5*(vv[0]*x[1] - vv[1]*x[0]) 
        z += zz
        
def add_lift(corners,
            bevel_name="Bevel"):  
 
    #have to make sure that the endpoints aren't overrepresented
    #so only do make_seg(y,x)[:-1,:] 
    segs = [make_seg(y,x)[:-1,:] for x,y in zip(corners,corners[1:])]
    pts  = []
    for seg in segs:
        pts.extend(seg)
    lift(pts)
    obj = MakePolyLine("lift", 
                        "lift_curve", 
                        pts)    
    add_bevel(obj)
    
def   spiral_corners(rr=1., 
                    rpt =2):
    corners = [ np.array([1,-1,0]),
               np.array([1,1,0]),
               np.array([-1,1,0]),
               np.array([-1,-1,0])]
               
    corners = [rr*v for v in corners]
               
    for  x in range(rpt):
        corners.extend(corners)
        
    return corners

   
            
def make_geodesic(num=10,
                  z0=0,
                  resolution=200,
                bevel_name="Bevel"):
    
    #uses numpy and bypasses mathutils
    
    radii = reversed([.125*2**k for k in range(num)])
    T = np.linspace(0, 2*np.pi, resolution)
    for rr in radii:
        
        #not very efficient but readable
        #you take a sqrt of rr
        X = np.sqrt(rr)*(1 - np.cos(T))
        Y = -np.sqrt(rr)*np.sin(T)
        Z = rr*(T - np.sin(T))/2 + z0
        
        T = 2*T
    
        pts = [v[:] for v in zip(X,Y,Z)]
        
        obj = MakePolyLine("geodesic", 
                          "geodesic_curve", 
                          pts)    
        add_bevel(obj)
       
#        if rr > 1: 
#            mk_copies_curve(obj)
            
def add_bevel(obj,
              bevel_name='Bevel'):
     #set the bevel object
    try:
        curve = obj.data
        curve.dimensions = '3D'
        curve.bevel_object = bpy.data.objects.get(bevel_name) 
    except:
        print('*warning* no Bevel')

def mk_copies_curve(obj,
                    num=4):
            
    for k in range(1,num):
        #this should take a parameter
        #make a copy and rotate it
        new_name = obj.name + '_rot%d'%(int(k*360/num))
        curve = bpy.data.curves.new(name=new_name, 
                                   type='CURVE')
     
        ob = bpy.data.objects.new(new_name, 
                                  curve)
        bpy.context.scene.objects.link(ob)
        ob.data = obj.data.copy() 
        ob.rotation_euler = (0,0,k*np.pi/num)


if False:
    make_spirals(num_spirals=5,
                max_z=10,
                min_radius=.5,
                max_radius=3,
                bevel_name="Bevel")
                
 
make_geodesic(num = 7,
               z0=-15)


