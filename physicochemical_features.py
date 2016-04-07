"""
This script calculates the isoeletric point, molecular weight, secondary
structure fraction, and amino acid composition for each of the annotated
fids.
"""

import sys
import os.path
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

# Write out the roles present to a file
fout1 = open('roles_present.txt','w')
for r in roles:
    fout1.write(r + "\n")
fout1.close()

# Calculate the isoelectric points
pI = calculate_pI(fids_seqs)
firstFive = pI.keys()[:5]
for i in firstFive:
    print(i + "\t" + str(pI[i]))

    

    
    
        
        
