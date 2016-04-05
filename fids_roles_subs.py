import sys
import os.path
from servers.SAP import SAPserver
#Make connection by instantiating SAPserver
server = SAPserver()

genomeID = '83333.1'

fin = open('pegs_in_genome.txt', 'r')
fids = []
for line in fin:
    fids.append(line.strip())
fin.close()
print("# of fids: " + str(len(fids)))
    

feature_hash = server.ids_to_subsystems({"-ids": fids, "-genome": genomeID})
roles_w_fids = []
subs_w_fids = []
for fid in feature_hash:
    for l in feature_hash[fid]:
        roles_w_fids.append(l[0])
        subs_w_fids.append(l[1])

print("# of roles that have fids associated: " + str(len(roles_w_fids)))
print("# of subsystems that have fids associated: " + str(len(subs_w_fids)))
    
    

