import os

data_path = "/home/SNP/NC_016088.1_soybean"
index_path = data_path + "/bwa-index"
reads_path = data_path + "/chr1_mutate1/reads/3-14-2014"
results_path = data_path + "/chr1_mutate1/results/3-14-2014-BWA"

prog_path = "/home/nsvo/genome-tools/bwa-0.7.7"

for cvr in ['1x', '2x', '3x', '5x', '7x', '10x']:
	for seq_err in ['0.01', '0.02', '0.04']:
		cmd = "time " + prog_path + "/bwa bwasw " + index_path + "/GRCh37_chr20.fasta " \
		+ reads_path + "/reads-100." + seq_err + "." + cvr + ".fq > " \
		+ results_path + "/reads-100." + seq_err + "." + cvr + ".bwasw.sam &"
		print cmd
		os.system(cmd)

