#! /usr/bin/python3

import os
import sys
import shutil
import tempfile


def test_dummy():
        print("test_dummy")
        val = 1
        assert val == 1

def test_root():
        # test whether ROOT is installed and compiled with Python support
        import ROOT

def test_import():
        # test whether the mctools module can be imported
        import mctools

def fluka2root(inp):
        tmpdir = tempfile.mkdtemp(suffix='.mc-tools')
        inpto = os.path.join(tmpdir, inp)
        shutil.copyfile(inp, inpto)

        os.chdir(tmpdir)

        cmd = "$FLUTIL/rfluka -N0 -M2 " + inp
        val = os.system(cmd)
        assert val == 0

        cmd = "fluka2root " + inp
        val = os.system(cmd)
        assert val == 0

        shutil.rmtree(tmpdir)

def compare(hist, tab, name):
        """ Compares hist and tab and calls assert if they are different
        """
        assert hist == tab, "problem with %s:\ttab: %s\thist: %s" % (name, tab, hist)

def convert(inpname, tally, unit, hname):
        """ tets histograms converted by fluka2root """
        import ROOT
        import pandas as pd

        base = os.path.splitext(inpname)[0]

        rootfname = "%s.%d.%s.root" % (base, unit, tally)
        tabfname  = "%s.%d_tab.lis" % (base, unit)
        print(base, unit, rootfname, tabfname)

        f = ROOT.TFile(rootfname)
        h2 = f.Get(hname)
        h2.Print()

        nbins = h2.GetNbinsY()
        dOmega = h2.GetYaxis().GetBinLowEdge(nbins+1)-h2.GetYaxis().GetBinLowEdge(1)

        h = h2.ProjectionX()
        h.Scale(dOmega)

        _format="%.3E"

        print(_format%h.GetBinLowEdge(1), _format%h.GetBinLowEdge(2))

        df = pd.read_csv(tabfname, sep='\s+', names=["emin", "emax", "val", "err"], skiprows=2, nrows=h.GetNbinsX()) # data frame
        print("shape:",df.shape)
#        print(df.head())

        nbins = h.GetNbinsX();
        for i in range(nbins):
                hemin = _format % h.GetBinLowEdge(i+1)
                hemax = _format % h.GetBinLowEdge(i+2)
                hval  = _format % h.GetBinContent(i+1)
                herr  = _format % h.GetBinError(i+1)
                femin = _format % df['emin'][i]
                femax = _format % df['emax'][i]
                fval  = _format % df['val'][i]
                ferr  = _format % df['err'][i]
                print(i+1,femin,femax,fval,ferr,"\t",hemin,hemax,hval,herr)
#                print(df.ix[i])
                compare(hemin, femin, "emin")
                compare(hemax, femax, "emax")
                compare(hval, fval, "val")
                compare(herr, ferr, "err")


def test_fluka2root():
#        inpfrom = os.path.join(os.environ["FLUPRO"], inp)
#        inputs = ("example.inp", "exmixed.inp", "exdefi.inp", "exfixed.inp")

        inputs = ("shield.inp",)
        for inp in inputs:
                fluka2root(inp)

convert('shield.inp', 'usrbdx', 47, 'beamIn') # fails emin, otherwise OK
#convert('shield.inp', 'usrbdx', 48, 'eFwd') # OK
#convert('shield.inp', 'usrbdx', 49, 'pFwd') # OK
#convert('shield.inp', 'usrbdx', 50, 'eBackE')
#convert('shield.inp', 'usrbdx', 51, 'pBackP') # OK
#convert('shield.inp', 'usrbdx', 52, 'pBackN') # OK
