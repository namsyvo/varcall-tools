'''
Evaluate variant call results for real data
'''

import os
import sys
import json
from datetime import datetime

if len(sys.argv) != 5:
    print "Usage: python eval_var_af_sid_mutant_diff_ref.py chr_name cov confi_S confi_I"
    exit(0)

chr_name = sys.argv[1]
cov = sys.argv[2]
confi_S = float(sys.argv[3])
confi_I = float(sys.argv[4])

#var_prof_file = os.path.join("/backup2/nsvo/variant_calling/Human_data/refs/NA12878/NA12878.vcf")
var_prof_file = os.path.join("/backup2/nsvo/variant_calling/Human_data/refs/NA12878/NISTIntegratedCalls.vcf")
var_prof = {}
KS, KI = 0, 0
with open(var_prof_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != "#":
            value = line.strip().split("\t")
            
            #ignore het var
            if value[9].split(":")[0] != "1/1" and value[9].split(":")[0] != "1|1":
                continue
            
            #if value[0] == "chr" + chr_name:
            if value[0] == chr_name:
                var_prof[int(value[1]) - 1] = value[3:5] + value[9].split(":")[0:1]
                if len(value[3]) == 1 and len(value[4]) == 1:
                    KS += 1
                else:
                    KI += 1
print "#var prof variants", KS, KI, KS + KI

dbsnp_var_prof = {}
dbsnp_var_prof_file = os.path.join("/backup2/nsvo/variant_calling/Human_data/refs/GRCh37_chr" + chr_name + "/TRIMMED.ALL.chr" + chr_name + ".integrated_phase1_v3.20101123.snps_indels_svs.genotypes.vcf")
DS_KS, DS_KI = 0, 0
with open(dbsnp_var_prof_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != "#":
            value = line.strip().split("\t")
            if value[0] == chr_name:
                dbsnp_var_prof[int(value[1]) - 1] = value[3:5]
                if len(value[3]) == 1 and len(value[4]) == 1:
                    DS_KS += 1
                else:
                    DS_KI += 1
print "#var dbsnp variants", DS_KS, DS_KI, DS_KS + DS_KI

result_path = os.path.join("/data/nsvo/test_data/GRCh37_chr" + chr_name + "/results/real_reads/NA12878")

var_call_file = os.path.join(result_path, "ivc_0.8.1_exome/ERR194147_shuf_" + cov + "x_chr" + chr_name + ".ivc.vcf")
var_call = {}
with open(var_call_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != '#':
            value = line.strip().split("\t")
            pos = int(value[1]) - 1
            if pos in dbsnp_var_prof:
                if len(value[3]) == 1 and len(value[4]) == 1:
                    if float(value[5]) >= confi_S:
                        var_call[pos] = value[3:5] + value[12:14]
                else:
                    if float(value[5]) >= confi_I:
                        var_call[pos] = value[3:5] + value[12:14]
            else:
                if len(value[3]) == 1 and len(value[4]) == 1:
                    if float(value[5]) >= confi_S:
                        var_call[pos] = value[3:5] + value[12:14]
                else:
                    if float(value[5]) >= confi_I:
                        var_call[pos] = value[3:5] + value[12:14]
print "#called variants", len(var_call)

hc_file = os.path.join(result_path, "gatk_hc/ERR194147_shuf_" + cov + "x_chr" + chr_name + ".bwa_sorted_RG_realign.vcf")
hc_var = {}
with open(hc_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != "#":
            value = line.strip().split("\t")
            
            if value[9].split(":")[0] != "1/1" and value[9].split(":")[0] != "1|1":
                continue
            
            if float(value[5]) >= 20:
                hc_var[int(value[1]) - 1] = value[3:6] + value[9].split(":")[0:1]
print "#cmp variants", len(hc_var)

st_file = os.path.join(result_path, "samtools/ERR194147_shuf_" + cov + "x_chr" + chr_name + ".bwa_sorted_RG_realign.norm.vcf")
st_var = {}
with open(st_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != "#":
            value = line.strip().split("\t")
            
            if value[9].split(":")[0] != "1/1" and value[9].split(":")[0] != "1|1":
                continue
            
            if float(value[5]) >= 20:
                st_var[int(value[1]) - 1] = value[3:6] + value[9].split(":")[0:1]
print "#cmp variants", len(st_var)

KA_KS, NA_KS, KA_KI, NA_KI, NS, NI = 0, 0, 0, 0, 0, 0
NS_DS, NI_DI = 0, 0
KA_KS_DS, KA_KS_HC, KA_KS_ST, KA_KI_DI, KA_KI_HC, KA_KI_ST, KA_KS_HC_ST, KA_KI_HC_ST = 0, 0, 0, 0, 0, 0, 0, 0
NS_DS_HC, NS_DS_ST, NS_DS_HC_ST, NS_HC, NS_ST, NS_HC_ST, NI_DI_HC, NI_DI_ST, NI_DI_HC_ST, NI_HC, NI_ST, NI_HC_ST = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
for var_pos, var in var_call.iteritems():
    if var_pos in var_prof:
        if len(var[0]) == 1 and len(var[1]) == 1:
            if set(var[0:2]) == set(var_prof[var_pos][0:2]):
                KA_KS += 1
                if var_pos in dbsnp_var_prof and set(var[0:2]) == set(dbsnp_var_prof[var_pos]):
                    KA_KS_DS += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]):
                    KA_KS_HC += 1
                if var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    KA_KS_ST += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]) and var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    KA_KS_HC_ST += 1
            else:
                NA_KS += 1
        else:
            if set(var[0:2]) == set(var_prof[var_pos][0:2]):
                KA_KI += 1
                if var_pos in dbsnp_var_prof and set(var[0:2]) == set(dbsnp_var_prof[var_pos]):
                    KA_KI_DI += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]):
                    KA_KI_HC += 1
                if var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    KA_KI_ST += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]) and var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    KA_KI_HC_ST += 1
            else:
                NA_KI += 1
    else:
        if len(var[0]) == 1 and len(var[1]) == 1:
            if float(var[2])/float(var[3]) <= 0.75 or int(var[2]) < 2: #ignore possible het var
                continue
            if var_pos in dbsnp_var_prof and set(var[0:2]) == set(dbsnp_var_prof[var_pos]):
                NS_DS += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]):
                    NS_DS_HC += 1
                if var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    NS_DS_ST += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]) and var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    NS_DS_HC_ST += 1
            else:
                NS += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]):
                    NS_HC += 1
                if var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    NS_ST += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]) and var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    NS_HC_ST += 1
        else:
            if float(var[2])/float(var[3]) <= 0.5 or int(var[2]) < 2:#ignore possible het var
                continue
            if var_pos in dbsnp_var_prof and set(var[0:2]) == set(dbsnp_var_prof[var_pos]):
                NI_DI += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]):
                    NI_DI_HC += 1
                if var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    NI_DI_ST += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]) and var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    NI_DI_HC_ST += 1
            else:
                NI += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]):
                    NI_HC += 1
                if var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    NI_ST += 1
                if var_pos in hc_var and set(var[0:2]) == set(hc_var[var_pos][0:2]) and var_pos in st_var and set(var[0:2]) == set(st_var[var_pos][0:2]):
                    NI_HC_ST += 1

