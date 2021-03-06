import os
import sys
import json

config_file = open(sys.argv[1])
data = json.load(config_file)
config_file.close()

prog_version = data["ProgVer"]
data_path = data["DataPath"]["DataDir"]
ref_dir = data["DataPath"]["RefDir"]
genome_fn = data["DataPath"]["GenomeFile"]
result_dir = data["DataPath"]["ResultDir"]
read_fn = data["DataPath"]["ReadPrefixFile"]

confi = float(sys.argv[2])

ref_len = 249250621
ref_para = ['0.0000', '0.0825', '0.1650', '0.2475', '0.3300']
read_lens = [100]
seq_errs = ['0.00015-0.0015']
read_nums = [cov*ref_len/(2*read_lens[0]) for cov in [10]]

ref_path = os.path.join(data_path, ref_dir)
genome_file = os.path.join(ref_path, genome_fn)

result_dn = sys.argv[3]
filter_num = 16836

for para in ref_para[4:5]:

    true_snp_comp, true_indel_comp, true_snp_part, true_indel_part, true_snp_none, true_indel_none = {}, {}, {}, {}, {}, {}

    variant_comp_file = os.path.join(ref_path, "mutate-" + para, "variant_comp.txt")
    variant_part_file = os.path.join(ref_path, "mutate-" + para, "variant_part.txt")
    variant_none_file = os.path.join(ref_path, "mutate-" + para, "variant_none.txt")

    with open(variant_comp_file) as f:
        for line in f.readlines():
            if line.strip():
                value = line.strip().split()
                if len(value[1]) == 1 and value[1] != ".":
                    true_snp_comp[int(value[0])] = value[1]
                else:
                    true_indel_comp[int(value[0])] = value[1]

    with open(variant_part_file) as f:
        for line in f.readlines():
            if line.strip():
                value = line.strip().split()
                if len(value[1]) == 1 and value[1] != ".":
                    true_snp_part[int(value[0])] = value[1]
                else:
                    true_indel_part[int(value[0])] = value[1]

    with open(variant_none_file) as f:
        for line in f.readlines():
            if line.strip():
                value = line.strip().split()
                if len(value[1]) == 1 and value[1] != ".":
                    true_snp_none[int(value[0])] = value[1]
                else:
                    true_indel_none[int(value[0])] = value[1]

    trace_info_path = os.path.join(data_path, result_dir, "mutate-" + para + "-dwgsim", "isc", "debug", "trace-info", result_dn, "filter")
    if not os.path.exists(trace_info_path):
        os.makedirs(trace_info_path)
    result_path = os.path.join(data_path, result_dir, "mutate-" + para + "-dwgsim", "isc", "debug", result_dn)

    for rl in read_lens:
        for err in seq_errs:
            for rn in read_nums:
                file_prefix = trace_info_path + "/" + read_fn + "." + str(rl) + "." + str(err) + "." + str(rn)

                tp_snp_none_file = open(file_prefix + ".tp_snp_none." + str(confi) + ".txt", "w")
                fp_snp_none_file = open(file_prefix + ".fp_snp_none." + str(confi) + ".txt", "w")
                tp_indel_none_file = open(file_prefix + ".tp_indel_none." + str(confi) + ".txt", "w")
                fp_indel_none_file = open(file_prefix + ".fp_indel_none." + str(confi) + ".txt", "w")

                tp_snp_part_file = open(file_prefix + ".tp_snp_part." + str(confi) + ".txt", "w")
                fp_snp_part_file = open(file_prefix + ".fp_snp_part." + str(confi) + ".txt", "w")
                tp_indel_part_file = open(file_prefix + ".tp_indel_part." + str(confi) + ".txt", "w")
                fp_indel_part_file = open(file_prefix + ".fp_indel_part." + str(confi) + ".txt", "w")

                tp_snp_comp_file = open(file_prefix + ".tp_snp_comp." + str(confi) + ".txt", "w")
                fp_snp_comp_file = open(file_prefix + ".fp_snp_comp." + str(confi) + ".txt", "w")
                tp_indel_comp_file = open(file_prefix + ".tp_indel_comp." + str(confi) + ".txt", "w")
                fp_indel_comp_file = open(file_prefix + ".fp_indel_comp." + str(confi) + ".txt", "w")

                fp_snp_other_file = open(file_prefix + ".fp_snp_other." + str(confi) + ".txt", "w")
                fp_indel_other_file = open(file_prefix + ".fp_indel_other." + str(confi) + ".txt", "w")

                snp = {}
                all_snp = {}
                called_snp_file = result_path + "/" + read_fn + "-" + str(rl) + "." + str(err) + "." + str(rn) + ".4096.snpcall.32.vcf"
                f = open(called_snp_file)
                for line in f.readlines():
                    value = line.strip().split()
                    if float(value[2]) >= confi:
                        snp[int(value[0]) - 1] = value
                    all_snp[int(value[0]) - 1] = value

                sorted_snp = sorted(snp.iteritems(), key=lambda x: float(x[1][2]), reverse=True)

                for key, value in sorted_snp[len(sorted_snp) - filter_num : len(sorted_snp)]:
                    val_info = str(key) + "\t" + "\t".join(value[1:]) + "\n"
                    if key in true_snp_comp or key in true_indel_comp:
                        if key in true_snp_comp:
                            if value[1] == true_snp_comp[key]:
                                tp_snp_comp_file.write(val_info)
                            else:
                                fp_snp_comp_file.write(val_info)
                        elif key in true_indel_comp:
                            if value[1] == true_indel_comp[key]:
                                tp_indel_comp_file.write(val_info)
                            else:
                                fp_indel_comp_file.write(val_info)
                    elif key in true_snp_part or key in true_indel_part:
                        if key in true_snp_part:
                            if value[1] == true_snp_part[key]:
                                tp_snp_part_file.write(val_info)
                            else:
                                fp_snp_part_file.write(val_info)
                        elif key in true_indel_part:
                            if value[1] == true_indel_part[key]:
                                tp_indel_part_file.write(val_info)
                            else:
                                fp_indel_part_file.write(val_info)
                    elif key in true_snp_none or key in true_indel_none:
                        if key in true_snp_none:
                            if value[1] == true_snp_none[key]:
                                tp_snp_none_file.write(val_info)
                            else:
                                fp_snp_none_file.write(val_info)
                        elif key in true_indel_none:
                            if value[1] == true_indel_none[key]:
                                tp_indel_none_file.write(val_info)
                            else:
                                fp_indel_none_file.write(val_info)
                    else:
                            if len(value[1]) == 1:
                                fp_snp_other_file.write(val_info)
                            else:
                                fp_indel_other_file.write(val_info)

                tp_snp_comp_file.close()
                fp_snp_comp_file.close()
                tp_snp_part_file.close()
                fp_snp_part_file.close()
                tp_snp_none_file.close()
                fp_snp_none_file.close()

                tp_indel_comp_file.close()
                fp_indel_comp_file.close()
                tp_indel_part_file.close()
                fp_indel_part_file.close()
                tp_indel_none_file.close()
                fp_indel_none_file.close()

                fp_snp_other_file.close()
                fp_indel_other_file.close()