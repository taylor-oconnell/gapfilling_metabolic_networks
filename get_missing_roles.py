
import sys
sys.path.append('/Users/Taylor/Desktop/python scripts/')
from servers.SAP import SAPserver
import libsbml
import os.path

#Make connection to SAPserver
server = SAPserver()

#######################################################################

def get_missing_roles(sbml_file):

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

    #Get the model object from the SBML file that was read
    model = doc.getModel()

    #Get all the reactions present in the model
    rxns = model.getListOfReactions()
    #Get the IDs for the reactions
    r_ids = []
    for r in rxns:
        r_id = r.getId()
        r_id = r_id.replace("_c0", "")
        r_id = r_id.replace("_e0", "")
        r_ids.append(r_id)

    #Get the functional roles that are present based upon the reactions present
    roles_pres = server.reactions_to_roles({"-ids":r_ids})
    roles_pres = roles_pres.values()
    all_roles_pres = [role for l in roles_pres for role in l]
    print("\n\n# OF FUNCTIONAL ROLES PRESENT: " + str(len(set(all_roles_pres))))
    
    #Get the subsystems that are present based upon the functional roles present
    subs_pres = server.subsystems_for_role({"-ids":list(all_roles_pres)})
    subs = subs_pres.values()
    all_subs = [s for l in subs for s in l]
    print("\n\n# OF SUBSYSTEMS PRESENT IN THE MODEL: " + str(len(set(all_subs))))


    #Find all roles that should be present in every subsystem represented in the model
    roles_theor = server.subsystem_roles({"-ids": list(all_subs)})
    r_theor = roles_theor.values()
    all_r_theor = [r for l in r_theor for r in l]
    print("\n\nNumber of theoretical roles: " + str(len(set(all_r_theor))) + "\n")


    #Use set() to get rid of duplicates of roles in the list of roles and list
    # of theoretical roles and subtract the set of roles we know we have
    # from the set of theoretical roles
    missing_roles = list(set(all_r_theor) - set(all_roles_pres))

    print("\n\nNumber of possible missing roles: " + str(len(missing_roles)))
    #print("\nMISSING ROLES:\n")
    #print(missing_roles)

    return missing_roles;
    

#######################################################################################

missing_roles = get_missing_roles("Opt224308.1.xml")
    
    
