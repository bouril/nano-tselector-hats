#define NanoSelector_cxx
// The class definition in NanoSelector.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.


// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// root> T->Process("NanoSelector.C")
// root> T->Process("NanoSelector.C","some options")
// root> T->Process("NanoSelector.C+")
//


#include "NanoSelector.h"
#include <TH2.h>
#include <TStyle.h>
#include <TLorentzVector.h>

void NanoSelector::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
}

void NanoSelector::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();

}

Bool_t NanoSelector::Process(Long64_t entry)
{
   // The Process() function is called for each entry in the tree (or possibly
   // keyed object in the case of PROOF) to be processed. The entry argument
   // specifies which entry in the currently loaded tree is to be processed.
   // When processing keyed objects with PROOF, the object is already loaded
   // and is available via the fObject pointer.
   //
   // This function should contain the \"body\" of the analysis. It can contain
   // simple or elaborate selection criteria, run algorithms on the data
   // of the event and typically fill histograms.
   //
   // The processing can be stopped by calling Abort().
   //
   // Use fStatus to set the return value of TTree::Process().
   //
   // The return value is currently not used.

   fReader.SetEntry(entry);

   TLorentzVector lep1, lep2;
   int lep1_id{0}, lep2_id{0};
   bool tooManyLep = false;

   for(UInt_t iEl=0; iEl < *nElectron; ++iEl) {
      if (Electron_pt[iEl] > 20. && std::abs(Electron_eta[iEl]) < 2.5 && Electron_cutBased[iEl] >= 4 && Electron_pfRelIso03_all[iEl] < 0.15 * Electron_pt[iEl] ) {
         if (lep1_id==0) {
            lep1.SetPtEtaPhiM(Electron_pt[iEl], Electron_eta[iEl], Electron_phi[iEl], Electron_mass[iEl]);
            lep1_id = Electron_pdgId[iEl];
            // if (!isRealData_) weight *= eleCorr_->GetBinContent(eleCorr_->FindBin(Electron_eta[iEl], Electron_pt[iEl]));
         } else if (lep2_id==0) {
            lep2.SetPtEtaPhiM(Electron_pt[iEl], Electron_eta[iEl], Electron_phi[iEl], Electron_mass[iEl]);
            lep2_id = Electron_pdgId[iEl];
            // if (!isRealData_) weight *= eleCorr_->GetBinContent(eleCorr_->FindBin(Electron_eta[iEl], Electron_pt[iEl]));
         } else {
            tooManyLep = true;
         }
      }
   }

   return kTRUE;
}

void NanoSelector::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.

}

void NanoSelector::Terminate()
{
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.

}
