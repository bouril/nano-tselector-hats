#!/usr/bin/env python
import argparse
import json
import warnings

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.PyConfig.DisableRootLogon = True


def setup_selector(args, selector, dataset, info):
    inputs = ROOT.TList()
    selector.SetInputList(inputs)

    # We can send any object inheiriting from TObject into the selector
    # A corresponding receive function has to be implemented in TSelector::Begin()
    fin = ROOT.TFile.Open("electron_scalefactors.root")
    electronSF = fin.Get("scalefactors_Tight_Electron")
    electronSF.SetDirectory(0)  # Prevent cleanup when file closed
    inputs.Add(electronSF)

    # We can also simply modify any public members of the selector from python
    selector.isRealData_ = False

    fin = ROOT.TFile.Open("muon_scalefactors.root")
    muonSF = fin.Get("scalefactors_Iso_MuonTightId")
    muonSF.SetDirectory(0)
    selector.muCorr_ = muonSF

    fin = ROOT.TFile.Open("pileup_scalefactors.root")
    # Suppose we are looking at the buggy 2017 MC and need per-dataset pileup SF
    pileupSF = fin.Get(dataset)
    if pileupSF != None:
        pileupSF.SetDirectory(0)
        selector.puCorr_ = pileupSF
    else:
        selector.puCorr_ = None


def run(args):
    ROOT.gROOT.ProcessLine(".L {}.C+".format(args.selector))
    warnings.filterwarnings(action='ignore', category=RuntimeWarning, message='no dictionary for class')
    SelectorType = getattr(ROOT, args.selector)

    with open('datadef_nano.json') as fin:
        samples = json.load(fin)

    outputFile = ROOT.TFile(args.output, "recreate")

    for dataset, info in samples.items():
        print(f"Processing {dataset}")
        filelist = info['files']
        if args.limit is not None:
            filelist = filelist[:args.limit]

        selector = SelectorType()
        setup_selector(args, selector, dataset, info)

        for filename in filelist:
            file = ROOT.TFile.Open(filename)
            tree = file.Get("Events")
            if args.maxevents:
                tree.Process(selector, "", args.maxevents)
            else:
                tree.Process(selector)

        outputDir = outputFile.mkdir(dataset)
        ROOT.SetOwnership(outputDir, False)
        outputDir.cd()
        for item in selector.GetOutputList():
            item.Write()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run NanoSelector')
    parser.add_argument('--selector', default='NanoSelector', help='The name of the selector to use (default: %(default)s)')
    parser.add_argument('--limit', type=int, default=None, metavar='N', help='Limit to the first N files of each dataset in sample JSON')
    parser.add_argument('--maxevents', type=int, default=None, metavar='N', help='Limit to the first N entries of the tree in each file')
    parser.add_argument('--output', default='output.root', help='Output filename (default: %(default)s)')
    args = parser.parse_args()

    run(args)
