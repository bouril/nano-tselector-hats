#!/usr/bin/env python
import argparse
import json
import warnings

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.PyConfig.DisableRootLogon = True


def setup_inputs(args, dataset, info):
    inputs = ROOT.TList()

    return inputs


def run(args):
    ROOT.gROOT.ProcessLine(".L {}.C+".format(args.selector))
    warnings.filterwarnings(action='ignore', category=RuntimeWarning, message='no dictionary for class')
    SelectorType = getattr(ROOT, args.selector)

    with open('datadef_nano.json') as fin:
        samples = json.load(fin)

    outputFile = ROOT.TFile(args.output, "recreate")

    for dataset, info in samples.items():
        print(f"Processing {dataset}")
        inputs = setup_inputs(args, dataset, info)
        filelist = info['files']
        if args.limit is not None:
            filelist = filelist[:args.limit]

        selector = SelectorType()
        selector.SetInputList(inputs)

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
