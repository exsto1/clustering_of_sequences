import os

os.system(f"cd-hit -i temp_files/all_seq.fasta -o temp_files/cd-hit_clustering -c 0.4 -n 2")
# os.system(f"sumaclust -h temp_files/all_seq.fasta")

# os.system("mmseqs easy-search temp_files/all_seq.fasta temp_files/all_seq.fasta temp_files/all_seq.fasta temp_files/mmseqs_clustering")