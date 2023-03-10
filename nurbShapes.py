import pymel.core as pm



def nurbCube(name, size):

    curve_points = [(0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5),
                    (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5),
                    (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5),
                    (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5),
                    (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5),
                    (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5),
                    (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5)]

    knots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    curve = pm.curve(d=1, p=curve_points, k=knots, n=name)
    curve.setAttr('s',(size,size,size))
    pm.makeIdentity(curve, apply=True, t=1, r=1, s=1, n=0, pn=1)
    pm.select(cl=True)

    return curve

def nurbSphere(name, radius):

    circle1 = pm.circle(nr=(1, 0, 0), r=radius, n=name)[0]
    circle2 = pm.circle(nr=(0, 1, 0), r=radius)[0]
    circle3 = pm.circle(nr=(0, 0, 1), r=radius)[0]
    # Parent the shapes of circle2 and circle3 to circle1
    pm.parent(circle2.getShape(), circle1, r=True, s=True)
    pm.parent(circle3.getShape(), circle1, r=True, s=True)

    # Delete the empty circle2 and circle3 transforms
    pm.delete(circle2)
    pm.delete(circle3)
    pm.makeIdentity(circle1, apply=True, t=1, r=1, s=1, n=0, pn=1)
    pm.select(clear=True)

    return circle1

def nurbPin(name, radius):
    # Create the ring circle
    Sphere = nurbSphere(name, radius)

    # Create the pointer curve
    pointer = pm.curve(n="pin", d=3, p=[(0, 0, radius), (0, 0, radius * 2), (0, 0, radius * 3.5), (0, 0, radius * 5)])

    # Parent the ring and pointer curves together
    pm.parent(pointer.getShape(), Sphere, r=True, s=True)
    pm.delete(pointer)

    # Freeze the transforms of the pointer curve
    pm.makeIdentity(Sphere, apply=True, t=1, r=1, s=1, n=0, pn=1)

    # Clear the selection
    pm.select(clear=True)

    return Sphere

def nurbSquare(name, size):

    points = [(1, 0, 1), (1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1)]
    squareCurve = pm.curve(p=points, d=1, n=name)
    squareCurve.setAttr('s',(size,size,size))
    pm.makeIdentity(squareCurve, apply=True, t=1, r=1, s=1, n=0, pn=1)
    return squareCurve


def nurbArrow(name, size):

    points = [(4, 0, 0), (0, 0, 4), (-4, 0, 0), (-2, 0, 0), (-2, 0, -3), (2, 0, -3), (2, 0, 0), (4, 0, 0)]
    arrow_curve = pm.curve(n=name, p=points, d=1, k=[0, 1, 2, 3, 4, 5, 6, 7])
    arrow_curve.setAttr('s',(size,size,size))
    pm.makeIdentity(arrow_curve, apply=True, t=1, r=1, s=1, n=0, pn=1)
    return(arrow_curve)




shapes = { 'cube': nurbCube, 'square':nurbSquare, 'sphere':nurbSphere, 'arrow':nurbArrow }


