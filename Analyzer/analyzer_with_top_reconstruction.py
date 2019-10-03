import sys
import ROOT
import nuSolutions
import math
import operator
import numpy as np

from nuSolutions            import doubleNeutrinoSolutions
from ratio_plot             import ratioplot
from run_samples_ttbar      import run_samples
from ROOT 		    import kRed	
from uncertainty_calculator import JES_wt_calc

ROOT.gSystem.Load("libDelphes")

try:
	ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
	ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
	pass
	
def PrintTL(vect):
    	print("Vector has PX : %f" %(vect.P4().Px()))
    	print("Vector has PY : %f" %(vect.P4().Py()))
    	print("Vector has PZ : %f" %(vect.P4().Pz()))
    	print("Vector has M  : %f" %(vect.P4().M()))
    	print("Vector has charge : %f" %(vect.Charge))
	return

def Convertnuto4vec(nu,i):
	neutrino = ROOT.TLorentzVector()
    	Px = nu[0][i][0]
	Py = nu[0][i][1]
	Pz = nu[0][i][2]
	E  = math.sqrt(Px**2 + Py**2 + Pz**2)
	neutrino.SetPxPyPzE(Px,Py,Pz,E)
	return neutrino

def dR(lepton1,lepton2) :
       deltaEta = abs(lepton1.Eta - lepton2.Eta)
       deltaPhi = abs(lepton1.Phi - lepton2.Phi)
       dR = math.sqrt(deltaEta**2 + deltaPhi**2)
       return dR
		
# Create chain of root trees
chain = ROOT.TChain("Delphes")
chain = run_samples()

# Create object of class ExRootTreeReader
treeReader 	    = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

# Get pointers to branches used in this analysis
branchJet       = treeReader.UseBranch("Jet")
branchEle       = treeReader.UseBranch("Electron")
branchMuon      = treeReader.UseBranch("MuonTight")
branchMET       = treeReader.UseBranch("PuppiMissingET")	#Pileup mitigation
branchPart      = treeReader.UseBranch("Particle")
branchWeight    = treeReader.UseBranch("Weight")

h_delta_phi     = ROOT.TH1F("Delta_Phi","Delta_Phi",20,0,3.14159)
a_delta_phi     = ROOT.TH1F("A_Delta_Phi","A_Delta_Phi",2,0,3.14159)

h_delta_phi_wt  = ROOT.TH1F("Delta_Phi_wt","Delta_Phi_wt",20,0,3.14159)
a_delta_phi_wt  = ROOT.TH1F("A_Delta_Phi_wt","A_Delta_Phi_wt",2,0,3.14159)

print("Number of entries in the tree :: %d " %(numberOfEntries))

#Main loop over entries
for entry in range(0, numberOfEntries):

    treeReader.ReadEntry(entry)
    jet_arr    = []
    lepton_arr = []
    nb         = 0                  		#Number of b-tags
    #weight     = (branchWeight.At(0)).Weight

    print("Processing event %d of %d " %(entry,numberOfEntries))
    #print("Weight for event is %d " %(weight))

    #MUONS
    for i in range(0,branchMuon.GetEntries()):
         if (branchMuon.At(i).PT > 30 and abs(branchMuon.At(i).Eta) < 2.5) :
             lepton_arr.append(branchMuon.At(i))

    #ELECTRONS
    for i in range(0,branchEle.GetEntries()):
         if (branchEle.At(i).PT > 30 and abs(branchEle.At(i).Eta) < 2.5)   :
             lepton_arr.append(branchEle.At(i))

    # Looking for highest PT leptons in the event
    #lepton_arr =  sorted(lepton_arr,key = operator.attrgetter('PT'), reverse = True)

    # 2 Leptons and Lepton dR cut
    if (len(lepton_arr) == 2):
         lepton1 = lepton_arr[0]
         lepton2 = lepton_arr[1]
         if (dR(lepton1,lepton2) < 0.2 ) : continue

    else : continue

    #Opposite Sign cut
    if (lepton1.Charge * lepton2.Charge != -1) : continue

    # Invariant mass cut
    Mll = (lepton1.P4() +lepton2.P4()).M()
    if ( not ((Mll < 76 or Mll > 106) and Mll > 40)) : continue

    #JETS
    for i in range(0,branchJet.GetEntries()):
        if (branchJet.At(i).PT > 30 and abs(branchJet.At(i).Eta) < 2.5 ) :
            jet_arr.append(branchJet.At(i))
            if (branchJet.At(i).BTag == 1) : nb+=1

    #Again look for highest PT jets
    #jet_arr =  sorted(jet_arr,key = operator.attrgetter('PT'), reverse = True)

    # >= 2 Jets and one B Tag
    if (len(jet_arr) > 1 and nb > 1):
         jet1 = jet_arr[0]
         jet2 = jet_arr[1]

    else : continue

    #MET cut
    MET_un  = branchMET.At(0)
    if   ( MET_un.MET < 40 )  : continue
        
    #Maybe see if a solution exists or not
    try    :	
    	   d = doubleNeutrinoSolutions((jet1.P4(),jet2.P4()),(lepton1.P4(),lepton2.P4()),(MET_un.P4().Px(),MET_un.P4().Py()))
           print("Found a solution : ")
           print(d.nunu_s)
           neutrino1  = Convertnuto4vec(d.nunu_s,0)
           neutrino2  = Convertnuto4vec(d.nunu_s,1)

    except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                print ("No solution for this one")       # your error handling block
                continue
            else:
                raise

    top      =  ROOT.TLorentzVector()
    top      =  jet1.P4() + neutrino1 + lepton1.P4()
  
    tbar     =  ROOT.TLorentzVector()
    tbar     =  jet2.P4() + neutrino2 + lepton2.P4()

    print("Top mass is :: %f" % (top.M()))
    print("Top Pt is :: %f" %(top.Pt()))	

    deltaphi = (lepton1.P4()).DeltaPhi((lepton2.P4())) 
    
    top_wt   = math.exp(0.0615 - (0.0005*top.Pt()))  
    tbar_wt  = math.exp(0.0615 - (0.0005*tbar.Pt()))
    event_wt = math.sqrt(top_wt * tbar_wt)
    
    h_delta_phi.Fill(abs(deltaphi))
    a_delta_phi.Fill(abs(deltaphi))

    #print("Top weight, Anti-top, Event weight from reweighting is :: %f %f %f" %(top_wt,tbar_wt,event_wt))
    #jet1_wt = JES_wt_calc(jet1.P4().Pt())
    #weight  = 1./(1 + jet1_wt**2)
    #print ("Weight here is :: %f " %(weight))
    h_delta_phi_wt.Fill(abs(deltaphi))
    a_delta_phi_wt.Fill(abs(deltaphi))

# Show resulting histograms

c = ROOT.TCanvas("c","c",600,600)
c.cd()
a_delta_phi.Draw("ep")
a_delta_phi.SaveAs("A_Delta_Phi.C")
c.SaveAs("A_Delta_Phi.pdf")


c2 = ROOT.TCanvas("c","c",600,600)
c2.cd()
a_delta_phi.Draw("ep")
a_delta_phi.SaveAs("A_Delta_Phi_wt.C")
c2.SaveAs("A_Delta_Phi_wt.pdf")

c1 = ROOT.TCanvas("c","c",600,600)
c1.cd()
h_delta_phi.Draw("ep")
h_delta_phi_wt.SetLineColor(kRed)
h_delta_phi_wt.Draw("same")
ratioplot(h_delta_phi,h_delta_phi_wt)
raw_input("Press Enter to continue...")
