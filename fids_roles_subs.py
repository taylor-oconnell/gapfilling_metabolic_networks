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
    fields = line.strip().split("\t")
    fids_seqs[fields[0]] = fields[1]
fin.close()
print("# of fids: " + str(len(fids_seqs)))

# Create file to write out the role:fid:sequence to text file
fout = open('role_peg_seq.txt', 'w')

# Get the roles and subsystems for all of the fids    
feature_hash = server.ids_to_subsystems({"-ids": fids_seqs.keys(), "-genome": genomeID})

# Some variables four counting roles and subsystems
role_fid_pairs = []
roles_w_fids = []
subs_w_fids = []
roles_per_fid = {}
subs_per_fid = {}


for fid in feature_hash:
    roles4fid = []
    subs4fid = []

    for lst in feature_hash[fid]:
        role = lst[0]
        sub = lst[1]

        # Write role:fid:seq to file
        if (role,fid) not in role_fid_pairs:
            role_fid_pairs.append((role,fid))
            fout.write(role + "\t" + fid + "\t" + fids_seqs[fid] + "\n")
            
        # Get the roles and subs per fid and get all of the roles and subs present           
        roles4fid.append(role)
        subs4fid.append(sub)
        roles_w_fids.append(role)
        subs_w_fids.append(sub)
        
    roles_per_fid[fid] = len(set(roles4fid)) # count roles per fid
    subs_per_fid[fid] = len(set(subs4fid))   # count subsystems per fid
    
fout.close()

"""
# Write out the roles present to a text file
fout1 = open('roles_present.txt','w')
for r in roles:
fout1.write(r + "\n")
fout1.close()
"""

# Print out some info about the roles
print("# of role:fid pairs: " + str(len(role_fid_pairs)) + "\n")
print("# of fids linked to functional roles: " + str(len(feature_hash)))
print("# of roles that have fids associated: " + str(len(set(roles_w_fids))))
print("# of subsystems that have fids associated: " + str(len(set(subs_w_fids))) + "\n")

print("max # of roles per fid: " + str(max(roles_per_fid.values())))
print("avg # of roles per fid: " + str(sum(roles_per_fid.values())/float(len(roles_per_fid.values()))))
print("min # of roles per fid: " + str(min(roles_per_fid.values())) + "\n")

print("max # of subsystems per fid: " + str(max(subs_per_fid.values())))
print("avg # of subsystems per fid: " + str(sum(subs_per_fid.values())/float(len(subs_per_fid.values()))))
print("min # of subsystems per fid: " + str(min(subs_per_fid.values())))

# Create histogram of roles per fid and subsystems per fid
plt.hist(roles_per_fid.values(), bins = 4)
plt.xlabel('Number of Functional Roles')
plt.ylabel('Count')
plt.title('Functional Roles per fid')
plt.show()
plt.hist(subs_per_fid.values(), bins = 8)
plt.xlabel('Number of Subsystems')
plt.ylabel('Count')
plt.title('Subsystems per fid')
plt.show()
    
    

