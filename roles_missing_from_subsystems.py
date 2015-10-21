
import sys
sys.path.append('/Users/Taylor/Desktop/python scripts/')
from servers.SAP import SAPserver
import libsbml
import os.path

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



########################################################################
########################################################################

if __name__ == '__main__':
    
    model = file_to_model("Opt224308.1.xml")

    rxns = get_reactions(model)
    print("# of reactions: " + str(len(rxns)))

    cmpds = get_compounds(model)
    print("# of compounds: " + str(len(cmpds)))

    roles = get_roles(rxns)

    missing_roles = get_missing_roles(roles)