S = KA_KS + NA_KS + NS_DS + NS
I = KA_KI + NA_KI + NI_DI + NI

result_file_path = os.path.join(result_path, "ivc_0.8.1_exome/ERR194147_shuf_" + cov + "x_chr" + chr_name + ".ivc.vcf.prec_rec.GIAB." + str(confi_S) + "." + str(confi_I) + ".txt")
result_file = open(result_file_path, "w")

header = ["Alg", "Cov", "Qual", "KA_KS", "KA_KS_DS", "KA_KS_HC", "KA_KS_ST", "KA_KS_HC_ST", "NA_KS", "KA_KI", "KA_KI_DI", "KA_KI_HC", "KA_KI_ST", "KA_KI_HC_ST", "NA_KI", "NS_DS", "NS_DS_HC", "NS_DS_ST", "NS_DS_HC_ST", "NS", "NS_HC", "NS_ST", "NS_HC_ST", "NI_DI", "NI_DI_HC", "NI_DI_ST", "NI_DI_HC_ST", "NI", "NI_HC", "NI_ST", "NI_HC_ST", "KS", "KI", "KS+KI", "CS", "CI", "CS+CI", "PS", "RS", "PI", "RI"]

result_file.write("\t".join(header) + "\n")
result_file.write("IVC_0.8.1\t50\t" + str(confi_S) + "," + str(confi_I) + "\t")
result_file.write("%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t" % (KA_KS, KA_KS_DS, KA_KS_HC, KA_KS_ST, KA_KS_HC_ST, NA_KS, KA_KI, KA_KI_DI, KA_KI_HC, KA_KI_ST, KA_KI_HC_ST, NA_KI, NS_DS, NS_DS_HC, NS_DS_ST, NS_DS_HC_ST, NS, NS_HC, NS_ST, NS_HC_ST, NI_DI, NI_DI_HC, NI_DI_ST, NI_DI_HC_ST, NI, NI_HC, NI_ST, NI_HC_ST))
result_file.write("%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5f\t%.5f\t%.5f\t%.5f" % (KS, KI, KS + KI, S, I, S+I, KA_KS/float(S), KA_KS/float(KS), KA_KI/float(I), KA_KI/float(KI)))
result_file.close()
print "Check results at:", result_file_path
