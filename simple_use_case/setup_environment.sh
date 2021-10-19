#!/bin/bash

help () {
    echo "This script can be used to prepare the local environment for the"
    echo "execution of the workflow, installing the required dependencies"
    echo "(although some basic dependencies are required to be installed already)"
    echo ""
    echo "Usage: ./setup_environment CMAKE_PREFIX (optional) BOOST_HOME (optional)"
    echo ""
    echo "       CMAKE_PREFIX can be used to tell cmake further places to look for packages"
    echo "       when installing dolfin, while BOOST_HOME can be set additionally"
    echo "       to tell dolfin the location of the boost installation to use"
    echo ""
    echo "Note: It is recommended that you run this from within a virtual environment"
    echo "      such that you can easily remove the installed python packages afterwards."
    echo "      Please note that dolfin is not installed system-wide but into a local"
    echo "      installation folder."
}

runAndCheck () {
    CMD=$1
    if ! $CMD; then
        echo "Command '$CMD' failed"
        exit 1
    fi
}

installPythonPackages () {
    runAndCheck "python3 -m pip install numpy"
    runAndCheck "python3 -m pip install meshio[all]"
    runAndCheck "python3 -m pip install fenics-ffc --upgrade"
}

getDolfin () {
    PATCH_REL_PATH=$1
    if ! [[ -d dolfin ]]; then
        FENICS_VERSION=$(python3 -c"import ffc; print(ffc.__version__)")

        echo " -- cloning dolfin $FENICS_VERSION"
        runAndCheck "git clone --branch=$FENICS_VERSION --depth=1 https://bitbucket.org/fenics-project/dolfin"

        if [[ -n "$PATCH_REL_PATH" ]]; then
            echo " -- patching dolfin"
            runAndCheck "cd dolfin"
            runAndCheck "git apply ../$PATCH_REL_PATH"
            runAndCheck "cd .."
        fi
    else
        echo "Skip cloning dolfin because folder already exists"
    fi
}

buildDolfin () {
    CMAKE_ARGS=$1

    runAndCheck "cd dolfin"
    runAndCheck "mkdir -p install"
    runAndCheck "mkdir -p build"
    runAndCheck "cd build"

    echo ""
    echo " -- configuring dolfing"
    echo " --- cmake command: cmake $CMAKE_ARGS ../"
    runAndCheck "cmake $CMAKE_ARGS ../"

    echo " -- building dolfin"
    runAndCheck "make"
    runAndCheck "make install"
    runAndCheck "cd ../.."
}

installDolfinPythonBindings () {
    BOOST_HOME_DIR=$1
    if [[ -n "$BOOST_HOME_DIR" ]]; then
        runAndCheck "export BOOST_HOME=$BOOST_HOME_DIR"
    fi

    runAndCheck "source dolfin/install/share/dolfin/dolfin.conf"
    runAndCheck "cd dolfin/python"
    runAndCheck "pip3 install ."
    runAndCheck "cd ../.."
}

checkInstalledProgram () {
    PROG=$1
    if ! command -v $PROG &> /dev/null; then
        echo "Required program '$PROG' not found"
        exit 1
    fi
}

checkInstalledLibrary () {
    LIB=$1
    OUT=$(ldconfig -p | grep $LIB)
    if [[ -z "$OUT" ]]; then
        echo "Library $LIB not found"
        exit 1
    fi
}

# maybe print help message
if [[ "$1" == *"help"* ]]; then
    help
    exit 1
fi

# check basic prerequisites
checkInstalledProgram gmsh
checkInstalledProgram cmake
checkInstalledProgram python3
checkInstalledProgram pvbatch
checkInstalledProgram pip3
checkInstalledLibrary libhdf5

THIS_DIRECTORY=$(dirname $0)
DOLFIN_PATCH="${THIS_DIRECTORY}/dolfin.patch"

# parse user input
CM_PREFIX_PATH=$1
BOOST_HOME=$2

CMAKE_OPTS=""
if [[ -n "$CM_PREFIX_PATH" ]]; then CMAKE_OPTS="-DCMAKE_PREFIX_PATH=$CM_PREFIX_PATH"; fi
if [[ -n "$BOOST_HOME" ]]; then CMAKE_OPTS="$CMAKE_OPTS -DBOOST_HOME=$BOOST_HOME"; fi

# define dolfin install directory
CUR_DIR=$(pwd)
CMAKE_OPTS="$CMAKE_OPTS -DDOLFIN_ENABLE_HDF5=ON -DCMAKE_INSTALL_PREFIX=$CUR_DIR/dolfin/install ../"

echo "Installing basic dependencies"
installPythonPackages

echo "Installing Dolfin"
getDolfin $DOLFIN_PATCH
buildDolfin "$CMAKE_OPTS"
installDolfinPythonBindings "$BOOST_HOME"
