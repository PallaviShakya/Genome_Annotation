# Genome_Annotation

BRAKER3 was used for genome annotation. Docker was used to run Braker 3 as per the prtocols: https://hub.docker.com/r/teambraker/braker3 

To mount the data into docker: 

```
docker run -d -p 1000:10 -v $(pwd):/home/jovyan --name braker3 teambraker/braker3:latest 
docker exec -it braker3 bash
```

1. First round of BRAKER3 used RNAseq reads from different life stages of _M. hapla_

```
nice -16 braker.pl --genome=M_hapla_assembly_v1.masked.fasta --species=M_hapla_VW9 --bam=A411.bam,A414.bam,A422.bam,A431.bam,A433.bam,B411.bam,B414.bam,B422.bam,B425.bam,B433.bam,A412.bam,A415.bam,A424.bam,A432.1.bam,A434.bam,B412.bam,B415.bam,B423.bam,B431.bam,B434.bam,A413.bam,A421.bam,A425.bam,A432.2.bam,A435.bam,B413.bam,B421.bam,B424.bam,B432.bam,B435.bam 
```

2. Second round of BRAKER3 used RNAseq reads from WUR, Guo 2017 data and protein database: 

```
nice -16 braker.pl --genome=../purged_hifiasm_assembly_v1.fasta --species=M_hapla_VW9_short_protein --threads=20 --prot_seq=../proteins.fa --bam=04_GC14.bam,A415.bam,A432.2.bam,B414.bam,B431.bam,EA10.bam,EA1.bam,EA26.bam,EA5.bam,FB15.bam,FB22.bam,FB30.bam,FB3.bam,GC15.bam,GC23.bam,GC31.bam,GC46.bam,GC53.bam,GC8.bam,09_GC42.bam,A421.bam,A433.bam,B415.bam,B432.bam,EA11.bam,EA20.bam,EA27.bam,EA6.bam,FB16.bam,FB23.bam,FB31.bam,FB4.bam,GC16.bam,GC24_GC44.bam,GC32.bam,GC47.bam,GC54A.bam,GC9.bam,12_GC14.bam,A422.bam,A434.bam,B421.bam,B433.bam,EA12.bam,EA21.bam,EA28.bam,EA8.bam,FB17.bam,FB25.bam,FB32.bam,FB6.bam,GC18.bam,GC25.bam,GC35.bam,GC48.bam,GC54C.bam,A411.bam,A424.bam,A435.bam,B422.bam,B434.bam,EA14.bam,EA22.bam,EA30.bam,FB09.bam,FB18.bam,FB26.bam,FB33.bam,FB8.bam,GC19.bam,GC26.bam,GC36.bam,GC4.bam,GC55.bam,A412.bam,A425.bam,B411.bam,B423.bam,B435.bam,EA16.bam,EA23.bam,EA31.bam,FB10.bam,FB19.bam,FB27.bam,FB36.bam,GC01.bam,GC20.bam,GC27_GC29_GC41.bam,GC37.bam,GC50.bam,GC5.bam,A413.bam,A431.bam,B412.bam,B424.bam,EA02.bam,EA17.bam,EA24_GC10.bam,EA32.bam,FB12.bam,FB20.bam,FB28.bam,FB37.bam,GC03.bam,GC21_GC43_GC49.bam,GC28.bam,GC39.bam,GC51.bam,GC6.bam,A414.bam,A432.1.bam,B413.bam,B425.bam,EA09.bam,EA18.bam,EA25.bam,EA3.bam,FB14.bam,FB21.bam,FB2.bam,FB38.bam,GC12_GC42.bam,GC22.bam,GC30.bam,GC45.bam,GC52.bam,GC7.bam –workingdir=/data/braker_short_long_protein/ 
```
3. Third round of BRAKER3 used the long-reads/isoseq reads. This was done using the long read branch of BRAKER3: https://github.com/Gaius-Augustus/BRAKER/blob/master/docs/long_reads/long_read_protocol.md 

```
mkdir long_read_protocol 
cd long_read_protocol 
nice -16 pbmm2 align --preset ISOSEQ -J 40 --sort ../polished_clustered_hapla.hq.bam ../purged_hifiasm_assembly_v1.fasta Mhap_VW9_PacBio_HiFi_longreads_RNA.bam 
sort -k 3,3 -k 4,4n Mhap_VW9_PacBio_HiFi_longreads_RNA.sam > Mhap_VW9_PacBio_HiFi_longreads_RNA.s.sam 
isoseq3 collapse --do-not-collapse-extra-5exons --max-5p-diff 5 --max-3p-diff 5 Mhap_VW9_PacBio_HiFi_longreads_RNA.bam Mhap_VW9_PacBio_HiFi_longreads_RNA.gff 
```
This script was used:  https://github.com/Gaius-Augustus/Augustus/blob/master/scripts/stringtie2fa.py :

```
../stringtie2fa.py -g ../purged_hifiasm_assembly_v1.fasta -f cupcake.collapsed.gff -o cupcake.fa 

```
Check the amount of sequences in cupcake.fa.mrna: 

```
cat cupcake.fa.mrna | grep ">" | wc -l 
```

Get Genemark S-T

```
tar -zxvf gmst_linux_64.tar.gz from Genemark S-T 
../gmst.pl --strand direct cupcake.fa.mrna --output gmst.out --format GFF 

```

This script was used  https://github.com/Gaius-Augustus/BRAKER/blob/long_reads/scripts/gmst2globalCoords.py : 

```
../gmst2globalCoords.py -t cupcake.collapsed.gff -p gmst.out -o gmst.global.gtf -g ../purged_hifiasm_assembly_v1.fasta 
```
4. TSEBRA (https://github.com/Gaius-Augustus/TSEBRA) was used to combine all results: 

```
python tsebra.py -g braker.gtf,braker2.gtf -l gmst.global.gtf -e hintsfile.gff,hintsfile2.gff -c /home/pallavishakya/git_repositories/BRAKER/TSEBRA/config/default.cfg -o 4_Mhapla_annotation.gtf -kl -k braker.gtf  
```
