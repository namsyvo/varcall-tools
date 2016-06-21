go run /home/nsvo/workspace/goprojects/src/github.com/namsyvo/IVC/main/ivc.go -R /data/nsvo/test_data/GRCh37_chr1/refs/GRCh37_chr1.fasta -V /data/nsvo/test_data/GRCh37_chr1/refs/ExAC.r0.3.1.sites.vep.vcf_chr1 -I /data/nsvo/test_data/GRCh37_chr1/indexes/ivc_0.8.1-2_exome -1 /data/nsvo/test_data/GRCh37_chr1/reads/real_reads/NA12878/aln_pos_$1_1.fastq -2 /data/nsvo/test_data/GRCh37_chr1/reads/real_reads/NA12878/aln_pos_$1_2.fastq -O /data/nsvo/test_data/GRCh37_chr1/results/real_reads/NA12878/ivc_0.8.1-2_exome/aln_pos_$1.ivc.vcf -debug=true 2> /data/nsvo/test_data/GRCh37_chr1/results/real_reads/NA12878/ivc_0.8.1-2_exome/aln_pos_$1.ivc.vcf.log 1> /data/nsvo/test_data/GRCh37_chr1/results/real_reads/NA12878/ivc_0.8.1-2_exome/aln_pos_$1.ivc.vcf.debug