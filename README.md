This is a short and quick example of using a TSelector to process NanoAOD,
and how it can be scaled out on condor.  There are many ways to accomplish
such a task--here I present just *one*.  Some components are common to any
solution: a core event processor, a steering framework, a metadata
database, a non-event data repository, and an interface to large compute resources.  

There is some [documentation](https://root.cern.ch/developing-tselector) about building a TSelector,
but it mostly boils down to opening an example file from the collection of files you want to process,
and calling `MakeSelector` [doc](https://root.cern.ch/doc/master/classTTree.html#abe2c6509820373c42a88f343434cbcb4) on the tree of interest, e.g.:
```
root -l
auto file0_ = TFile::Open("root://cmseos.fnal.gov//store/mc/RunIIFall17NanoAOD/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/50000/7C2B491C-BCAB-E811-88A2-002590DE6E5E.root");
auto Events = (TTree*) file0_->Get("Events");
Events->MakeSelector("NanoSelector");
```

This is how the selector in this repository was created.

Sadly, to run over collections of files that have different tree structure (e.g. data vs. MC, which have different branches),
one would have to disable some branches.  The perfect function, `TTreeReader::DeregisterValueReader`, is a [protected member function](https://root.cern.ch/doc/v608/classTTreeReader.html#ab9df60de0ade744cb2d5ef423cd12aec).
I don't know why, but I plan to ask.  There are a few workarounds, one is to have one selector for data and one for MC, having them call a common external function.  Another is to use `MakeClass`, which gives more manual control over branch loading, but comes at a heavy cost for NanoAOD, where the array sizes become hardcoded.
Keep in mind that all `TTreeReaderValue` and `TTreeReaderArray` objects are public members of the selector, so you can just pass your selector by reference to external
functions, and they can access all the variables.

To steer the selector behavior, it is much easier to work in python.  The `driver.py` executable configures the selector and runs it on
a list of samples, as specified by the user in `datadef_nano.json`.  JSON is a convenient way to encode the necessary metadata, although
it can be annoying to maintain.  Helper scripts can be written in python to make this JSON creation a bit less burdensome.

To wrap the selector on condor, I've created a `wrapper.sh` that provides a basic ROOT+python 3 environment from LCG.
You can source this environment from any machine with access to cvmfs,
```bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_94python3/x86_64-slc6-gcc62-opt/setup.sh
```

Lastly, there is `submit.jdl`, which can be passed to `condor_submit`.  Here, one specifies what arguments to pass to the driver script.
After all is done, you should have a few `output_*.root` files that can be `hadd`-ed to complete the operation.

And that's how you scale out the old-fashioned way.
