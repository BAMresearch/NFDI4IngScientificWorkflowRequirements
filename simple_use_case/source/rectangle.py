def generate_rectangle_mesh():
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

    # Parameters
    nx = 5
    ny = 5
    x1, y1 = 0.0, 0.0
    x3 = 2.0
    y3 = 3.0
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

    gmsh.model.geo.synchronize()

    # add physical group
    ps = gmsh.model.addPhysicalGroup(2, [1])
    gmsh.model.setPhysicalName(2, ps, "surface")

    # generate 2d mesh
    gmsh.model.mesh.generate(2)

    # write output file
    gmsh.write("rectangle.msh")
    gmsh.finalize()

    return (a, b)
