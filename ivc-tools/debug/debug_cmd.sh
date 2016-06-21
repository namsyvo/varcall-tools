go run /home/nsvo/workspace/goprojects/src/github.com/namsyvo/IVC/main/ivc.go -R /data/nsvo/test_data/GRCh37_chr1/refs/GRCh37_chr1.fasta -V /data/nsvo/test_data/GRCh37_chr1/refs/TRIMMED.ALL.chr1.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.vcf -I /data/nsvo/test_data/GRCh37_chr1/indexes/NA12878_trim_index/ -1 /data/nsvo/test_data/GRCh37_chr1/reads/real_reads/NA12878/aln_pos_$1_1.fastq -2 /data/nsvo/test_data/GRCh37_chr1/reads/real_reads/NA12878/aln_pos_$1_2.fastq -O /data/nsvo/test_data/GRCh37_chr1/results/real_reads/NA12878/ivc_0.8.1-2_exome/aln_pos_$1.ivc.vcf -debug=true 2> /data/nsvo/test_data/GRCh37_chr1/results/real_reads/NA12878/ivc_0.8.1-2_exome/aln_pos_$1.ivc.vcf.log 1> /data/nsvo/test_data/GRCh37_chr1/results/real_reads/NA12878/ivc_0.8.1-2_exome/aln_pos_$1.ivc.vcf.debug