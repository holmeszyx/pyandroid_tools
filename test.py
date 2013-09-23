#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from aapt import AAPT
from pyadb import adb
import aapt_utils

def main():
    aapt_instance = AAPT("/home/holmes/prosoft/android-sdk-linux/build-tools/17.0.0/aapt")    
    apk_file = "/home/holmes/xy/release/RomasterSu_1.0.4_0922_1200_1001_kingsoft.apk"    
    apk_info = aapt_instance.dump_badging(apk_file)
    # print(apk_info)
    apk_info_list = apk_info.split("\n")
    # for i in xrange(len(apk_info_list)):
    #     print(i)
    #     print(apk_info_list[i])
    package_info = aapt_utils.parse_map(apk_info_list[0])
    print(package_info)

    _adb = adb.ADB("/home/holmes/prosoft/android-sdk-linux/platform-tools/adb")
    result = _adb.install(reinstall=True, pkgapp=apk_file)
    # result = _adb.shell_command("id")
    # print(_adb.lastFailed())
    print(result if result != None else _adb.get_error())

if __name__ == "__main__":
    main()