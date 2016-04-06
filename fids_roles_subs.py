import sys
import os.path
import matplotlib.pyplot as plt
from servers.SAP import SAPserver
#Make connection by instantiating SAPserver
server = SAPserver()

genomeID = '83333.1'

# Read in the fids and protein sequences fom text file
fin = open('pegs_and_seqs.txt', 'r')
fids_seqs = {}
for line in fin:
    fields = line.strip().split()
    fids_seqs[fields[0]] = fields[1]
fin.close()
print("# of fids: " + str(len(fids_seqs)))

# Write out the role:fid:sequence to a text file
#fout = open('role_peg_seq.txt', 'w')

# Get the roles and subsystems for all of the fids    
feature_hash = server.ids_to_subsystems({"-ids": fids_seqs.keys(), "-genome": genomeID})

roles_w_fids = []
subs_w_fids = []
roles_per_fid = {}
subs_per_fid = {}

for fid in feature_hash:
    roles_per_fid[fid] = len(feature_hash[fid]) # count roles per fid
    subs4role = []
    
    for lst in feature_hash[fid]:
        subs4role.append(lst[1])
        roles_w_fids.append(lst[0])
        subs_w_fids.append(lst[1])
        # Write role:fid:seq to file
        #fout.write(lst[1] + "\t" + fid + "\t" + fids_seqs[fid] + "\n")
        
    subs_per_fid[fid] = len(set(subs4role))
    
#fout.close()

print("length of feature hash: " + str(len(feature_hash)))
print("# of roles that have fids associated: " + str(len(set(roles_w_fids))))
print("# of subsystems that have fids associated: " + str(len(set(subs_w_fids))))

print("max # of roles per fid: " + str(max(roles_per_fid.values())))
print("min # of roles per fid: " + str(min(roles_per_fid.values())))

print("max # of subsystems per fid: " + str(max(subs_per_fid.values())))
print("min # of subsystems per fid: " + str(min(subs_per_fid.values())))

# Create histogram of roles per fid and subsystems per fid
plt.hist(roles_per_fid.values(), bins = 10)
plt.xlabel('Number of Functional Roles')
plt.ylabel('Frequency')
plt.title('Functional Roles per fid')
plt.show()
plt.hist(subs_per_fid.values(), bins = 10)
plt.xlabel('Number of Subsystems')
plt.ylabel('Frequency')
plt.title('Subsystems per fid')
plt.show()
    
    

