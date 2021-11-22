import random
from urllib import request
from tqdm import tqdm
import os

correct = len(os.listdir("seq"))
while correct < 100:
    id = f'{random.randint(1, 99999):05}'
    url = f"http://pfam.xfam.org/family/PF{id}/alignment/seed/format?format=fasta&alnType=seed&order=t&case=u&gaps=none&download=0"
    try:
        data = request.urlopen(url).read().decode("utf-8")
        if data:
            if data.count(">") > 10:
                newfile = open(f"seq/PF{id}.fasta", "w")
                newfile.write(data)
                newfile.close()
                correct += 1
    except:
        continue
    print(correct)


