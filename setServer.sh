SCRIPT_DIR=$(pwd -P)
Project_ROOT=${SCRIPT_DIR}


FLAG="TEST"
if [ $# -eq 1 ]; then
    FLAG=$1
fi

if [ "$FLAG" != "TEST" ]; then
    #rewrite the ServerSelector.h //#define TEST_SERVER
    rm -f ${Project_ROOT}/New\ Orient2/globals/ServerSelector.h
    echo "//#define TEST_SERVER" > ${Project_ROOT}/New\ Orient2/globals/ServerSelector.h
else
    #rewrite the ServerSelector.h #define TEST_SERVER
    rm -f ${Project_ROOT}/New\ Orient2/globals/ServerSelector.h
    echo "#define TEST_SERVER" > ${Project_ROOT}/New\ Orient2/globals/ServerSelector.h
fi