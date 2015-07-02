#!/bin/sh
#
# build_xcode.sh
#
# How to build Project in batch way:
# 1. build_xcode.sh debug
# 2. build_xcode.sh release

if [ $# -eq 0 ]; then
    echo "Usage: build_xcode.sh [debug|release] [common|nocommon]"
    exit 1
fi

DEPLOYMENT_TARGET=8.0


SCRIPT_DIR=$(pwd -P)
Project_ROOT=${SCRIPT_DIR}

BUILD_TYPE=$1
DEVICE="iphonesimulator$SDK_VERSION"

if [ "$BUILD_TYPE" == "debug" ]; then
	BUILD_TYPE="Debug"
    DEVICE="iphonesimulator$SDK_VERSION"
elif [ "$BUILD_TYPE" == "release" ]; then
	BUILD_TYPE="Release"
    DEVICE="iphoneos$SDK_VERSION"
    PRODUCT_DIR="${BUILD_TYPE}-iphoneos"
else
	echo "input debug or release to make the build."
	exit 1
fi

if [ $# -lt 2 ]; then
    BUILD_TARGET=New\ Orient2
elif [ $2 == "common" ]; then
    BUILD_TARGET=New\ Orient2\ common
else
    BUILD_TARGET=New\ Orient2
fi

# The pathes of projects
NEW_ORIENT2_WKS=${Project_ROOT}/New\ Orient2.xcworkspace
NEW_ORIENT2_PROJ=${Project_ROOT}/New\ Orient2.xcodeproj
POD_PROJ=${Project_ROOT}/Pods/Pods.xcodeproj

#ALL_PROJECTS="$NEW_ORIENT2_PROJ $POD_PROJ”

#python ./version.py $Project_ROOT/.

echo "DEVICE = $DEVICE"

echo "-= Begin Clean =-"
#for PROJ in $ALL_PROJECTS
#do
echo "--= Clean $PROJ =--"
xcodebuild -project ${Project_ROOT}/New\ Orient2.xcodeproj clean > /dev/null
xcodebuild -project $POD_PROJ clean > /dev/null
#done
echo "-= Clean Complete =-"
echo
echo

echo "-= Begin Build =-"
#for PROJ in $ALL_PROJECTS
#do
echo "--= Build $PROJ $BUILD_TYPE =--"

xcodebuild -project $POD_PROJ -configuration $BUILD_TYPE -sdk $DEVICE IPHONEOS_DEPLOYMENT_TARGET=${DEPLOYMENT_TARGET} build
    if [ $? -ne 0 ]; then
        echo "Failed to build project: $POD_PROJ..."
        exit 1
    fi

mkdir ${Project_ROOT}/build/${PRODUCT_DIR}
mv ${Project_ROOT}/Pods/build/${PRODUCT_DIR}/*.* ${Project_ROOT}/build/${PRODUCT_DIR}/

xcodebuild -project ${Project_ROOT}/New\ Orient2.xcodeproj -configuration $BUILD_TYPE -sdk $DEVICE IPHONEOS_DEPLOYMENT_TARGET=${DEPLOYMENT_TARGET} build
if [ $? -ne 0 ]; then
    echo "Failed to build project: ${SCRIPT_DIR}/New\ Orient2.xcodeproj..."
    exit 1
fi

#done
echo "-= Build Complete =-"
xcrun -sdk iphoneos PackageApplication -v ${Project_ROOT}/build/${PRODUCT_DIR}/New\ Orient2.app -o ${Project_ROOT}/build/${PRODUCT_DIR}/New\ Orient2.ipa

echo
echo

exit 0
