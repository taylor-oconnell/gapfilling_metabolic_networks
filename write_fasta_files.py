"""
This script reads in two text files: one with all the fids and sequences
and another with all the fids that are linked to functional roles.  It
writes out two fasta files; one for the sequences linked to functional roles,
and another for all the sequences that are not linked to any roles (these
will be the candidate fids for gapfilling).
"""

import sys
import os.path

fin1 = open('role_peg_seq.txt', 'r')
fin2 = open('pegs_and_seqs.txt', 'r')
fout1 = open('pegs_w_roles.fasta', 'w')
fout2 = open('candidate_pegs.fasta', 'w')

fids_w_roles = []
for line in fin1:
    fields = line.strip().split("\t")
    if fields[1] not in fids_w_roles:
        fids_w_roles.append(fields[1])
        fout1.write(">" + fields[1] + "\n" + fields[2] + "\n")
fin1.close()
fout1.close()
print("# of fids with roles: " + str(len(fids_w_roles))+ "\n")

fids_wout_roles = []
tot_fids = 0
for line in fin2:
    tot_fids = tot_fids + 1
    fields = line.strip().split("\t")
    if fields[0] not in fids_w_roles:
        fids_wout_roles.append(fields[0])
        fout2.write(">" + fields[0] + "\n" + fields[1] + "\n")
fin2.close()
fout2.close()
print("# of fids without roles: " + str(len(fids_wout_roles)) + "\n")

if (len(fids_w_roles) + len(fids_wout_roles)) == tot_fids:
    print("OK!  Things are adding up properly.")
else:
    print("ERROR: Linked and unlinked fids not adding up to total number of fids.")
        
        
