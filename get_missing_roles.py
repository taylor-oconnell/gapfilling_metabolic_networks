
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

    #Create a model from the SBML file that was read
    model = doc.getModel()

    #Print pertinent information about the model
    print ("\nMODEL INFO:\n")
    print("       # of compartments: " + str(model.getNumCompartments()) )
    print("          # of reactions: " + str(model.getNumReactions()) )
    print("          # of compounds: " + str(model.getNumSpecies()) )


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


    #Find which functional roles are present based upon the reactions present
    roles_pres = server.reactions_to_roles({"-ids":r_ids})
    #Pull just the values from the dictionary -- each value is a list of roles
    roles = roles_pres.values()
    #Create a new list in which to combine the many lists of roles returned by
    # the reactions_to_roles() function above
    all_roles_pres = []
    
    #Combine all the lists together into one list
    for r in roles:
        all_roles_pres.extend(r)
    print("\n\n# OF FUNCTIONAL ROLES PRESENT: " + str(len(set(all_roles_pres))))
    
    


    #Find which subsystems are present based upon the functional roles present
    subs_pres = server.subsystems_for_role({"-ids":list(all_roles_pres)})
    #Pull just the values from the dictionary -- each value is a list of subsystems
    subs = subs_pres.values()
    #Create a new list in which to combine the many lists of subsystems
    # returned by the roles_to_subsystems() function above
    all_subs = []
    #Combine all the lists together into one
    for s in subs:
        all_subs.extend(s)
    print("\n\n# OF SUBSYSTEMS PRESENT IN THE MODEL: " + str(len(set(all_subs))))


    #Find all roles that should be present in every subsystem represented in the model
    roles_theor = server.subsystem_roles({"-ids": list(all_subs)})
    #Pull just the values from the dictionary -- each value is a list of subsystems
    r_theor = roles_theor.values()
    #Create a new list in which to combine the many lists of subsystems
    # returned by the roles_to_subsystems() function above
    all_r_theor = []
    #Combine all the lists together into one
    for r in r_theor:
        all_r_theor.extend(r)
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
    
    
