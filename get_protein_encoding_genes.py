import sys
import os.path
from servers.SAP import SAPserver

#Make connection by instantiating SAPserver
server = SAPserver()


#############################################################################

def get_pegs(genomeID):

    """
    This function takes a genome id as an input and returns a list of ids for
    the protein-encoding genes in the genome.
    """
    
    pegs = server.all_features({'-ids':[genomeID], '-type':'peg'})
    pegs = [peg for l in pegs.values() for peg in l]

    return pegs

#############################################################################

def get_nonhypothetical_pegs(genomeID):

    pegs = server.feature_assignments({'-genome':genomeID, '-type':'peg', '-hypothetical':0})
    #pegs = pegs.keys()

    return pegs

#############################################################################

def get_hypothetical_pegs(genomeID):

    pegs = server.feature_assignments({'-genome':genomeID, '-type':'peg', '-hypothetical':1})
    #pegs = pegs.keys()

    return pegs

#############################################################################


def get_prot_seqs(pegs):

    """
    This function takes a list of feature ids as an input and returns a
    dictionary that has feature ids as the keys and the corresponding protein
    sequences as the values.
    """

    fids_seqs = server.fids_to_proteins({'-ids':pegs, '-sequence':1})
    return fids_seqs

#############################################################################


def get_roles_for_prots(pegs):

    """
    This function takes a list of feature ids as an input and returns a
    dictionary that has feature ids as the keys and their corresponding roles
    as the values.
    """

    fids_roles = server.ids_to_functions({'-ids':pegs, '-genome': '83333.1'})
    return fids_roles


#############################################################################


def match_roles_and_seqs(fids_seqs, fids_roles):

    """
    This function takes two dictionaries as input (one mapping fids to
    protein sequences and another mapping fids to roles).  It returns a
    dictionary that has roles as the keys and their corresponding protein 
    sequence as the values. (1 role : 1 seq)
    """

    roles_seqs = {}
    
    for key1 in fids_seqs:
        for key2 in fids_roles:
            # check that the fids match
            if key1 == key2:
                roles_seqs[fids_roles[key2]] = fids_seqs[key1]

    return roles_seqs
                

#############################################################################
#############################################################################


if __name__ == '__main__':

    # Get all of the fids for the pegs in the genome
    fids = get_pegs('83333.1')
    #fids = fids[0:25]
    print "# of pegs in genome: " + str(len(fids)) + "\n"
    #print the fids for the pegs
    for i in range(25):
        print fids[i]
        
        
    """
    # Get the non-hypothetical pegs
    pegs_nh = get_nonhypothetical_pegs('83333.1')
    print "# of non-hypothetical pegs in genome: " + str(len(pegs_nh)) + "\n"

    fids, funcs = zip(*pegs_nh.items())
    for i in range(10):
        print fids[i] + "\t\t" + funcs[i]

    # Get the hypothetical pegs
    #pegs_h = get_hypothetical_pegs('83333.1')
    #print "# of hypothetical pegs in genome: " + str(len(pegs_h)) + "\n"
    #print pegs_h

    # Check that the # of hypothetical pegs and the # of
    # non-hypothetical pegs add to the total # of pegs
    #if len(pegs_nh) + len(pegs_h) == len(pegs):
        #print "OK. Things are adding up properly."
    #else:
        #print "ALERT: # of hypothetical pegs and # of non-hypothetical pegs do not sum to the # of total pegs."
    """
    # Get the protein sequences for each feature (gene) in the genome.
    prot_seqs = get_prot_seqs(fids[0:25])
    print "\n# of fids: " + str(len(prot_seqs.keys()))
    print "\n# of protein sequences: " + str(len(prot_seqs.values()))
    for i in range(25):
        print str(fids[i]) + "\t\t" + str(prot_seqs[fids[i]])
    #print prot_seqs

    # Get the functional role for each feature (gene) in the genome.
    roles = get_roles_for_prots(fids[0:25])
    print roles

    # Match the roles and sequences together
    roles_and_seqs = match_roles_and_seqs(prot_seqs, roles)

    print roles_and_seqs

    

    



    





    
