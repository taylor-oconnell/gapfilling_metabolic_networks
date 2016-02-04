
import sys
sys.path.append('/Users/Taylor/Desktop/python scripts/')
from servers.SAP import SAPserver
import libsbml
import os.path
import hashlib


#Make connection by instantiating SAPserver
server = SAPserver()



#######################################################################
def file_to_model(sbml_file):


    """
    Read in an SBML file, create a model object from it, print some
    pertinent information about the model, and return the model
    object.
    
    """

    #Check that the file exists
    if not os.path.exists(sbml_file):
        print("[Error] " + sbml_file + ": No such file exists.")
        sys.exit(1)

    #Read the SBML document and print errors if any are encountered
    doc = libsbml.SBMLReader().readSBML(sbml_file)
    if doc.getNumErrors() > 0:
        sys.stderr.write("Errors occurred when reading the document:")
        doc.printErrors()
        sys.exit(1)
    else:
        print "The SBML file " + sbml_file + " was successfully read."

    return doc;



###########################################################################

def get_reactions(sbml_model):

    """
    Get all of the reactions present in the model, get their associated
    reaction ids and return a list of the reaction ids for all
    reactions in the model.

    """
    
    model = sbml_model.getModel()

    #Get all the reactions present in the model
    rxns = []
    rxns = model.getListOfReactions()
    #Get the IDs for each reaction
    r_ids = []
    for r in rxns:
        r_id = r.getId()
        r_id = r_id.replace("_c0", "")
        r_id = r_id.replace("_e0", "")
        r_ids.append(r_id)

    return r_ids;



###########################################################################


def get_compounds(sbml_model):

    """
    Get all of the compounds present in the model, get their associated
    compound ids and return a list of the compound ids for all
    compounds in the model.
    
    """
    
    model = sbml_model.getModel()
    
    #Get all the compounds present in the model
    cmpds = []
    cmpds = model.getListOfSpecies()
    #Get the IDs for each compound
    cmpd_ids = [c.getId() for c in cmpds]

    return cmpd_ids;



#############################################################################


def get_roles(r_ids):

    #Find which functional roles are present based upon the reactions present
    roles_pres = server.reactions_to_roles({"-ids":r_ids})
    roles = roles_pres.values()
    all_roles_pres = [r for l in roles for r in l]
    print("\n\n# OF FUNCTIONAL ROLES PRESENT: " + str(len(set(all_roles_pres))))

    return all_roles_pres;



#################################################################################
    

def get_missing_roles(all_roles_present):

    #Find which subsystems are present based upon the functional roles present
    subs_pres = server.subsystems_for_role({"-ids":list(all_roles_present)})
    subs = subs_pres.values()
    all_subs = [s for l in subs for s in l]

    print("\n\n# OF SUBSYSTEMS PRESENT IN THE MODEL: " + str(len(set(all_subs))))

    #Find all roles that should be present in every subsystem represented in the model
    roles_theor = server.subsystem_roles({"-ids": list(all_subs)})
    r_theor = roles_theor.values()
    all_r_theor = [role for l in r_theor for role in l]

    print("\n\nNumber of theoretical roles: " + str(len(set(all_r_theor))) + "\n")

    #Use set() to get rid of duplicates of roles in the list of roles and list
    # of theoretical roles and subtract the set of roles we know we have
    # from the set of theoretical roles
    missing_roles = list(set(all_r_theor) - set(all_roles_present))

    print("\n\nNumber of possible missing roles: " + str(len(missing_roles)))
    #print("\nMISSING ROLES:\n")
    #print(missing_roles)

    return missing_roles;


#################################################################################
    

def get_prots_for_roles(roles_list):

    # Check the type of input
    if type(roles_list) is not list:
        roles_list = [roles_list]
    
    #Find the protein MD5 ids associated with each of the missing functional
    # roles
    roles_and_md5s = server.roles_to_proteins({"-roles":roles_list})

    return roles_and_md5s


#################################################################################
    

