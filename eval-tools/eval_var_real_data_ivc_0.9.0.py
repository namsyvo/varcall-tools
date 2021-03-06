'''
Evaluate variant call results for real data
'''

import os
import sys

if len(sys.argv) != 8:
    print "Usage: python eval_var_real_data_ivc_0.9.1.py ivc_dir chr_name cov_num confi_S_K confi_I_K confi_S_U confi_I_U"
    exit(0)

ivc_dir = sys.argv[1]
chr_name = sys.argv[2]
cov_num = sys.argv[3]
confi_S_K = float(sys.argv[4])
confi_I_K = float(sys.argv[5])
confi_S_U = float(sys.argv[6])
confi_I_U = float(sys.argv[7])

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

#var_prof_file = os.path.join("/backup2/nsvo/variant_calling/Human_data/refs/NA12878/NA12878.vcf")
var_prof_file = os.path.join("/backup2/nsvo/variant_calling/Human_data/refs/NA12878/NISTIntegratedCalls.vcf")
var_prof = {}
TS, TI, TS_KS, TI_KI = 0, 0, 0, 0
with open(var_prof_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != "#":
            value = line.strip().split("\t")
            '''
            if value[9].split(":")[0] != "1/1" and value[9].split(":")[0] != "1|1":
                continue
            '''
            #if value[0] == "chr" + chr_name:
            if value[0] == chr_name:
                var_pos = int(value[1]) - 1
                var_val = value[3:5] + value[9].split(":")[0:1]
                var_prof[var_pos] = var_val
                if var_pos in dbsnp_var_prof and var_val[0:2] == dbsnp_var_prof[var_pos]:
                    if len(value[3]) == 1 and len(value[4]) == 1:
                        TS_KS += 1
                    else:
                        TI_KI += 1
                if len(value[3]) == 1 and len(value[4]) == 1:
                    TS += 1
                else:
                    TI += 1
print "#var prof variants", TS, TI, TS + TI, TS_KS, TI_KI, TS_KS + TI_KI

result_path = os.path.join("/data/nsvo/test_data/GRCh37_chr" + chr_name + "/results/real_reads/NA12878")

var_call_file = os.path.join(result_path, "ivc_0.9.1/" + ivc_dir +"/ERR194147_shuf_" + cov_num + "_chr" + chr_name + ".ivc.vcf")
var_call, var_call_all = {}, {}
with open(var_call_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != '#':
            value = line.strip().split("\t")
            ref_hap = value[3].split("|")
            var_hap = value[4].split("|")
            if '-' in set(ref_hap + var_hap):
                continue
            '''
            #ignore het var
            ref_hap = value[3].split("|")
            var_hap = value[4].split("|")
            if len(ref_hap) == 2:
                if ref_hap[0] != ref_hap[1]:
                    continue
            elif len(var_hap) == 2:
                if var_hap[0] != var_hap[1]:
                    continue
            '''
            pos = int(value[1]) - 1
            var_call_all[pos] = value[3:6] + value[9:]
            if pos in dbsnp_var_prof:
                if len(value[3]) == 1 and len(value[4]) == 3:
                    if float(value[5]) >= confi_S_K and int(value[12]) >= 1 and int(value[13]) >= 1:
                    #if float(value[5]) >= confi_S_K and float(value[12])/int(value[13]) >= 0.25:
                        var_call[pos] = value[3:6] + value[9:]
                else:
                    if float(value[5]) >= confi_I_K and int(value[12]) >= 1 and int(value[13]) >= 1:
                    #if float(value[5]) >= confi_I_K and float(value[12])/int(value[13]) >= 0.25:
                        var_call[pos] = value[3:6] + value[9:]
            else:
                if len(value[3]) == 1 and len(value[4]) == 3:
                    if float(value[5]) >= confi_S_U and int(value[12]) >= 1 and int(value[13]) >= 1:
                    #if float(value[5]) >= confi_S_U and float(value[12])/int(value[13]) >= 0.25:
                        var_call[pos] = value[3:6] + value[9:]
                else:
                    if float(value[5]) >= confi_I_U and int(value[12]) >= 1 and int(value[13]) >= 1:
                    #if float(value[5]) >= confi_I_U and float(value[12])/int(value[13]) >= 0.25:
                        var_call[pos] = value[3:6] + value[9:]
print "#called variants", len(var_call), len(var_call_all)

cmp_tool_file = os.path.join(result_path, "gatk_hc/ERR194147_shuf_" + cov_num + "_chr" + chr_name + ".bwa_sorted_RG_realign.vcf")
cmp_tool_var = {}
'''
with open(cmp_tool_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != "#":
            value = line.strip().split("\t")
            
            if value[9].split(":")[0] != "1/1" and value[9].split(":")[0] != "1|1":
                continue
            
            if float(value[5]) >= 20:
                cmp_tool_var[int(value[1]) - 1] = value[3:6] + value[9].split(":")[0:1]
print "#cmp variants", len(cmp_tool_var)
'''
#analysis_dir = os.path.join(result_path, "ivc_0.9.1/" + ivc_dir +"/cmp_to_gatk_" + cov_num + "_platinum")
analysis_dir = os.path.join(result_path, "ivc_0.9.1/" + ivc_dir +"/cmp_to_gatk_" + str(confi_S_K) + "." + str(confi_I_K) + "." + str(confi_S_U) + "." + str(confi_I_U) + "_" + ivc_dir + "_" + cov_num + "_giab")
if not os.path.exists(analysis_dir):
    os.mkdir(analysis_dir)

out_file1 = open(os.path.join(analysis_dir, "gatk_miscall_tp_snp"), "w")
out_file2 = open(os.path.join(analysis_dir, "gatk_notcall_tp_snp"), "w")
out_file3 = open(os.path.join(analysis_dir, "gatk_miscall_tp_indel"), "w")
out_file4 = open(os.path.join(analysis_dir, "gatk_notcall_tp_indel"), "w")

out_file5 = open(os.path.join(analysis_dir, "gatk_call_ns"), "w")
out_file6 = open(os.path.join(analysis_dir, "gatk_notcall_ns"), "w")
out_file7 = open(os.path.join(analysis_dir, "gatk_call_ni"), "w")
out_file8 = open(os.path.join(analysis_dir, "gatk_notcall_ni"), "w")

KA_KS, KA_KS_DS, NA_KS, NA_KS_DS, KA_KI, KA_KI_DI, NA_KI, NA_KI_DI, NS, NS_DS, NI, NI_DI = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
for var_pos, var in var_call.iteritems():
    if var_pos in var_prof:
        if len(var[0]) == 1 and len(var[1]) == 3:
            alleles = var[1].split("|")
            if set(var[0].split("|") + var[1].split("|")) == set(var_prof[var_pos][0:2]):
                if var_pos in dbsnp_var_prof and set(var[0].split("|") + var[1].split("|")) == set(dbsnp_var_prof[var_pos]):
                    KA_KS_DS += 1
                else:
                    KA_KS += 1
                if var_pos in cmp_tool_var and set(var_prof[var_pos][0:2]) != set(cmp_tool_var[var_pos][0:2]):
                    out_file1.write(str(var_pos + 1) + "\t" + str(var) + "\t" + str(cmp_tool_var[var_pos]) + "\n")
                elif var_pos not in cmp_tool_var:
                    out_file2.write(str(var_pos + 1) + "\t" + str(var) + "\n")
            else:
                if var_pos in dbsnp_var_prof and set(var[0].split("|") + var[1].split("|")) == set(dbsnp_var_prof[var_pos]):
                    NA_KS_DS += 1
                else:
                    NA_KS += 1
        else:
            if set(var[0].split("|") + var[1].split("|")) == set(var_prof[var_pos][0:2]):
                if var_pos in dbsnp_var_prof and set(var[0].split("|") + var[1].split("|")) == set(dbsnp_var_prof[var_pos]):
                    KA_KI_DI += 1
                else:
                    KA_KI += 1
                if var_pos in cmp_tool_var and set(var_prof[var_pos][0:2]) != set(cmp_tool_var[var_pos][0:2]):
                    out_file3.write(str(var_pos + 1) + "\t" + str(var) + "\t" + str(cmp_tool_var[var_pos]) + "\n")
                elif var_pos not in cmp_tool_var:
                    out_file4.write(str(var_pos + 1) + "\t" + str(var) + "\n")
            else:
                if var_pos in dbsnp_var_prof and set(var[0].split("|") + var[1].split("|")) == set(dbsnp_var_prof[var_pos]):
                    NA_KI_DI += 1
                else:
                    NA_KI += 1
    else:
        if len(var[0]) == 1 and len(var[1]) == 3:
            if var_pos in dbsnp_var_prof and set(var[0].split("|") + var[1].split("|")) == set(dbsnp_var_prof[var_pos]):
                NS_DS += 1
            else:
                NS += 1
            if var_pos in cmp_tool_var:
                out_file5.write(str(var_pos + 1) + "\t" + str(var) + "\t" + str(cmp_tool_var[var_pos]) + "\n")
            else:
                out_file6.write(str(var_pos + 1) + "\t" + str(var) + "\n")
        else:
            if var_pos in dbsnp_var_prof and set(var[0].split("|") + var[1].split("|")) == set(dbsnp_var_prof[var_pos]):
                NI_DI += 1
            else:
                NI += 1
            if var_pos in cmp_tool_var:
                out_file7.write(str(var_pos + 1) + "\t" + str(var) + "\t" + str(cmp_tool_var[var_pos]) + "\n")
            else:
                out_file8.write(str(var_pos + 1) + "\t" + str(var) + "\n")

out_file1.close()
out_file2.close()
out_file3.close()
out_file4.close()

out_file5.close()
out_file6.close()
out_file7.close()
out_file8.close()

out_file1 = open(os.path.join(analysis_dir, "ivc_notcall_snp"), "w")
out_file2 = open(os.path.join(analysis_dir, "ivc_notcall_indel"), "w")
out_file3 = open(os.path.join(analysis_dir, "ivc_miscall_snp"), "w")
out_file4 = open(os.path.join(analysis_dir, "ivc_miscall_indel"), "w")
for var_pos, var in var_prof.iteritems():
    if var_pos not in var_call_all:
        if len(var[0]) == 1 and len(var[1]) == 1:
            out_file1.write(str(var_pos + 1) + "\t" + str(var) + "\n")
        else:
            out_file2.write(str(var_pos + 1) + "\t" + str(var) + "\n")
    elif var_pos in var_call_all and set(var[0:2]) != set(var_call_all[var_pos][0].split("|") + var_call_all[var_pos][1].split("|")):
        if len(var[0]) == 1 and len(var[1]) == 1:
            out_file3.write(str(var_pos + 1) + "\t" + str(var) + "\t" + str(var_call_all[var_pos]) + "\n")
        else:
            out_file4.write(str(var_pos + 1) + "\t" + str(var) + "\t" + str(var_call_all[var_pos]) + "\n")
out_file1.close()
out_file2.close()
out_file3.close()
out_file4.close()

CS = KA_KS + KA_KS_DS + NA_KS + NA_KS_DS + NS_DS + NS
CI = KA_KI + KA_KI_DI + NA_KI + NA_KI_DI + NI_DI + NI

#result_file_path = os.path.join(result_path, "ivc_0.9.1/" + ivc_dir + "/ERR194147_shuf_" + cov_num + "_chr" + chr_name + ".ivc.vcf.prec_rec.Platinum." + str(confi_S_K) + "." + str(confi_I_K) + "." + str(confi_S_U) + "." + str(confi_I_U) + ".txt")
result_file_path = os.path.join(result_path, "ivc_0.9.1/" + ivc_dir + "/ERR194147_shuf_" + cov_num + "_chr" + chr_name + ".ivc.vcf.prec_rec.GIAB." + str(confi_S_K) + "." + str(confi_I_K) + "." + str(confi_S_U) + "." + str(confi_I_U) + ".txt")
result_file = open(result_file_path, "w")

#header = ["Alg", "cov_num", "Qual", "KA_KS", "KA_KS_DS", "NA_KS", "NA_KS_DS", "KA_KI", "KA_KI_DI", "NA_KI", "NA_KI_DI", "NS", "NS_DS", "NI", "NI_DI", "S", "I", "S+I", "CS", "CI", "CS+CI", "PS", "RS", "PI", "RI"]
header = ["Alg", "cov_num", "Qual", "TP_U_S", "TP_K_S", "TL_FP_U_S", "TL_FP_K_S", "TP_U_I", "TP_K_I", "TL_FP_U_I", "TL_FP_K_I", "FL_FP_U_S", "FL_FP_K_S", "FL_FP_U_I", "FL_FP_K_I", "TS", "TI", "TS+TI", "CS", "CI", "CS+CI", "PS", "RS", "PI", "RI"]

result_file.write("\t".join(header) + "\n")
result_file.write("IVC_0.9.1\t" + cov_num + "\t" + str(confi_S_K) + "," + str(confi_I_K) + "," + str(confi_S_U) + "," + str(confi_I_U) + "\t")
result_file.write("%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t" % (KA_KS, KA_KS_DS, NA_KS, NA_KS_DS, KA_KI, KA_KI_DI, NA_KI, NA_KI_DI, NS, NS_DS, NI, NI_DI))
result_file.write("%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5d\t%.5f\t%.5f\t%.5f\t%.5f" % (TS, TI, TS + TI, CS, CI, CS+CI, KA_KS/float(CS), KA_KS/float(TS), KA_KI/float(CI), KA_KI/float(TI)))
result_file.close()
print "Check results at:", result_file_path
