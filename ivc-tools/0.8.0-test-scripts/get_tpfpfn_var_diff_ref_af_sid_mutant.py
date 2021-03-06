'''
Extract TP, FP, and FN from SNP call results
Usage: python get_tpfpfn_var_diff_ref_af_sid_mutant.py config_file confi_num cov_num result_dir
    E.g.: python get_tpfpfn_var_diff_ref_af_sid_mutant.py config_chr1_test.json 1.14 5 called_var_dir
'''
import os
import sys
import json

if len(sys.argv) != 8:
    print "Usage: python get_tpfpfn_var_diff_ref_af_sid_mutant.py config_file confi_K confi_U confi_1 prof_para cov_num result_dir"
    exit(0)

config_file = open(sys.argv[1])
data = json.load(config_file)
config_file.close()

prog_version = data["ProgVer"]
data_dir = data["DataPath"]["DataDir"]
ref_dir = data["DataPath"]["RefDir"]
index_dir = data["DataPath"]["IndexDir"]
result_dir = data["DataPath"]["ResultDir"]
read_fn = data["DataPath"]["ReadPrefixFile"]
dbsnp_fn = data["DataPath"]["dbsnpFile"]
ref_len = data["RefLen"]

confi_K = float(sys.argv[2])
confi_U = float(sys.argv[3])
confi_1 = float(sys.argv[4])
para = sys.argv[5]
cov_num = sys.argv[6]
result_dn = sys.argv[7]

read_lens = [100]
seq_errs = ['0.00015-0.0015']
read_nums = []
if cov_num == "all":
    read_nums = [cov*ref_len/(2*read_lens[0]) for cov in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 50, 100]]
else:
    read_nums = [cov*ref_len/(2*read_lens[0]) for cov in [int(cov_num)]]

print "Getting ref genome and var prof info..."
chr_pos, chr_name = [], []
data = open(os.path.join(data_dir, index_dir, "index_0.70", "GRCh37.fasta.mgf.idx")).readlines()
for line in data:
    if line[0] == '>':
        info = line.strip().split()
        chr_name.append(info[0][1:])
        chr_pos.append(int(info[1]))
    else:
        break

var_prof = {}
for line in open(dbsnp_fn):
    if line[0] != '#':
        info = line.strip().split()
        offset_pos = -1
        for i in range(len(chr_pos)):
            if info[0] == chr_name[i]:
                offset_pos = chr_pos[i]
                break
        if offset_pos == -1:
            print "Missing chromosome", info[0]
        var_prof[offset_pos + int(info[1]) - 1] = info[3:5]

gatk_confi = 20.0

print "Getting true variants info..."
ref_path = os.path.join(data_dir, ref_dir)
known_var_file = os.path.join(ref_path, "known_var_" + para + ".txt")
unknown_var_file = os.path.join(ref_path, "unknown_var_" + para + ".txt")

