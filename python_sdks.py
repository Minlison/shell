#!/usr/bin/env python

import re
import subprocess

sdk_header_pattern = re.compile("^.*SDKs:$")
sdk_switch_pattern = re.compile("^.*(-sdk)\s[a-z]+\d+\.\d+$")

def run_command(cmd):
    return subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE).communicate()

input = run_command(['xcodebuild', '-showsdks'])[0] # take first element of returned tuple
sdks = {}
in_sdk = False
platform = ''

for e in input.split('\n'):
    if sdk_header_pattern.match(e) and not in_sdk:
        in_sdk = True
        platform = e[0:e.rfind(' ')]
        sdks[platform] = []
    if in_sdk and sdk_switch_pattern.match(e):
        sdk = e.split(' ')[-1]
        sdks[platform].append(sdk)
    if in_sdk and e == '':
        in_sdk = False
        del platform

for k,v in sdks.iteritems():

    if k=='iOS Simulator':
        print v[0]
#for k,v in sdks.iteritems():
#    print 'Platform: ', k
#        for e in v:
#            print '\t', e
#            print