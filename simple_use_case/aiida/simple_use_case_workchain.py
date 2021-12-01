from aiida.engine import WorkChain
from aiida.plugins import DataFactory
SinglefileData = DataFactory("singlefile")



class SimpleUseCaseWorkChain(WorkChain):
    """WorkChain defining the simple use case."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("geofile", valid_type=SinglefileData)
        spec.input("fenics_code", valid_type=SinglefileData)
        spec.input("postprocessing", valid_type=SinglefileData)
        spec.input("latex_code", valid_type=SinglefileData)
        spec.outline(cls.generate_mesh)
        spec.outline(cls.convert_mesh)
        spec.outline(cls.solve_poisson)
        spec.outline(cls.make_contourplot)
        spec.outline(cls.compile)
        spec.output("paper", valid_type=SinglefileData)

    def generate_mesh(self):
        """generate the mesh using Gmsh"""
        pass

    def convert_mesh(self):
        """convert the mesh to dolfin format using meshio-convert"""
        pass

    def solve_poisson(self):
        """solve the poisson equation using fenics"""
        pass

    def make_contourplot(self):
        """make a plot of the solution using pvbatch"""
        pass

    def compile(self):
        """compilation of the latex code"""

        # FIXME
        # pdf = calcfunction_compile(self.inputs.latex_code)

        # Declaring the output
        self.out("paper", pdf)