true_known_snp, true_known_indel, true_unknown_snp, true_unknown_indel,  = {}, {}, {}, {}
KAKS, NS, KAKID, NID = 0, 0, 0, 0
with open(known_var_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != '#':
            value = line.strip().split()
            pos, known_var = int(value[0]), value[1:]
            if len(var_prof[pos][0]) == 1 and len(var_prof[pos][1]) == 1:
                true_known_snp[pos] = known_var
                if known_var[0] != known_var[1]:
                    KAKS += 1
            else:
                true_known_indel[pos] = known_var
                if known_var[0] != known_var[1]:
                    KAKID += 1

with open(unknown_var_file) as f:
    for line in f.readlines():
        if line.strip() and line[0] != '#':
            value = line.strip().split()
            pos, unknown_var = int(value[0]), value[1:]
            if len(var_prof[pos][0]) == 1 and len(var_prof[pos][1]) == 1:
                true_unknown_snp[pos] = unknown_var
                if unknown_var[0] != unknown_var[1]:
                    NS += 1
            else:
                true_unknown_indel[pos] = unknown_var
                if unknown_var[0] != unknown_var[1]:
                    NID += 1
print KAKS, NS, KAKID, NID

print "Getting and evaluating called variants info..."
fpfntp_info_path = os.path.join(data_dir, result_dir, "ivc_" + para, result_dn, "fpfntp_info")
if not os.path.exists(fpfntp_info_path):
    os.makedirs(fpfntp_info_path)

result_path = os.path.join(data_dir, result_dir, "ivc_" + para, result_dn)
gatk_result_path = os.path.join(data_dir, result_dir, "gatk_hc_realign")

header = "pos\tref\talt\tqual\tvar_prob\tmap_prob\tcom_qual\tbase_num\tbase_qual\tchr_dis\tchr_diff\tmap_prob\taln_prob\tpair_prob\ts_pos1\tbranch1\ts_pos2\tbranch2\tread_header\taln_base\taln_base_num\n"
fp_header = "pos\ttrue_ref\ttrue_alt\tref\talt\tqual\tvar_prob\tmap_prob\tcom_qual\tbase_num\tbase_qual\tchr_dis\tchr_diff\tmap_prob\taln_prob\tpair_prob\ts_pos1\tbranch1\ts_pos2\tbranch2\tread_header\taln_base\taln_base_num\n"

for rl in read_lens:
    for err in seq_errs:
        for rn in read_nums:
            fn_part = read_fn + "_" + str(rl) + "." + str(err) + "." + str(rn)
            gatk_snp = {}
            gatk_var_call_file = gatk_result_path + "/" + fn_part + ".bwa.vcf"
            f = open(gatk_var_call_file)
            for line in f.readlines():
                if line.strip() and line[0] != '#':
                    value = line.strip().split()
                    if float(value[5]) >= gatk_confi:
                        for elem in value[7].split(';'):
                            info = elem.split('=')
                            if info[0] == "DP":
                                dp = info[1]
                        offset_pos = -1
                        for i in range(len(chr_pos)):
                            if value[0] == chr_name[i]:
                                offset_pos = chr_pos[i]
                                break
                        if offset_pos == -1:
                            print "Missing chromosome", value[0]
                        pos = offset_pos + int(value[1]) - 1
                        gatk_snp[pos] = [value[3], value[4], value[5], dp]
            f.close()
            print "GATK # called variants", len(gatk_snp)

            file_prefix = fpfntp_info_path + "/" + fn_part

            tp_snp_known_file = open(file_prefix + ".tp_snp_known." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            tp_snp_known_file.write(header)
            fp_snp_known_file = open(file_prefix + ".fp_snp_known." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fp_snp_known_file.write(fp_header)
            tp_indel_known_file = open(file_prefix + ".tp_indel_known." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            tp_indel_known_file.write(header)
            fp_indel_known_file = open(file_prefix + ".fp_indel_known." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fp_indel_known_file.write(fp_header)

            tp_snp_unknown_file = open(file_prefix + ".tp_snp_unknown." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            tp_snp_unknown_file.write(header)
            fp_snp_unknown_file = open(file_prefix + ".fp_snp_unknown." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fp_snp_unknown_file.write(fp_header)

            tp_indel_unknown_file = open(file_prefix + ".tp_indel_unknown." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            tp_indel_unknown_file.write(header)
            fp_indel_unknown_file = open(file_prefix + ".fp_indel_unknown." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fp_indel_unknown_file.write(fp_header)

            fp_snp_none_file = open(file_prefix + ".fp_snp_none." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fp_snp_none_file.write(header)
            fp_indel_none_file = open(file_prefix + ".fp_indel_none." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fp_indel_none_file.write(header)

            fn_snp_known_file = open(file_prefix + ".fn_snp_known." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fn_snp_known_file.write("pos\tsnp\n")
            fn_snp_unknown_file = open(file_prefix + ".fn_snp_unknown." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fn_snp_unknown_file.write("pos\tsnp\n")

            fn_indel_known_file = open(file_prefix + ".fn_indel_known." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fn_indel_known_file.write("pos\tsnp\n")
            fn_indel_unknown_file = open(file_prefix + ".fn_indel_unknown." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fn_indel_unknown_file.write("pos\tsnp\n")

            fn_snp_known_lowqual_file = open(file_prefix + ".fn_snp_known_lowqual." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fn_snp_unknown_lowqual_file = open(file_prefix + ".fn_snp_unknown_lowqual." + str(confi_K) + "." + str(confi_U) + ".txt", "w")

            fn_indel_known_lowqual_file = open(file_prefix + ".fn_indel_known_lowqual." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fn_indel_unknown_lowqual_file = open(file_prefix + ".fn_indel_unknown_lowqual." + str(confi_K) + "." + str(confi_U) + ".txt", "w")

            fn_snp_known_callgatk_file = open(file_prefix + ".fn_snp_known_callgatk." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fn_snp_unknown_callgatk_file = open(file_prefix + ".fn_snp_unknown_callgatk." + str(confi_K) + "." + str(confi_U) + ".txt", "w")

            fn_indel_known_callgatk_file = open(file_prefix + ".fn_indel_known_callgatk." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fn_indel_unknown_callgatk_file = open(file_prefix + ".fn_indel_unknown_callgatk." + str(confi_K) + "." + str(confi_U) + ".txt", "w")

            fp_snp_none_callgatk_file = open(file_prefix + ".fp_snp_none_callgatk." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fp_indel_none_callgatk_file = open(file_prefix + ".fp_indel_none_callgatk." + str(confi_K) + "." + str(confi_U) + ".txt", "w")

            fp_low_qual_file = open(file_prefix + ".fp_low_qual." + str(confi_K) + "." + str(confi_U) + ".txt", "w")
            fp_low_qual_gatk_file = open(file_prefix + ".fp_low_qual_gatk." + str(confi_K) + "." + str(confi_U) + ".txt", "w")

            var_call, low_qual_snp = {}, {}
            var_call_file = result_path + "/" + fn_part + ".varcall.vcf"
            f = open(var_call_file)
            cn = rn/(ref_len/(2*read_lens[0]))
            for line in f.readlines():
                value = line.strip().split()
                if value[0][0] == '#' or value[3] == value[4]:
                    continue
                offset_pos = -1
                for i in range(len(chr_pos)):
                    if value[0] == chr_name[i]:
                        offset_pos = chr_pos[i]
                        break
                if offset_pos == -1:
                    print "Missing chromosome", value[0]
                pos = offset_pos + int(value[1]) - 1
                if value[5] == "NaN":
                    var_call[pos] = value[3:5]
                if pos in true_known_snp:
                    if float(value[5]) >= confi_K:
                        var_call[pos] = value[3:5]
                elif pos in true_known_indel:
                    if float(value[5]) >= confi_K:
                        var_call[pos] = value[3:5]
                elif len(value[3]) == 1 and len(value[4]) == 1:
                    if float(value[5]) >= confi_U:
                        if cn <= 4:
                            if float(value[12]) > 1.0:
                                var_call[pos] = value[3:5]
                            elif float(value[5]) >= confi_1:
                                var_call[pos] = value[3:5]
                        else:
                            if float(value[12]) > cn/4.0:
                                var_call[pos] = value[3:5]
                else:
                    if float(value[5]) >= confi_U:
                        if cn <= 5:
                            if float(value[12]) > 1.0:
                                var_call[pos] = value[3:5]
                            elif float(value[5]) >= confi_1:
                                var_call[pos] = value[3:5]
                        else:
                            if float(value[12]) > cn/5.0:
                                var_call[pos] = value[3:5]
                if pos not in var_call:
                    low_qual_snp[pos] = value[3:]
                    continue

                var = var_call[pos]
                var_call_info = "\t".join(value[3:6]) + "\t" +  "\t".join(value[9:]) + "\n"
                if pos in true_known_snp or pos in true_known_indel:
                    if pos in true_known_snp:
                        if var == true_known_snp[pos]:
                            tp_snp_known_file.write(str(pos) + "\t" + var_call_info)
                        else:
                            fp_snp_known_file.write(str(pos) + "\t" + true_known_snp[pos][0] + "\t" + true_known_snp[pos][1] + "\t" + var_call_info)
                    elif pos in true_known_indel:
                        if var == true_known_indel[pos]:
                            tp_indel_known_file.write(str(pos) + "\t" + var_call_info)
                        else:
                            fp_indel_known_file.write(str(pos) + "\t" + true_known_indel[pos][0] + "\t" + true_known_indel[pos][1] + "\t" + var_call_info)
                elif pos in true_unknown_snp or pos in true_unknown_indel:
                    if pos in true_unknown_snp:
                        if var == true_unknown_snp[pos]:
                            tp_snp_unknown_file.write(str(pos) + "\t" + var_call_info)
                        else:
                            fp_snp_unknown_file.write(str(pos) + "\t" + true_unknown_snp[pos][0] + "\t" + true_unknown_snp[pos][1] + "\t" + var_call_info)
                    elif pos in true_unknown_indel:
                        if var == true_unknown_indel[pos]:
                            tp_indel_unknown_file.write(str(pos) + "\t" + var_call_info)
                        else:
                            fp_indel_unknown_file.write(str(pos) + "\t" + true_unknown_indel[pos][0] + "\t" + true_unknown_indel[pos][1] + "\t" + var_call_info)
                else:
                    if len(value[3]) == 1 and len(value[4]) == 1:
                        fp_snp_none_file.write(str(pos) + "\t" + var_call_info)
                        if pos in gatk_snp:
                            fp_snp_none_callgatk_file.write(str(pos) + "\t" + var_call_info)
                    else:
                        fp_indel_none_file.write(str(pos) + "\t" + var_call_info)
                        if pos in gatk_snp:
                            fp_indel_none_callgatk_file.write(str(pos) + "\t" + var_call_info)

            f.close()
            print "IVC # called variants", len(var_call)

            #Print FN info
            for pos, value in true_known_snp.iteritems():
                if pos not in var_call and value != var_prof[pos]:
                    fn_snp_known_file.write(str(pos) + "\t" + "\t".join(value) + "\n")
                    if pos in low_qual_snp:
                        fn_snp_known_lowqual_file.write(str(pos) + "\t" + "\t".join(low_qual_snp[pos]) + "\n")
                    if pos in gatk_snp:
                        fn_snp_known_callgatk_file.write(str(pos) + "\t" + "\t".join(gatk_snp[pos]) + "\n")

            for pos, value in true_unknown_snp.iteritems():
                if pos not in var_call:
                    fn_snp_unknown_file.write(str(pos) + "\t" + "\t".join(value) + "\n")
                    if pos in low_qual_snp:
                        fn_snp_unknown_lowqual_file.write(str(pos) + "\t" + "\t".join(low_qual_snp[pos]) + "\n")
                    if pos in gatk_snp:
                        fn_snp_unknown_callgatk_file.write(str(pos) + "\t" + "\t".join(gatk_snp[pos]) + "\n")

            for pos, value in true_known_indel.iteritems():
                if pos not in var_call and value != var_prof[pos]:
                    fn_indel_known_file.write(str(pos) + "\t" + "\t".join(value) + "\n")
                    if pos in low_qual_snp:
                        fn_indel_known_lowqual_file.write(str(pos) + "\t" + "\t".join(low_qual_snp[pos]) + "\n")
                    if pos in gatk_snp:
                        fn_indel_known_callgatk_file.write(str(pos) + "\t" + "\t".join(gatk_snp[pos]) + "\n")

            for pos, value in true_unknown_indel.iteritems():
                if pos not in var_call:
                    fn_indel_unknown_file.write(str(pos) + "\t" + "\t".join(value) + "\n")
                    if pos in low_qual_snp:
                        fn_indel_unknown_lowqual_file.write(str(pos) + "\t" + "\t".join(low_qual_snp[pos]) + "\n")
                    if pos in gatk_snp:
                        fn_indel_unknown_callgatk_file.write(str(pos) + "\t" + "\t".join(gatk_snp[pos]) + "\n")

            for pos, value in low_qual_snp.iteritems():
                if pos not in true_known_snp and pos not in true_unknown_snp \
                    and pos not in true_known_indel and pos not in true_unknown_indel:
                    fp_low_qual_file.write(str(pos) + "\t" + "\t".join(value) + "\n")
                    if pos in gatk_snp:
                        fp_low_qual_gatk_file.write(str(pos) + "\t".join(gatk_snp[pos]) + "\n")

            tp_snp_known_file.close()
            fp_snp_known_file.close()
            tp_snp_unknown_file.close()
            fp_snp_unknown_file.close()
            
            tp_indel_known_file.close()
            fp_indel_known_file.close()
            tp_indel_unknown_file.close()
            fp_indel_unknown_file.close()
            
            fp_snp_none_file.close()
            fp_indel_none_file.close()
            
            fn_snp_known_file.close()
            fn_snp_unknown_file.close()
            
            fn_indel_known_file.close()
            fn_indel_unknown_file.close()
            
            fn_snp_known_lowqual_file.close()
            fn_snp_unknown_lowqual_file.close()
            
            fn_indel_known_lowqual_file.close()
            fn_indel_unknown_lowqual_file.close()

            fn_snp_known_callgatk_file.close()
            fn_snp_unknown_callgatk_file.close()
            
            fn_indel_known_callgatk_file.close()
            fn_indel_unknown_callgatk_file.close()

            fp_snp_none_callgatk_file.close()
            fp_indel_none_callgatk_file.close()

            fp_low_qual_file.close()
            fp_low_qual_gatk_file.close()