def get_seqs_for_roles(roles_and_md5s):

    print roles_and_md5s
    
    m = hashlib.md5()

    # Extract the protein md5s into list to find their fids
    prot_ids = roles_and_md5s.values()
    prot_ids = [ID for l in prot_ids for ID in l]
    # Find the fids associated with each of the proteins from the missing
    # functional roles
    protIDs_and_fids = server.proteins_to_fids({"-prots":prot_ids})
    # Loop through to eliminate the extra fids that code for the exact
    # same seqquence
    md5_and_fid = {}
    for key in protIDs_and_fids:
        new_val = protIDs_and_fids[key]
        md5_and_fid[key] = new_val[0]
    print md5_and_fid
    
    # Get the protein sequences for the fids
    fids = md5_and_fid.values()      
    fids_and_seqs = server.fids_to_proteins({"-ids":fids, "-sequence":1})
    print fids_and_seqs

    # Map the sequences to the md5s using the fids
    md5s_and_seqs = {}
    for key1 in fids_and_seqs:
        for key2 in md5_and_fid:
            if key1 == md5_and_fid[key2]:
                md5s_and_seqs[key2] = fids_and_seqs[key1]
    print md5s_and_seqs
                
    
    """
    # Convert the protein sequences to MD5 checksums so we can map
    # them back to their roles
    fids_and_md5s = {}
    for key in fids_and_seqs:
        val = fids_and_seqs[key]
        m.update(val.encode('utf-8'))
        fids_and_md5s[key] = m.hexdigest()
    print fids_and_md5s
    
    
    # Map the protein md5s to their sequences using their fids
    md5s_and_seqs ={}
    for key1 in fids_and_md5s:
        for key2 in fids_and_seqs:
            if key1 == key2:
                if fids_and_md5s[key1] not in md5s_and_seqs:
                    md5s_and_seqs[fids_and_md5s[key1]] = fids_and_seqs[key2]
    print md5s_and_seqs
    """           
                      
    # Map the protein sequences to their roles using their md5s
    roles_and_seqs = {}
    count1 = 0
    count0 = 0
    for key1 in md5s_and_seqs:
        for key2 in roles_and_md5s:
            
            #count0 = count0 + 1
            # Check if the md5 is in the list of md5s for the role.
            if key1 in roles_and_md5s[key2]:
                #count1 = count1 + 1
    #print "count0: " + str(count0)
    #print "count1: " + str(count1)
    
                # Check if the role is already in the dictionary mapping
                # roles to seqs.  If not, add it along with the seq. If
                # the role's there already,add the seq to the list of
                # seqs for the existing role.
                if key2 not in roles_and_seqs:
                    roles_and_seqs[key2] = [md5s_and_seqs[key1]]
                else:
                    roles_and_seqs[key2].append(md5s_and_seqs[key1])
    
    
                
    return roles_and_seqs
    

########################################################################
########################################################################

if __name__ == '__main__':

    #read model
    model = file_to_model("Opt224308.1.xml")

    # get the reactions present
    rxns = get_reactions(model)
    print("# of reactions: " + str(len(rxns)))

    # get the compounds present
    cmpds = get_compounds(model)
    print("# of compounds: " + str(len(cmpds)))

    # get the roles for reactions present
    roles = get_roles(rxns)

    # find which roles are possibly missing
    missing_roles = get_missing_roles(roles)
    print "\n" + str(missing_roles[0])
    
    
    # get the protein IDs associated with the missing roles
    md5s_for_missing_roles = get_prots_for_roles(missing_roles[0])
    #print md5s_for_missing_roles

    #prot_ids = ids_for_missing_roles.values()
    #prot_ids = [ID for l in prot_ids for ID in l]
    #print prot_ids
    #print "\nThere are " + str(len(prot_ids)) + " protein sequences for the role."
    
    
    # get the protein sequences for the missing roles
    roles_and_seqs = get_seqs_for_roles(md5s_for_missing_roles)
    print roles_and_seqs

    # reality checks
    if len([missing_roles[0]]) == len(md5s_for_missing_roles):
        print "\nOK1"

    if len(md5s_for_missing_roles)==len(roles_and_seqs):
        print "OK2"

    if len(md5s_for_missing_roles.values()) == len(roles_and_seqs.values()):
        print "OK3"
    
    
    """
    print("\n\nFirst two missing roles and their corresponding prot IDs:\n")
    for i in range(2):
        print str(missing_roles[i]) + "\t" + str(ids_for_missing_roles[missing_roles[i]])
        
    
        

    print "\n\n"
    print fids_and_seqs
    """


    
    














