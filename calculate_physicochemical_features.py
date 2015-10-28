import Bio
import sys
sys.path.append('/Users/Taylor/Desktop/python scripts/')
from servers.SAP import SAPserver

#Make connection by instantiating SAPserver
server = SAPserver()


##############################################################################

def calculate_pI(prot_ids, prot_seqs):
    
    """
    This function takes a list of protein ids and a list of coresponding
    protein sequences and calculates the isoelectric point of each protein.
    It returns a dictionary with the protein ids as the keys and their
    respective isoelectric points as the values.

    """

    isoelectric_points = {}
    
    for i in xrange(len(prot_seqs)):
        p = ProteinAnalysis(prot_seqs(i))
        pI = p.isoelectric_point()
        isoelectric_points[prot_ids(i)] = pI

    return isoelectric_points

################################################################################

def calculate_MW(prot_ids, prot_seqs):

    """
    This function takes a list of protein ids and a list of corresponding
    protein sequences and calculates the isoelectric point of each protein.
    It returns a dictionary with the protein ids as the keys and their
    respective isoelectric points as the values.

    """

    molec_weights = {}

    for i in xrange(len(prot_seqs)):
        p = ProteinAnalysis(prot_seqs(i))
        mw = p.molecular_weight()
        molec_weights[prot_ids(i)] = mw

    return molec_weights

#################################################################################
    



        
