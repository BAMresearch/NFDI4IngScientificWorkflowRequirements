"""
$ pvbatch postprocessing.py -h
"""

import sys
import argparse
from paraview.simple import (
    GetActiveViewOrCreate,
    GetColorTransferFunction,
    GetLayout,
    GetScalarBar,
    Show,
    SaveScreenshot,
    PVDReader,
)
from numpy import linspace


def main(args):
    xdmf_file = args.xdmf
    source = PVDReader(registrationName="xdmfreader", FileName=[xdmf_file])
    array_info = source.PointData[args.field]
    data_range = array_info.GetRange(-1)

    view = GetActiveViewOrCreate("RenderView")
    view.OrientationAxesVisibility = 0

    display = Show(source, view)

    display.SetScalarBarVisibility(view, True)
    fun = GetColorTransferFunction(args.field)
    fun.RescaleTransferFunction(data_range[0], data_range[1])

    color_bar = GetScalarBar(fun, view)
    color_bar.AutoOrient = 0
    color_bar.Orientation = "Horizontal"
    color_bar.ComponentTitle = ""
    color_bar.TitleFontFamily = "Times"
    color_bar.LabelFontFamily = "Times"
    color_bar.LabelFontSize = 30
    color_bar.AutomaticLabelFormat = 0
    color_bar.ScalarBarLength = 0.33
    color_bar.Title = f"${args.field}$"
    color_bar.LabelFormat = "%#3.1f"
    color_bar.RangeLabelFormat = "%#3.1f"
    fontsize = 30
    color_bar.TitleFontSize = fontsize
    color_bar.LabelFontSize = int(fontsize * 0.95)

    def get_custom_labels(vmin, vmax, num):
        x = linspace(vmin, vmax, num=num)
        return x.tolist()

    color_bar.UseCustomLabels = 1
    color_bar.CustomLabels = get_custom_labels(data_range[0], data_range[1], 7)
    color_bar.AddRangeLabels = 1

    layout = GetLayout()

    # layout/tab size in pixels
    layout.SetSize(1483, 924)

    # current camera placement for renderView1
    view.InteractionMode = "2D"
    view.CameraPosition = [0.5, 0.5, 2.7320508075688776]
    view.CameraFocalPoint = [0.5, 0.5, 0.0]
    view.CameraParallelScale = 0.7071067811865476

    # save screenshot
    SaveScreenshot(args.png, view, ImageResolution=[2000, 1246])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=f"pvbatch {__file__}",
        description="Make a contour plot of the solution.",
        usage="%(prog)s [options] xdmf png",
    )
    parser.add_argument("xdmf", type=str, help="The source xdmf filepath.")
    parser.add_argument("png", type=str, help="The target png filepath.")
    parser.add_argument(
        "--field",
        type=str,
        default="u",
        help="Field variable to plot (default: u)",
    )
    args = parser.parse_args(sys.argv[1:])
    main(args)
