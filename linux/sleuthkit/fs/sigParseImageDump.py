#!/usr/bin/python

import sys, os, subprocess, re

def runCommand(cmd):
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    return [proc.stdout.read(), proc.stderr.read()]

def main(argv):
    if len(argv) < 3:
        sys.stderr.write("\nUsage: %s <hdax.dd> <file sig list of offsets> <output folder> \n" % (argv[0],))
        return 1

    if not os.path.exists(argv[1]) or not os.path.exists(argv[2]):
        sys.stderr.write("\nERROR: an input file was not found!\n")
        return 1

    dd = runCommand('which dd')[0].strip()
    identify = runCommand('which file')[0].strip()
    display = runCommand('which display')[0].strip()
    grep = runCommand('which grep')[0].strip()
    ddImage = argv[1]

    if not os.path.exists(argv[3]):
        os.makedirs(argv[3])

    outputDir = argv[3]

    inputFile = open(argv[2], "r")
    inputFile.readline()

    for line in inputFile:
        address = runCommand('echo "%s" | cut -f2 -d\' \'' % line.strip())[0].strip()
        print "attempting number: %s" % address
        ddCmd = "%s if=%s count=4000 skip=%s" % (dd, ddImage, address)
        retval = runCommand("%s | %s - | %s \"image\"" % (ddCmd, identify, grep))[0]

        if retval != "":
            runCommand("%s > %s/%s" %(ddCmd, outputDir, address))

    inputFile.close()
if __name__ == "__main__":
    sys.exit(main(sys.argv))
