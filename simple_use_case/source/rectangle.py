def generate_rectangle_mesh(p1, p3, nx=5, ny=5):
    """
    Partition of a rectangle Ω = [a, b] x [a, b]
    into (nx - 1) * (ny - 1) triangles


     ^  4---------3
     |  |         |
     b  |    Ω    |
     |  |         |
     v  1---------2
        <----a---->
    """
    import gmsh

    assert len(p1) == 2
    assert len(p3) == 2

    # Parameters
    x1, y1 = p1
    x3, y3 = p3
    a = x3 - x1
    b = y3 - y1

    gmsh.initialize()
    # add model name
    gmsh.model.add("rectangle")

    # add all four points
    gmsh.model.geo.addPoint(x1, y1, 0.0)
    gmsh.model.geo.addPoint(x1 + a, y1, 0.0)
    gmsh.model.geo.addPoint(x1 + a, y1 + b, 0.0)
    gmsh.model.geo.addPoint(x1, y1 + b, 0.0)

    # add lines in counter-clock wise order
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(2, 3, 2)
    gmsh.model.geo.addLine(3, 4, 3)
    gmsh.model.geo.addLine(4, 1, 4)

    # add curve loop and surface
    gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)
    gmsh.model.geo.addPlaneSurface([1], 1)

    # add physical group
    ps = gmsh.model.addPhysicalGroup(2, [1])
    gmsh.model.setPhysicalName(2, ps, "surface")

    # set number of nodes per line
    gmsh.model.geo.mesh.setTransfiniteCurve(1, nx)
    gmsh.model.geo.mesh.setTransfiniteCurve(2, ny)
    gmsh.model.geo.mesh.setTransfiniteCurve(3, nx)
    gmsh.model.geo.mesh.setTransfiniteCurve(4, ny)
    gmsh.model.geo.mesh.setTransfiniteSurface(1, "Left")

    gmsh.model.geo.synchronize()

    # generate 2d mesh
    gmsh.model.mesh.generate(2)

    # write output file
    gmsh.write("rectangle.msh")
    gmsh.finalize()

    return (a, b)


if __name__ == "__main__":
    a, b = generate_rectangle_mesh([0.0, 0.0], (2.0, 4.0), nx=5, ny=10)
    print(a)
    print(b)
