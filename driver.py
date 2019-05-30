#!/usr/bin/env python
import argparse
import json
import warnings

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True


def run(args):
    ROOT.gROOT.ProcessLine(".L {}.C+".format(args.selector))
    warnings.filterwarnings(action='ignore', category=RuntimeWarning, message='no dictionary for class')
    selector = ROOT.NanoSelector()

    with open('datadef_nano.json') as fin:
        samples = json.load(fin)

    for sample, info in samples.items():
        filelist = info['files']
        if args.limit is not None:
            filelist = filelist[:args.limit]

        for filename in filelist:
            file = ROOT.TFile.Open(filename)
            tree = file.Get("Events")
            tree.Process(selector)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run NanoSelector')
    parser.add_argument('--selector', default='NanoSelector', help='The name of the selector to use (default: %(default)s)')
    parser.add_argument('--limit', type=int, default=None, metavar='N', help='Limit to the first N files of each dataset in sample JSON')
    args = parser.parse_args()

    run(args)
