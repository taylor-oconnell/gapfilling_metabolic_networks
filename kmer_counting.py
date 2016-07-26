import sys
import os.path
import skbio


kmer_counts = {}

for seq in skbio.io.read('all_pegs.fasta',format='fasta'):

    fid = seq.metadata['id']
    kmers = seq.kmer_frequencies(2)

    kmer_counts[fid] = kmers

    
print(len(kmer_counts))
