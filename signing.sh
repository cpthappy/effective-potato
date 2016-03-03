
/usr/local/jdk1.8.0_71/bin/jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore ./keystores/de-monikoo-R1.keystore workspace/effective-potato/src/bin/Monikoo-0.2-release-unsigned.apk monikoo1

.buildozer/android/platform/android-sdk-20/tools/zipalign -v 4 workspace/effective-potato/src/bin/Monikoo-0.2-release-unsigned.apk workspace/effective-potato/src/bin/Monikoo-0.2-release.apk
