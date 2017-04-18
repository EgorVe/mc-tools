#! /usr/bin/python -W all

import sys, argparse
import numpy as np
from os import path
sys.path.append("/usr/local/flair")
sys.path.append("/usr/local/flair/lib")
from Data import *
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

def main():
    """ Converts usbsuw output into a ROOT histogram """

    parser = argparse.ArgumentParser(description=main.__doc__,
                                     epilog="Homepage: https://github.com/kbat/mc-tools")
    parser.add_argument('usrbin', type=str, help='usrxxx binary output (produced by usbsuw)')
    parser.add_argument('root', type=str, nargs='?', help='output ROOT file name', default="")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose', help='Print some output')
    
    args = parser.parse_args()

    if not path.isfile(args.usrbin):
        print >> sys.stderr, "usrbin2root: File %s does not exist." % args.usrbin
        return 1

    if args.root == "":
        rootFileName = "%s%s" % (args.usrbin,".root")
    else:
        rootFileName = args.root
    
    b = Usrbin()
    b.readHeader(args.usrbin)
    val = unpackArray(b.readData(0))
    err = unpackArray(b.readStat(0))

    ND = len(b.detector)
    
# for i in range(len(b.detector)):
    if args.verbose:
        b.sayHeader()
        print "\n%d tallies found:" % ND
        for i in range(ND):
            b.say(i)
            print ""

    fout = ROOT.TFile(rootFileName, "recreate")
    for i in range(ND):
        bin = b.detector[i]
        
        h = ROOT.TH3F("h%d" % (bin.score), "%s;x;y;z" % bin.name, bin.nx, bin.xlow, bin.xhigh, bin.ny, bin.ylow, bin.yhigh, bin.nz, bin.zlow, bin.zhigh)
        
        for i in range(bin.nx):
            for j in range(bin.ny):
                for k in range(bin.nz):
                    gbin = i + j * bin.nx + k * bin.nx * bin.ny
                    h.SetBinContent(i+1, j+1, k+1, val[gbin])
                    h.SetBinError(i+1, j+1, k+1, err[gbin])
        h.SetEntries(b.weight)
        h.Write()

    fout.Close()

if __name__=="__main__":
    sys.exit(main())