for i in range(2, 23):
        #fn = "/data/nsvo/test-data/GRCh37_chr1/refs/af_mutant/snp_prof.vcf"
        #f = open("/data/nsvo/test-data/GRCh37_chr1/refs/af_mutant/known_variants.txt")
        fn = "/backup2/nsvo/variant_calling/Human_data/refs/GRCh37_chr" + str(i) + "/ALL.chr" + str(i) + ".integrated_phase1_v3.20101123.snps_indels_svs.genotypes.vcf"
        ins_num, del_num = 0, 0
        ins_len2_num, del_len2_num = 0, 0
        r_ins_num, r_del_num = 0, 0
        r_ins_len2_num, r_del_len2_num = 0, 0
        
        print fn
        f = open(fn)
        for line in f:
                if line[0] == '#':
                        continue
                tmp = line.strip().split()
                ins = tmp[4]
                if len(ins) > 1:
                        ins_num += 1
                        flag = True
                        for i in range(1, len(ins)):
                                if ins[i] != ins[i - 1]:
                                        flag = False
                        if flag:
                                r_ins_num += 1
                                print ins
                dels = tmp[3]
                if len(dels) > 1:
                        del_num += 1
                        flag = True
                        for i in range(1, len(dels)):
                                if dels[i] != dels[i - 1]:
                                        flag = False
                        if flag:
                                r_del_num += 1
                                print dels
                '''
                if len(var) == 2:
                        indel_len2_num += 1
                        if var[0] == var[1]:
                                repeated_indel_len2_num += 1
                                print var
                '''
        print "INS:"
        print ins_num, r_ins_num
        print ins_len2_num, r_ins_len2_num
        print "DEL:"
        print del_num, r_del_num
        print del_len2_num, r_del_len2_num
        print "------------"
