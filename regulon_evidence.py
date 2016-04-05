import sys
import os.path
from servers.SAP import SAPserver

#Make connection by instantiating SAPserver
server = SAPserver()

def regulon_evidence(genomeID, roles_and_fids, subs_and_fids, subs_and_roles)

    # Get the regulons in the genome
    regulons = server.atomic_regulons(genomeID)

    # Loop through the roles
    for r in roles_and_fids:
        # Grab the role name and the fid for the role
        role = r.keys()
        fid = r.values()
        
        # Loop through the regulons
        for reg in regulons:
            # Get the fids in the regulon
            fids_in_reg = reg.values()

            # Check if the fid for role is in the regulon
            if fid in fids_in_reg:

                # Get the other fids in its subsystem
                other_fids = []
                for s in subs_and_fids:
                    if fid in s.values():
                        other_fids.append(list((set(s.values) - set(fid))))

                # Set a count variable to count number of other fids in the
                # subsystem that are also in the regulon
                count = 0
                # Check if each of the other fids are also in the regulon
                for f in other_fids:
                    
                    # If so, then add to the count
                    if f in fids_in_reg:
                        count = count +1

        roles_and_reg_evidence[role] = count
                        
                        
                        
                

        

        

            

        
        

    

    

    

    
