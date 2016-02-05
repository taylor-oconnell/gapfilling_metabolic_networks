from Bio.SeqUtils import ProtParam
import sys
sys.path.append('/Users/Taylor/Desktop/python scripts/')
from servers.SAP import SAPserver

#Make connection by instantiating SAPserver
server = SAPserver()


##################################################################################

def calculate_pI(prots):
    
    """
    This function takes a dictionary input where the keys are protein ids and
    the values are the corresponding protein sequences. The function calculates
    the isoelectric point of each protein and returns a dictionary with the
    protein ids as the keys and their respective isoelectric points as the values.

    """
    
    prot_ids, prot_seqs = zip(*prots.items())
    
    isoelectric_points = {}
    
    for i in xrange(len(prot_seqs)):
        p = ProtParam.ProteinAnalysis(prot_seqs[i])
        pI = p.isoelectric_point()
        isoelectric_points[prot_ids[i]] = pI

    return isoelectric_points

###################################################################################

def calculate_MW(prots):

    """
    This function takes a dictionary input where the keys are protein ids and
    the values are the corresponding protein sequences. The function calculates
    the isoelectric point of each protein and returns a dictionary with the
    protein ids as the keys and their respective isoelectric points as the values.

    """
    
    prot_ids, prot_seqs = zip(*prots.items())
    
    molec_weights = {}

    for i in xrange(len(prot_seqs)):
        p = ProtParam.ProteinAnalysis(prot_seqs[i])
        mw = p.molecular_weight()
        molec_weights[prot_ids[i]] = mw

    return molec_weights

####################################################################################
    
def calculate_secondary_structure_fraction(prots):

    """
    This function takes a dictionary input where the keys are protein ids and the
    values are the corresponding protein sequences. The function calculates the
    secondary structure fraction (%helix, %turn, %sheet) of each protein and
    returns a dictionary with the protein ids as the keys and tuples of the form
    (%helix, %turn, %sheet) as the values.

    """

    prot_ids, prot_seqs = zip(*prots.items())
    
    secondary_structure_fractions = {}

    for i in xrange(len(prot_seqs)):
        p = ProtParam.ProteinAnalysis(prot_seqs[i])
        ssf = p.secondary_structure_fraction()
        secondary_structure_fractions[prot_ids[i]] = ssf

    return secondary_structure_fractions

####################################################################################

def calculate_aa_composition(prots):

    """
    This function takes a dictionary input where the keys are protein ids and the
    values are the corresponding protein sequences.  The function calculates the
    secondary structure fraction (%helix, %turn, %sheet) of each protein.  It
    returns a dictionary with the protein ids as the keys and dictionaries of
    amino acid fractions as the values.

    """

    prot_ids, prot_seqs = zip(*prots.items())
     

    aa_composition = {}

    for i in xrange(len(prot_seqs)):
        p = ProtParam.ProteinAnalysis(prot_seqs[i])
        aa_comp = p.get_amino_acids_percent()
        aa_composition[prot_ids[i]] = aa_comp

    return aa_composition




####################################################################################
####################################################################################

if __name__ == '__main__':
    
    pIs = calculate_pI({'id1':'AAAA', 'id2':'DDDD', 'id3':'RRRR'})
    print pIs
    print "\n\n"

    MWs = calculate_MW({'id1':'AAAA', 'id2':'DDDD', 'id3':'RRRR'})
    print MWs
    print "\n\n"

    ssf = calculate_secondary_structure_fraction({'id1':'AAAA', 'id2':'DDDD', 'id3':'RRRR'})
    print ssf
    print "\n\n"

    aac = calculate_aa_composition({'id1':'AAAA', 'id2':'DDDD', 'id3':'RRRR'})
    print aac
    print "\n\n"

        
