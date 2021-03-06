import sys

dir_name = "/data/nsvo/test-data/GRCh37_chr1/reads/sim-reads/af_sid_mutant_dwgsim"
cov_num = sys.argv[1]
out_fn = sys.argv[2]
read_ids = sys.argv[3:]
ref_len = 249250621
read_nums = int(cov_num)*ref_len/(2*100)
file_names = ["dwgsim_reads_100.0.00015-0.0015." + str(read_nums) + ".bwa.read1.fastq", \
          "dwgsim_reads_100.0.00015-0.0015." + str(read_nums) + ".bwa.read2.fastq"]
for fn in file_names:
    inf = open(dir_name + "/" + fn)
    outf = open(dir_name + "/diff_var_gatk_hc_analysis/" + fn + "." + out_fn, "w")
    r_num = 0
    while True:
        line = inf.readline()
        info = line.strip().split('_')
        if info[len(info)-1].split('/')[0] in read_ids:
            outf_1read = open(dir_name + "/diff_var_gatk_hc_analysis/" + fn + "." + info[len(info)-1].split('/')[0], "w")
            outf.write(line)
            outf_1read.write(line)
            line = inf.readline()
            outf.write(line)
            outf_1read.write(line)
            line = inf.readline()
            outf.write(line)
            outf_1read.write(line)
            line = inf.readline()
            outf.write(line)
            outf_1read.write(line)
            outf_1read.close()
            r_num += 1
        if r_num == len(read_ids):
            break
    outf.close()
