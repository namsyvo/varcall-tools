'''
Generate reads with DWGSIM
Usage: python dwgsim-genreads-exp.py
'''
import os

ref_len = 249250621
read_lens = [100]
seq_errs = ['0.00015-0.0015']
read_nums = [cov*ref_len/(2*read_lens[0]) for cov in [2, 3, 4, 6, 7, 8, 9, 10, 15, 20, 25, 30]]
#read_nums = [cov*ref_len/(2*read_lens[0]) for cov in [1, 5]]

for rl in read_lens:
	for err in seq_errs:
		for rn in read_nums:
			ref_path = "/data/nsvo/test-data/GRCh37_chr1/refs/af_sid_mutant/mutant_genome.fasta"
			result_path = "/data/nsvo/test-data/GRCh37_chr1/reads/sim-reads/af_sid_mutant_dwgsim/"
			if not os.path.exists(result_path):
				os.makedirs(result_path)
			os.system("/home/nsvo/genome-tools/DWGSIM/dwgsim -N " + str(rn) + " -1 " + str(rl) + " -2 " + str(rl) \
			+ " -e " + str(err) + " -E " + str(err) + " -r 0 " + ref_path + " " + result_path \
			+ "/dwgsim_reads_" + str(rl) + "." + str(err) + "." + str(rn) + " &")