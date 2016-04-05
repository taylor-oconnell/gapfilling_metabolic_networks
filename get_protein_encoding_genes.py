import sys
import os.path
from servers.SAP import SAPserver

#Make connection by instantiating SAPserver
server = SAPserver()


#############################################################################

def get_pegs(genomeID):

    """
    This function takes a genome id as an input and returns a list of fids for
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


def get_fids_for_roles(roles_present, genomeID):

    """
    This function takes a list of feature ids as an input and returns a
    dictionary that has feature ids as the keys and their corresponding roles
    as the values.
    """

    roles_fids = server.occ_of_role({'-roles':roles_present, '-genomes': [genomeID]})
    return roles_fids

##############################################################################


def get_prot_seqs(pegs):

    """
    This function takes a list of feature ids as an input and returns a
    dictionary that has feature ids as the keys and the corresponding protein
    sequences as the values.
    """

    fids_seqs = server.fids_to_proteins({'-ids':pegs, '-sequence':1})
    return fids_seqs

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

    genome_id = '83333.1'
    """
    # Get all of the fids for the pegs in the genome
    fids = get_pegs(genome_id)
    print "# of pegs in genome: " + str(len(fids)) + "\n"
    fout_pegs = open('pegs_in_genome.txt', 'w')
    for f in fids:
        fout_pegs.write(f + "\n")
    fout_pegs.close()
    """
    """
    # Get the protein sequences for each feature (gene) in the genome.
    prot_seqs = get_prot_seqs(fids)
    print "\n# of fids: " + str(len(prot_seqs.keys()))
    
    #fout_ps = open('pegs_and_seqs.txt', 'w')
    #for p in prot_seqs:
        #fout_ps.write(p + "\t" + prot_seqs[p] + "\n")
    #fout_ps.close()
    
    count1 = 0
    for i in prot_seqs.values():
        if i == []:
            count1 = count1 + 1
    print("# of fids with no prot sequence: " + str(count1))
    
    # Read in all the fid:sequence pairs in the genome
    fid_seq = {}
    fin1 = open('pegs_and_seqs.txt', 'r')
    for line in fin1:
        [fid, seq] = line.strip().split("\t")
        fid_seq[fid] = seq
    fin1.close()
    
    # Read in the roles present in the model
    roles = []
    fin2 = open('roles_present.txt', 'r')
    for line in fin2:
        roles.append(line.strip())
    fin2.close()

    #Get the fids in the genome associated with the roles
    roles_fids = get_fids_for_roles(roles, genome_id)
    print("# of role/fid pairs: " + str(len(roles_fids)))

    count0 = 0
    count1 = 0
    count2 = 0
    num = 0
    for r in roles_fids:
        num = num + len(roles_fids[r])
        if len(roles_fids[r]) > 1:
            #print(r + "\t" + str(roles_fids[r]))
            count0 = count0 + 1
        if len(roles_fids[r]) == 1:
            count1 = count1 + 1
        if len(roles_fids[r]) == 0:
            count2 = count2 + 1
    print("# of roles with multiple fids: " + str(count0))
    print("# of roles with one fid: " + str(count1))
    print("# of roles with no fid: " + str(count2))
    print("# of fids linked to roles: " + str(num))

    # Write out file with role, fid, and sequence
    fout_rfs = open('role_peg_seq.txt', 'w')
    for r in roles_fids:
        for f in roles_fids[r]:
            fout_rfs.write(r + "\t" + f + "\t" + fid_seq[f] + "\n")
    fout_rfs.close()
    """
    
    
   # Create dictionary with fids as keys and protein seqs as values
    fin3 = open('role_peg_seq.txt', 'r')
    peg_seq = {}
    for line in fin3:
        fields = line.strip().split("\t")
        if fields[1] not in peg_seq:
            peg_seq[fields[1]] = fields[2]
    fin3.close()
    
    # Get a list of the fids that are linked to roles
    fids_w_roles = peg_seq.keys()
       
    # Write out a FASTA file of the protein sequences for the fids
    # linked to functional roles
    fout_fasta = open('pegs_with_roles.fasta', 'w')
    for p in peg_seq:
        fout_fasta.write(">" + p + "\n" + peg_seq[p] + "\n")
    fout_fasta.close()
    
    
    # Write out a FASTA file of the protein sequences for all the fids
    # present in the genome. Also write out a FASTA file of the protein
    # sequences for all the fids that are not linked to a functional role.
    fout_fasta2 = open('all_pegs.fasta', 'w')
    fout_fasta3 = open('pegs_without_roles.fasta', 'w')
    fin4 = open('pegs_and_seqs.txt', 'r')
    for line in fin4:
        fields = line.strip().split("\t")
        fout_fasta2.write(">" + fields[0] + "\n" + fields[1] + "\n")
        if fields[0] not in fids_w_roles:
            fout_fasta3.write(">" + fields[0] + "\n" + fields[1] + "\n")
    fout_fasta2.close()
    fout_fasta3.close()
    fin4.close()
    



    
    
    
    




    

    



    





    
