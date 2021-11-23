from sklearn import metrics
from tqdm import tqdm
from matplotlib import pyplot as plt

def get_true_class():
    file_h = open("temp_files/all_seq.fasta")
    file = file_h.readlines()
    file_h.close()
    data = [i.lstrip(">").rstrip().split("/")[0].split("_")[:3] for i in file if ">" in i]
    data = [[i[0], i[1]] for i in data]
    indexing = [i[1] for i in data]
    result = {}
    for i in data:
        if i[0] in result:
            result[i[0]].append(i[1])
        else:
            result[i[0]] = [i[1]]
    return result, indexing


def get_cd_hit_class():
    file_h = open("temp_files/cd-hit_clustering.clstr")
    file = file_h.read()
    file_h.close()

    data = file.split(">Cluster")[1:]
    result = {}
    for i in data:
        name = i.split("\n")[0]
        seq = i.split("\n")[1:-1]
        result[name] = [i.split("_")[1] for i in seq]

    return result


def get_CLANS_class():
    file_h = open("temp_files/CLANS_clusters")
    file = file_h.read()
    file_h.close()

    seq_data = file.split("<seq>")[1].split("</seq>")[0].split("\n")
    seq_data = [i.split("_")[1] for i in seq_data if ">" in i]

    groups_data = file.split("<seqgroups>")[1].split("</seqgroups>")[0].split("name")[1:]
    groups_data = [[i.split("\n")[0], i.split("\n")[5]] for i in groups_data]
    groups_data = [i for i in groups_data if "linkage" in i[0]]
    groups_data = [[i[0].split("_")[1], i[1].split("=")[1].split(";")[:-1]] for i in groups_data]

    result = {}
    for i in groups_data:
        result[i[0]] = [seq_data[int(i1)] for i1 in i[1]]

    return result


def merge_families_into_clans(data):
    file_h = open("temp_files/Pfam-A.clans.tsv")
    file = file_h.readlines()
    file_h.close()
    data_clans = [i.split("	")[:2] for i in file]

    result = {}
    for i in data:
        for i1 in data_clans:
            if i == i1[0]:
                if i1[1]:
                    if i1[1] in result:
                        result[i1[1]].extend(data[i])
                    else:
                        result[i1[1]] = data[i]
                else:
                    result[i] = data[i]

    return result


def group_making(dictionary, indexing):
    groups = []
    for i in dictionary:
        group = [0 for i in range(len(indexing))]
        for i1 in dictionary[i]:
            group[indexing.index(i1)] = 1
        groups.append(group)
    return groups


def compare_groups(group1, group2):
    result = []
    for i in tqdm(group1):
        test = 0
        for i1 in group2:
            temp = metrics.jaccard_score(i, i1)
            if temp > test:
                test = temp
        print(test)
        result.append(test)

    return result


true_lab, indexing = get_true_class()
true_groups = group_making(true_lab, indexing)

cd_hit_lab = get_cd_hit_class()
cd_hit_groups = group_making(cd_hit_lab, indexing)

CLANS_lab = get_CLANS_class()
CLANS_groups = group_making(CLANS_lab, indexing)

pfam_clans_lab = merge_families_into_clans(true_lab)
pfam_clans_groups = group_making(pfam_clans_lab, indexing)
print(len(pfam_clans_groups))

hist_data = compare_groups(pfam_clans_groups, CLANS_groups)

plt.figure()
plt.hist(hist_data)
plt.show()
