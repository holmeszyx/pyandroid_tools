#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from aapt import AAPT
from pyadb import adb
import aapt_utils
import sys
import os.path

INSTALL_SUCCESS = 0
INSTALL_FAILURE_EXIST = -1
INSTALL_FAILURE_INCONSISTENT_CERTIFICATES = -2

def main():
    args = sys.argv 
    apk_file = None;
    if len(args) <= 1:
        print("Need a apk file")
        exit(-1)

    apk_file = args[1]
    if not os.path.isabs(apk_file):
        apk_file = os.path.abspath(apk_file)

    _adb = adb.ADB("/home/holmes/prosoft/android-sdk-linux/platform-tools/adb")
    print("Try to install app %s" % apk_file)
    result = install_apk(_adb, apk_file)
    if result == None:
        print("error for adb install")
        exit(-2)
    install_result = result.split("\n")[1]
    install_result_code = parse_install_result(install_result.strip())
    if install_result_code == 0:
        exit(0)

    aapt_instance = AAPT("/home/holmes/prosoft/android-sdk-linux/build-tools/17.0.0/aapt")    
    apk_info = aapt_instance.dump_badging(apk_file)
    apk_info_list = apk_info.split("\n")
    package_info = aapt_utils.parse_map(apk_info_list[0])
    # print(package_info)
    package_name = package_info["name"]
    version_name = package_info["versionName"]
    print("Uninstall app %s with version %s" % (package_name, version_name))
    print(_adb.uninstall(package=package_name, keepdata=True))
    print("Reinstall app")
    print(install_apk(_adb, apk_file))


def install_apk(adb, apkfile):
    if adb != None:
        return adb.install(reinstall=True, pkgapp=apkfile)
    else:
        print("ADB is None");
        return None;

def parse_install_result(result):
    # print (result)
    f = result.find("Success")
    if f != -1:
        return INSTALL_SUCCESS
    f = result.find("Failure")
    error_reason = None
    if f != -1:
        error_reason = result[9:-1]
    print ("* Error reason is %s" % error_reason)
    return parse_error_reason(error_reason)

def parse_error_reason(reason):
    if reason == "INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES":
        return INSTALL_FAILURE_INCONSISTENT_CERTIFICATES
    elif reason == "INSTALL_FAILED_ALREADY_EXISTS":
        return INSTALL_FAILURE_EXIST



if __name__ == "__main__":
    main()