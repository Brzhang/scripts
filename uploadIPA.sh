SCRIPT_DIR=$(pwd -P)
Project_ROOT=${SCRIPT_DIR}
PRODUCT_DIR="Release-iphoneos"

#FileName=$1
#ProjectType=$2
SERVER_FLAG="TEST"
SERVER_NAME="TEST"
if [ $# -eq 1 ]; then
    SERVER_FLAG=$1
fi

if [ "$FLAG" != "TEST" ]; then
    SERVER_NAME="RELEASE"
fi

cd ${Project_ROOT}/build/${PRODUCT_DIR}/
md5 New\ Orient2.ipa >> MD5.txt
#get version
VERSION=$(cat ../../buildScript/version.txt)
#compress
zip -9  -r NewOrient2_${VERSION}_${SERVER_NAME}.zip New\ Orient2.ipa MD5.txt New\ Orient2.app.dSYM

#upload
VersionDir=`echo $VERSION | awk -F "." '{print $1 "." $2 "." $3}'`
echo $VersionDir
DateDir=`date +%Y%m%d`
echo $DateDir

echo >> log.txt
svn import NewOrient2_${VERSION}_${SERVER_NAME}.zip https://svn.ihowdo.com/svn/dev/测试/iOS\ 公立学生端/$VersionDir/$DateDir/NewOrient2_${VERSION}_${SERVER_NAME}.zip -F log.txt
svn commit -m "NewOrient2_${VERSION}_${SERVER_NAME} 申请提测" -F log.txt
