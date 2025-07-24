"""
$ pvbatch postprocessing.py -h
"""

import sys
import argparse
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np


def main(args):
    import os
    vtu_file = os.path.expanduser(args.vtu)
    
    # Read VTU file using VTK directly
    try:
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(vtu_file)
        reader.Update()
        mesh = reader.GetOutput()
        if mesh is None or mesh.GetNumberOfPoints() == 0:
            raise ValueError("VTK returned empty mesh - file format may be unsupported or corrupted")
        
    except Exception as e:
        print(f"Failed to read VTU file: {e}")
        sys.exit(1)

    # Query available arrays
    point_data = mesh.GetPointData()
    cell_data = mesh.GetCellData()
    
    try:
        point_arrays = [point_data.GetArrayName(i) for i in range(point_data.GetNumberOfArrays())]
        cell_arrays = [cell_data.GetArrayName(i) for i in range(cell_data.GetNumberOfArrays())]

        if args.field in point_arrays:
            array_type = "point"
        elif args.field in cell_arrays:
            array_type = "cell"
        else:
            print(f"Error: Field '{args.field}' not found in point or cell arrays.")
            print(f"Available point arrays: {point_arrays}")
            print(f"Available cell arrays: {cell_arrays}")
            sys.exit(1)

        # Create points along a line using vtkLineSource (2D: z=0)
        resolution = 101
        line_source = vtk.vtkLineSource()
        line_source.SetPoint1(0.0, 0.0, 0.0)
        line_source.SetPoint2(1.0, 1.0, 0.0)
        line_source.SetResolution(resolution - 1)
        line_source.Update()
        probe_polydata = line_source.GetOutput()

        # Create VTK probe filter
        probe_filter = vtk.vtkProbeFilter()
        probe_filter.SetSourceData(mesh)
        probe_filter.SetInputData(probe_polydata)
        probe_filter.Update()
        
        # Get results
        result = probe_filter.GetOutput()
        sampled_points = vtk_to_numpy(result.GetPoints().GetData())
        
        # Get field data
        if args.field in point_arrays:
            field_array = result.GetPointData().GetArray(args.field)
        else:
            field_array = result.GetCellData().GetArray(args.field)
        
        if field_array is None:
            print(f"Error: Field '{args.field}' not found in sampled data.")
            sys.exit(1)
        
        field_data = vtk_to_numpy(field_array)

        # Prepare data for CSV using numpy instead of pandas
        arc_length = np.linalg.norm(sampled_points - sampled_points[0], axis=1)
        
        # Check for valid mask in VTK results
        valid_mask_array = result.GetPointData().GetArray("vtkValidPointMask")
        if valid_mask_array is not None:
            valid_mask = vtk_to_numpy(valid_mask_array)
            if not np.all(valid_mask == 1):
                print("Error: Not all probe points are valid (some are outside the mesh).")
                sys.exit(1)

        # Write CSV manually using numpy
        header = ["arc_length", args.field]
        data_array = np.column_stack([arc_length, field_data])
        
        np.savetxt(args.csv, data_array, delimiter=',', header=','.join(header), comments='')
        print(f"Data successfully written to {args.csv}")
    except Exception as e:
        print(f"Postprocessing error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=f"python {__file__}",
        description="Plots the solution over a line and writes the data to file.",
        usage="%(prog)s [options] vtu csv",
    )

    parser.add_argument("vtu", type=str, nargs='?', 
                        default="poisson.vtu",
                        help="The source vtu filepath.")
    parser.add_argument("csv", type=str, nargs='?', 
                        default="plotoverline.csv", 
                        help="The target csv filepath.")
    parser.add_argument(
        "--field",
        type=str,
        default="u",
        help="Field variable to plot (default: u)",
    )
    
    args = parser.parse_args(sys.argv[1:])
    main(args)





