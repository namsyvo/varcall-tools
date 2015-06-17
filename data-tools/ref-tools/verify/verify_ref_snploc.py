B'''
ref_path = "/home/SNP/NC_016088.1_soybean/index/"
#ref_path = "/home/SNP/GRCh37_human/index/"
ref = []
f1;2c=open(ref_path + "/genomestar.txt")
#f=open(ref_path + "/GRCh37_chr20.fasta")
for line in f.readlines():
	if line.strip():
		ref.extend(line.strip())
print len(ref)
print ref[0], ref[len(ref)-1]
'''
import sys
snp_loc = {}
f=open(sys.argv[1])
for line in f.readlines():
	tmp = line.strip().split()
	snp_loc[int(tmp[0])] = tmp[1:]
#print len(snp_loc)

import numpy as np
prev_key = 0
dis = []
for key in sorted(snp_loc):
        dis.append(int(key) - prev_key)
        prev_key = int(key)
print np.mean(dis), np.var(dis)
print np.min(dis), np.max(dis)
