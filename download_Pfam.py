import random
from urllib import request
from tqdm import tqdm

correct = 0
while correct < 100:
    id = random.randint(10000, 99999)
    url = f"http://pfam.xfam.org/family/PF{id}/alignment/seed/format?format=fasta&alnType=seed&order=t&case=u&gaps=none&download=0"
    try:
        request.urlretrieve(url, f"seq/PF{id}.fasta")
        correct += 1
    except:
        continue
    print(correct)


