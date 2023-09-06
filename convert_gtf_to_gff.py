from sys import argv


cds_count = 1

with open(argv[1]) as gtf_file:
    for line in gtf_file:
        line = line.strip().split("\t")
        if line[2] == 'gene':
            line[8] = "ID=" +line[8]
        elif line[2] == 'transcript':
            cds_count = 1
            line[2] = "mRNA"
            transcript_p = line[8]
            parent_p = transcript_p.split('.')[0]
            transcript_p = f"ID={transcript_p}"
            gene_id_p = f"Parent={parent_p}"
            line[8] = ";".join([transcript_p, gene_id_p])

        elif line[2] == 'exon':
            parent, gene_id_p = line[8].split('; ')
            parent = parent.replace("transcript_id \"", "").replace('"', "")
            id_p = f"ID={parent}.exon{cds_count}"
            parent = f"Parent={parent}"
            line[8] = ";".join([id_p, parent])
            cds_count += 1

        elif line[2] == 'CDS':
            parent, gene_id_p = line[8].split('; ')
            parent = parent.replace("transcript_id \"", "").replace('"', "")
            id_p = f"ID={parent}.CDS{cds_count}"
            parent = f"Parent={parent}"
            line[8] = ";".join([id_p, parent])
            cds_count += 1

        elif line[2] == 'start_codon':
            parent, gene_id_p = line[8].split('; ')
            parent = parent.replace("transcript_id \"", "").replace('"', "")
            id_p = f"ID={parent}.start{cds_count}"
            parent = f"Parent={parent}"
            line[8] = ";".join([id_p, parent])
            cds_count += 1

        elif line[2] == 'stop_codon':
            parent, gene_id_p = line[8].split('; ')
            parent = parent.replace("transcript_id \"", "").replace('"', "")
            id_p = f"ID={parent}.stop{cds_count}"
            parent = f"Parent={parent}"
            line[8] = ";".join([id_p, parent])
            cds_count += 1

        elif line[2] == "3'-UTR":
            parent, gene_id_p = line[8].split('; ')
            parent = parent.replace("transcript_id \"", "").replace('"', "")
            id_p = f"ID={parent}.3UTR{cds_count}"
            parent = f"Parent={parent}"
            line[8] = ";".join([id_p, parent])
            cds_count += 1

        elif line[2] == "5'-UTR":
            parent, gene_id_p = line[8].split('; ')
            parent = parent.replace("transcript_id \"", "").replace('"', "")
            id_p = f"ID={parent}.5UTR{cds_count}"
            parent = f"Parent={parent}"
            line[8] = ";".join([id_p, parent])
            cds_count += 1

        else:
            continue

        print("\t".join(line))

