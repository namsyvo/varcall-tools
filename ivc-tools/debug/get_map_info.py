"""
Get alignment info for fp (snp, indel)
Input: result folder, length of read/ref/mut
Ouput: alignment info (read-ref)
Usage: python get_map_info.py called_var_dir length var_type
"""
import sys
import os

def rev_comp(read):
    rev_comp_read = ""
    for elem in read:
        if elem == 'A':
            rev_comp_read += 'T'
        elif elem == 'T':
            rev_comp_read += 'A'
        elif elem == 'C':
            rev_comp_read += 'G'
        elif elem == 'G':
            rev_comp_read += 'C'
        else:
            rev_comp_read += elem
    return rev_comp_read[::-1]

if __name__ == "__main__":

    read_dn = "/data/nsvo/test-data/GRCh37_chr1/reads/sim-reads/af_sid_mutant_dwgsim"
    read_fn = ["dwgsim_reads_100.0.00015-0.0015.6231265.bwa.read1.fastq", "dwgsim_reads_100.0.00015-0.0015.6231265.bwa.read2.fastq"]

    fref = open("/data/nsvo/test-data/GRCh37_chr1/indexes/af_sid_mutant_index/index_0.70/GRCh37_chr1.fasta.mgf")
    ref_seq = ""
    for line in fref:
        if line[0] != '>':
            ref_seq += line.strip()

    fref = open("/data/nsvo/test-data/GRCh37_chr1/refs/af_sid_mutant/mutant_genome.fasta")
    mut_seq = ""
    for line in fref:
        if line[0] != '>':
            mut_seq += line.strip()

    result_path = sys.argv[1]
    dis = int(sys.argv[2])
    var_type = int(sys.argv[3])
    var_num = int(sys.argv[4])

    result_dn = os.path.join("/data/nsvo/test-data/GRCh37_chr1/results/sim-reads/af_sid_mutant_dwgsim/ivc_0.70", result_path, "fpfntp_info")
    fp_fn = ["dwgsim_reads_100.0.00015-0.0015.6231265.fp_snp_none.1.14.txt", \
             "dwgsim_reads_100.0.00015-0.0015.6231265.fp_snp_unknown.1.14.txt", \
             "dwgsim_reads_100.0.00015-0.0015.6231265.fp_snp_known.1.14.txt", \
             "dwgsim_reads_100.0.00015-0.0015.6231265.fp_indel_none.1.14.txt", \
             "dwgsim_reads_100.0.00015-0.0015.6231265.fp_indel_unknown.1.14.txt", \
             "dwgsim_reads_100.0.00015-0.0015.6231265.fp_indel_known.1.14.txt"]

    if not os.path.exists(os.path.join(read_dn, "alignment-analysis")):
        os.makedirs(os.path.join(read_dn, "alignment-analysis"))

    map_outf = open(os.path.join(result_dn, fp_fn[var_type] + "-alignment-analysis"), "w")
    fp_inf = open(os.path.join(result_dn, fp_fn[var_type]))
    line = fp_inf.readline()

    snp_pos, chr_diff, s_pos1, branch1, s_pos2, branch2, header = 0, 0, 0, True, 0, True, ""
    prev_pos = 0
    for j in range(var_num):
        line = fp_inf.readline()
        tmp = line.strip().split()
        if var_type == 0 or var_type == 3:
            snp_pos, chr_diff, s_pos1, branch1, s_pos2, branch2, header = int(tmp[0]), int(tmp[10]), tmp[14], tmp[15], tmp[16], tmp[17], tmp[18]
        else:
            snp_pos, chr_diff, s_pos1, branch1, s_pos2, branch2, header = int(tmp[0]), int(tmp[12]), tmp[16], tmp[17], tmp[18], tmp[19], tmp[20]
        if snp_pos == prev_pos:
            continue
        prev_pos = snp_pos

        #print map info
        map_outf.write(line)
        tmp = header.split("_")
        read_id = tmp[len(tmp) - 1].split("/")[0]            
        #print reads
        reads = []
        for k in [0, 1]:
            read_inf = open(os.path.join(read_dn, read_fn[k]))
            while True:
                line = read_inf.readline()
                info = line.strip().split('_')
                if info[len(info)-1].split('/')[0] == read_id:
                    read_outf = open(os.path.join(read_dn, "alignment-analysis", read_fn[k] + "." + read_id), "w")
                    read_outf.write(line)
                    map_outf.write(line)
                    line = read_inf.readline()
                    read_outf.write(line)
                    map_outf.write(line)
                    reads.append(line.strip())
                    line = read_inf.readline()
                    read_outf.write(line)
                    map_outf.write(line)
                    line = read_inf.readline()
                    read_outf.write(line)
                    map_outf.write(line)
                    map_outf.write("\n")
                    read_outf.close()
                    break

        #print pos1, pos2
        mut_pos, ref_pos, diff = 0, 0, 0
        read = ""
        title = ""
        if header[len(header) - 1] == '1':
            mut_pos = int(tmp[2]) - 1
            ref_pos = mut_pos + chr_diff
            diff = abs(ref_pos - snp_pos)
            if branch1 == "true":
                read = reads[0]
                title = "1st-align"
            else:
                read = rev_comp(reads[0])
                title = "1st-RC-align"
        else:
            mut_pos = int(tmp[3]) - 1
            ref_pos = mut_pos + chr_diff + 1
            diff = abs(ref_pos - snp_pos)
            if branch2 == "true":
                read = reads[1]
                title = "2nd-align"
            else:
                read = rev_comp(reads[1])
                title = "2nd-RC-align"

        map_outf.write("\t".join(["mut_seq", str(mut_pos), str(dis)]) + "\n")
        map_outf.write(mut_seq[mut_pos : mut_pos + dis] + "\n")
        map_outf.write("\t".join(["ref_seq", str(ref_pos), str(dis), str(diff)]) + "\n")
        map_outf.write(ref_seq[ref_pos : ref_pos + dis] + "\n")
        map_outf.write("\n")

        map_outf.write(title + "\n")
        map_outf.write(read + "\n")
        map_outf.write(ref_seq[ref_pos : ref_pos + dis] + "\n")
        map_outf.write("----------------------------------------------------------------\n\n")

    map_outf.close()
