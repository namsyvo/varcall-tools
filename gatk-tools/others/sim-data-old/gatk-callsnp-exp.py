import os
import sys

config_file = sys.argv[1]
f=open(config_file)
prog_path = f.readline().strip()
data_path = f.readline().strip()
genome_fn = f.readline().strip()
dbsnp_fn = f.readline().strip()
read_fn = f.readline().strip()
f.close()

ref_len = 249250621
#ref_para = ['0.0000', '0.0825', '0.1650', '0.2475', '0.3300']
read_lens = [100]
seq_errs = ['0.00015-0.0015']
read_nums = [cov*ref_len/(2*read_lens[0]) for cov in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30]]

ref_path = data_path + "/refs"
tool_path = "/home/nsvo/genome-tools"

#for para in ref_para[4:5]:
for rl in read_lens:
    for err in seq_errs:
        for rn in read_nums[1:]:
            sam_path = data_path + "/results/sim-reads/new_mutant_dwgsim/bwa"
            result_path = data_path + "/results/sim-reads/new_mutant_dwgsim/gatk"
            if not os.path.exists(result_path):
                os.makedirs(result_path)
            bam_file = sam_path + "/" + read_fn + "_" + str(rl) + "." + str(err) + "." + str(rn) + ".bwa_sorted_RG.bam "
            result_file = result_path + "/" + read_fn + "_" + str(rl) + "." + str(err) + "." + str(rn) + ".bwa.vcf"
            cmd = prog_path + "/gatk-callsnp.sh " + ref_path + "/GRCh37_chr1.fasta " \
                + bam_file + " " + ref_path +  "/" + dbsnp_fn + " " + result_file + " " + tool_path + " 2>" + result_file + ".log &"
            os.system(cmd)
