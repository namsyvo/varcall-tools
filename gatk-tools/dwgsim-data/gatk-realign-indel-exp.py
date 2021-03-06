'''
Call variants with GATK
Usage: python gatk-callvar-hc-exp.py config_file coverage_num
'''
import os
import sys
import json

config_file = open(sys.argv[1])
data = json.load(config_file)
config_file.close()

prog_path = data["ProgPath"]
script_path = data["ScriptPath"]
data_path = data["DataPath"]["DataDir"]
genome_fn = data["DataPath"]["GenomeFile"]
result_dir = data["DataPath"]["ResultDir"]
read_fn = data["DataPath"]["ReadPrefixFile"]
dbsnp_fn = data["DataPath"]["dbsnpFile"]
ref_len = data["RefLen"]

cov_num = sys.argv[2]

read_lens = [100]
seq_errs = ['0.00015-0.0015']
read_nums = []
if cov_num == "all":
    #read_nums = [cov*ref_len/(2*read_lens[0]) for cov in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 50, 100]]
    read_nums = [cov*ref_len/(2*read_lens[0]) for cov in [15, 20]]
else:
    read_nums = [cov*ref_len/(2*read_lens[0]) for cov in [int(cov_num)]]

ref_file = os.path.join(data_path, "refs", genome_fn)
sam_path = os.path.join(data_path, result_dir, "bwa")
for rl in read_lens:
    for err in seq_errs:
        for rn in read_nums:
            read_prefix = read_fn + "_" + str(rl) + "." + str(err) + "." + str(rn)
            bam_file = os.path.join(sam_path, read_prefix + ".bwa_sorted_RG.bam")
            result_file = os.path.join(sam_path, read_prefix + ".bwa_sorted_RG_realign.bam")
            cmd = "/usr/bin/time -v " + script_path + "/gatk-realign-indel.sh " + ref_file + " " \
                + bam_file + " " + dbsnp_fn + " " + result_file + " " + prog_path + " 2>" + result_file + ".log"
            print cmd
            os.system(cmd)
