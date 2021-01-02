import csv

import operator
import random
import tqdm
import copy
from codons import all_codons

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def codon_change(from_codon, to_codon, lst):
    """
    Efficient in place list element replacement
    """
    idx = -1
    for _ in range(lst.count(from_codon)):
        idx = lst.index(from_codon, idx+1)
        lst[idx] = to_codon

    return lst

def read_csv(filename):
    records = []
    with open(filename, 'rt') as fp:
        reader = csv.reader(fp, delimiter=',')
        for ii, row in enumerate(reader):
            if ii > 0:
                records.append(row)

    return records



def compare(virus_mod, vaccine):
    """
    Compares a given virus modification to the vaccine
    """
    matches = 0
    for element in zip(virus_mod, vaccine):
        vir = element[0]
        vac = element[1]

        our = vir
        if vac == our:
            matches +=1

    return matches / len(vaccine) * 100

virvac = read_csv("side-by-side.csv")
virus_codons = [x[1] for x in virvac]
vaccine_codons = [x[2] for x in virvac]

# test CCTCCT --> AAAGGT proline substitution - only got to 79.27% - ever so slightly worse
#vaccine_codons = list(chunks("".join(vaccine_codons).replace("CCTCCT", "AAAGTT"), 3))
print(compare(virus_codons, vaccine_codons))

best_match = 0
best_chng = None
current_virus = virus_codons
mapp = {}
try:
    for i in range(0, 1000):
        for c1 in tqdm.tqdm(all_codons, leave=False):
            for c2 in all_codons:
                matches = 0
                for i in range(len(virus_codons)):
                    # if there's a match
                    if current_virus[i] == c1:
                        if c2 == vaccine_codons[i]:
                            matches += 1
                    else:
                        if current_virus[i] == vaccine_codons[i]:
                            matches += 1
                if matches > best_match:
                    best_match = matches
                    best_chng = (c1, c2)
        current_virus = codon_change(best_chng[0], best_chng[1], current_virus)
        mapp[best_chng[0]] = best_chng[1]
        print(best_match/len(virus_codons) * 100, best_chng)
        best_chng = 0
        best_match = 0
except KeyboardInterrupt:
    pass
print(mapp)
print(current_virus)
