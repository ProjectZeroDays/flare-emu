############################################
# Copyright (C) 2018 FireEye, Inc.
#
# Licensed under the Apache License, Version 2.0, <LICENSE-APACHE or
# http://apache.org/licenses/LICENSE-2.0> or the MIT license <LICENSE-BSD-3-CLAUSE or
# https://opensource.org/licenses/BSD-3-Clause>, at your option. This file may not be
# copied, modified, or distributed except according to those terms.
#
# Author: James T. Bennett
#
# flare_emu_test_hooks.py is an IDApython script for testing flare-emu
#
# NOTE: you may have to rename functions IDA Pro fails to recognize, such as printf
#
# Dependencies:
# https://github.com/fireeye/flare-emu
############################################

from __future__ import print_function
import idc
import idaapi
import idautils
import flare_emu

tests = {"from MultiByteToWideChar\r\n":["this is a test".encode("utf-16"), 15], 
         "from WideCharToMultiByte\r\n":["this is a test", 15], 
         "truncated MultiByteToWideChar":["this".encode("utf-16"), 4], 
         "truncated WideCharToMultiByte":["this", 4], 
         "strcpy to HeapAlloc":["this is a test"], 
         "lstrcpy to HeapAlloc":["this is a test"], 
         "HeapReAlloc":["this is a test"], 
         "fixed LocalAlloc\r\n":["this is a test"], 
         "fixed LocalAlloc with padding":["this"], 
         "movable LocalAlloc":["this is a test"], 
         "LocalReAlloc":["this is a test"], 
         "mbstowcs":["this is a test".encode("utf-16"), 14], 
         "mbtowc":["t".encode("utf-16"), 1], 
         "VirtualAllocEx":["this".encode("utf-16")], 
         "malloc\r\n":["this".encode("utf-16")], 
         "malloc with padding":["test".encode("utf-16")], 
         "calloc":["this".encode("utf-16")], 
         "memcpy to offset":["test"], 
         "strlen":["this is a test", 14], 
         "strnlen":["this is a test", 2], 
         "wcslen":["this".encode("utf-16"), 4], 
         "wcsnlen":["this".encode("utf-16"), 2], 
         "strcmp":["this is a test", "this is a test", 0], 
         "stricmp":["THIS IS A TEST", "this is a test", 0], 
         "strncmp":["this is a mess", "this is a test", 0], 
         "strnicmp":["THIS IS A MESS", "this is a test", 0], 
         "wcscmp":["this is a test".encode("utf-16"), "this is a test".encode("utf-16"), 0], 
         "wcsicmp":["THIS IS A TEST".encode("utf-16"), "this is a test".encode("utf-16"), 0], 
         "wcsncmp":["this is a mess".encode("utf-16"), "this is a test".encode("utf-16"), 0], 
         "wcsnicmp":["THIS IS A MESS".encode("utf-16"), "this is a test".encode("utf-16"), 0], 
         "strchr":[97, 8, "this is a test"], 
         "wcschr":[97, 8, "this is a test".encode("utf-16")], 
         "strrchr":[116, 13, "this is a test"], 
         "wcsrchr":[116, 13, "this is a test".encode("utf-16")], 
         "strcat":["The Quick Brown Fox Jumps Over The Lazy Dog"], 
         "strlwr":["the quick brown fox jumps over the lazy dog"], 
         "wcscat":["The Quick Brown Fox Jumps Over The Lazy Dog".encode("utf-16")], 
         "wcslwr":["the quick brown fox jumps over the lazy dog".encode("utf-16")], 
         "strdup":["the quick brown fox jumps over the lazy dog"], 
         "wcsdup":["the quick brown fox jumps over the lazy dog".encode("utf-16")]
        }
 
def iterateHook(eh, address, argv, userData):
    testString = eh.getEmuString(argv[0])
    for test in tests:
        if test in testString:
            print("testing '%s'" % testString.replace("\r\n", ""))
            for i in range(len(tests[test])):
                if isinstance(tests[test][i], str):
                    if tests[test][i][:2] == "\xff\xfe":
                        expected = tests[test][i][2:]
                        actual = eh.getEmuWideString(argv[i+1])
                    else:
                        expected = tests[test][i]
                        actual = eh.getEmuString(argv[i+1])
                else:
                    expected = tests[test][i]
                    actual = argv[i+1]
                    
                if expected != actual:
                    print("FAILED: %s does not match expected result %s" % (actual, expected))
            return
    print("%s: test not found" % (testString.replace("\r\n", "")))
    
if __name__ == '__main__':   
    eh = flare_emu.EmuHelper()
    print("testing iterate feature for printf function")
    eh.iterate(idc.get_name_ea_simple("printf"), iterateHook)
