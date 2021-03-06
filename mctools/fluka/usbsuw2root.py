#! /usr/bin/python2 -W all

from __future__ import print_function
import sys, argparse
from os import path
from mctools import fluka
from mctools.fluka.flair import Data
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
        print("usrbin2root: File %s does not exist." % args.usrbin, file=sys.stderr)
        return 1

    if args.root == "":
        rootFileName = "%s%s" % (args.usrbin,".root")
    else:
        rootFileName = args.root
    
    b = Data.Usrbin()
    b.readHeader(args.usrbin)

    ND = len(b.detector)
    
    if args.verbose:
        b.sayHeader()
        print("\n%d tallies found:" % ND)
        for i in range(ND):
            b.say(i)
            print("")

    fout = ROOT.TFile(rootFileName, "recreate")
    for i in range(ND):
        val = Data.unpackArray(b.readData(i))
        err = Data.unpackArray(b.readStat(i))
        bin = b.detector[i]

        title = fluka.particle.get(bin.score, "unknown")
        if bin.type % 10 in (0, 3, 4, 5, 6):  # Fluka Manual, pages 250-251
            title = title +  ";x [cm];y [cm];z [cm]"
        h = ROOT.TH3F(bin.name, title, bin.nx, bin.xlow, bin.xhigh, bin.ny, bin.ylow, bin.yhigh, bin.nz, bin.zlow, bin.zhigh)
        
        for i in range(bin.nx):
            for j in range(bin.ny):
                for k in range(bin.nz):
                    gbin = i + j * bin.nx + k * bin.nx * bin.ny
                    h.SetBinContent(i+1, j+1, k+1, val[gbin])
                    h.SetBinError(i+1, j+1, k+1, err[gbin]*val[gbin])
        h.SetEntries(b.weight)
        h.Write()

    fout.Close()

if __name__=="__main__":
    sys.exit(main())
