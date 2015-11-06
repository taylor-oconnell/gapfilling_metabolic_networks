import sys
sys.path.append('/Users/Taylor/Desktop/python scripts/')
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
    pegs = [peg for listt in pegs.values() for peg in listt]

    return pegs

#############################################################################

def get_nonhypothetical_pegs(genomeID):

    pegs = server.feature_assignments({'-genome':genomeID, '-type':'peg', '-hypothetical':0})
    pegs = pegs.keys()

    return pegs

#############################################################################

def get_hypothetical_pegs(genomeID):

    pegs = server.feature_assignments({'-genome':genomeID, '-type':'peg', '-hypothetical':1})
    pegs = pegs.keys()

    return pegs

#############################################################################


def get_prot_seqs(pegs):

    """
    This function takes a list of feature ids as an input and returns a
    dictionary that has feature ids as the keys and the corresponding protein
    sequences as the values.
    """

    seqs = server.fids_to_proteins({'-ids':pegs, '-sequence':1})
    return seqs

#############################################################################
#############################################################################


if __name__ == '__main__':

    
    pegs = get_pegs('83333.1')
    print "# of pegs in genome: " + str(len(pegs)) + "\n"
    for i in range(10):
        print pegs[i]

    pegs_nh = get_nonhypothetical_pegs('83333.1')
    print "# of non-hypothetical pegs in genome: " + str(len(pegs_nh)) + "\n"

    pegs_h = get_hypothetical_pegs('83333.1')
    print "# of hypothetical pegs in genome: " + str(len(pegs_h)) + "\n"

    if len(pegs_nh) + len(pegs_h) == len(pegs):
        print "OK. Things are adding up properly."
    else:
        print "ALERT: # of hypothetical pegs and # of non-hypothetical pegs do not sum to the # of total pegs."
    

    prot_seqs = get_prot_seqs(pegs)
    print "# of sequences: " + str(len(prot_seqs)) + "\n"
    protSeqs = prot_seqs.items()
    for i in range(10):
        print protSeqs[i]
    



    





    
