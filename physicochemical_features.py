"""
This script calculates the isoeletric point, molecular weight, secondary
structure fraction, and amino acid composition for each of the annotated
fids.
"""

import sys
import os.path
import pickle
from  calculate_physicochemical_features import calculate_pI, calculate_MW, calculate_secondary_structure_fraction, calculate_aa_composition

roles = []
fids_seqs = {}

# Read in the roles and fids
fin1 = open('role_peg_seq.txt','r')
for line in fin1:
    fields = line.strip().split("\t")
    
    if fields[0] not in roles:
        roles.append(fields[0])
        
    if fields[1] not in fids_seqs:
        fids_seqs[fields[1]] = fields[2]
        
fin1.close()
"""
# Write out the roles present to a file
fout1 = open('roles_present.txt','w')
for r in roles:
    fout1.write(r + "\n")
fout1.close()
"""
# Calculate the isoelectric points
pI = calculate_pI(fids_seqs)
firstFive = pI.keys()[:5]
for i in firstFive:
    print(i + "\t" + str(pI[i]))
print("\n")
pickle.dump(pI, open("pI.p", "wb"))

# Calculate the molecular weights
MW = calculate_MW(fids_seqs)
firstFive = MW.keys()[:5]
for i in firstFive:
    print(i + "\t" + str(MW[i]))
print("\n")
pickle.dump(MW, open("MW.p", "wb"))

# Calculate the secondary structure fraction
ssf = calculate_secondary_structure_fraction(fids_seqs)
firstFive = ssf.keys()[:5]
for i in firstFive:
    print(i + "\t" + str(ssf[i]))
print("\n")
pickle.dump(ssf, open("ssf.p", "wb"))

# Calculate the amino acid composition
aac = calculate_aa_composition(fids_seqs)
firstFive = aac.keys()[:5]
for i in firstFive:
    print(i + "\t" + str(aac[i]))
print("\n")
pickle.dump(aac, open("aac.p", "wb"))


    

    
    
        
        
