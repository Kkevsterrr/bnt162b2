import csv
import itertools

def read_csv(filename):
    records = []
    with open(filename, 'rt') as fp:
        reader = csv.reader(fp, delimiter=',')
        for ii, row in enumerate(reader):
            if ii > 0:
                records.append(row)

    return records


with open("codon-table-grouped.csv", "r") as fd:
    lines = fd.readlines()

all_codons = []

for line in lines[1:]:
    all_codons.append(line.split(",")[1].strip())

virvac = read_csv("side-by-side.csv")
virus_codons = [x[1] for x in virvac]
vaccine_codons = [x[2] for x in virvac]

# Only include codons that are in one or the other; this is a slight optimization to remove
# 3 unused codons ('TAG', 'CCG', 'CGA')
all_codons = [c for c in all_codons if c in virus_codons or c in vaccine_codons]
all_codon_pairs = list(itertools.combinations(all_codons, 2))
