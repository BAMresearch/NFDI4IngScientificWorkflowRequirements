#!/bin/bash

runAndCheck () {
    CMD=$1
    if ! $CMD; then
        echo "Command '$CMD' failed"
        exit 1
    fi
}

SCRIPT_DIR=$(dirname $(realpath $0))
CASE_DIR=$(dirname "$SCRIPT_DIR")
BASE_DIR=$(dirname "$CASE_DIR")

SOURCE_DIR="${CASE_DIR}/source"
DOLFIN_CONF="${BASE_DIR}/dolfin/install/share/dolfin/dolfin.conf"

# prepare dolfin environment
if ! [[ -f "$DOLFIN_CONF" ]]; then
    echo "Could not find dolfin config file"
    exit 1
else
    runAndCheck "source $DOLFIN_CONF"
fi

# check if source dir exists
if ! [[ -d "$SOURCE_DIR" ]]; then
    echo "Source directory could not be found at ${SOURCE_DIR}"
    exit 1
fi

# actual workflow execution
echo "Creating mesh file with gmsh"
GEO_FILE="${SOURCE_DIR}/unit_square.geo"
MESH_FILE_NAME="unit_square"
MSH_FILE="${MESH_FILE_NAME}.msh"
runAndCheck "gmsh -2 ${GEO_FILE} -o ${MSH_FILE}"

echo "Converting .msh to .xdmf using meshio"
XDMF_GRID="${MESH_FILE_NAME}.xdmf"
HDF5_GRID="${MESH_FILE_NAME}.h5"
runAndCheck "meshio convert ${MSH_FILE} ${XDMF_GRID}"

echo "Running simulation with dolfin"
RUN_SCRIPT="${SOURCE_DIR}/poisson.py"
RESULT_FILE="result"
RESULT_VTK_FILE="${RESULT_FILE}.pvd"
FEM_ORDER=2
runAndCheck "python3 ${RUN_SCRIPT} --mesh ${XDMF_GRID} --degree $FEM_ORDER --output ${RESULT_VTK_FILE}"

echo "producing images"
POST_PRO_SCRIPT="${SOURCE_DIR}/postprocessing.py"
PNG_FILE="result.png"
runAndCheck "pvbatch ${POST_PRO_SCRIPT} ${RESULT_VTK_FILE} ${PNG_FILE}"

echo ""
echo "Workflow has finished successfully!"
echo "The following files were produced in the current folder:"
echo " - ${MSH_FILE}"
echo " - ${XDMF_GRID}"
echo " - ${HDF5_GRID}"
echo " - ${RESULT_VTK_FILE}"
echo " - ${RESULT_FILE}000000.vtu"
echo " - ${PNG_FILE}"
