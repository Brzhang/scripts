VERSIONFILE=${PROJECT_DIR}/buildScript/version.txt
if [ "${CONFIGURATION}" = "Release" -a ! -f "$VERSIONFILE" ]; then
    VERSION=$(/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" "${PROJECT_DIR}/${INFOPLIST_FILE}")
    BUILDNUM=$(/usr/libexec/PlistBuddy -c "Print CFBundleVersion" "${PROJECT_DIR}/${INFOPLIST_FILE}")
    NEWBUILDNUM=$(($BUILDNUM + 1))
    /usr/libexec/PlistBuddy -c "Set :CFBundleVersion $NEWBUILDNUM" "${PROJECT_DIR}/${INFOPLIST_FILE}"
    #white the new version to file
    echo $VERSION.$NEWBUILDNUM >> ${PROJECT_DIR}/buildScript/version.txt
fi
