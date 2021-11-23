import os

files = os.listdir("seq")
for i in files:
    file_h = open(f"seq/{i}")
    file = file_h.read().split(">")
    file_h.close()
    file = "".join([f">{i.split('.')[0]}_" + i1 for i1 in file[1:31]])
    newfile = open("temp_files/all_seq.fasta", "a")
    newfile.write(file)
    newfile.close()


