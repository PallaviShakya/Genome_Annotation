from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from sys import argv

for record in SeqIO.parse(argv[1], 'fasta'):

  rid = record.id

  sequence_frame1 = record.seq.translate()

  print(f">{rid}\n{str(sequence_frame1)}")

