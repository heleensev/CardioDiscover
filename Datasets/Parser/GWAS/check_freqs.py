import re

def get_frqs(filename, frq_idx, sep):

    minor = 0
    major = 0

    with open(filename) as gwas:
        headline = gwas.readline()
        for line in gwas.readlines():
            frq = '%f' % float(line.split(sep)[frq_idx])
            #print(frq)
            if float(frq) < 0.5:
                minor += 1
            else:
                major += 1

    print(filename)
    print('minor: {}'.format(minor))
    print('major: {}'.format(major))
    print('_______________________')

def get_effect(filename, eff_idx, sep):

    negative = 0
    positive = 0

    with open(filename) as gwas:
        headline = gwas.readline()
        for line in gwas.readlines():
            frq = '%f' % float(line.split(sep)[eff_idx])
            # print(frq)
            if float(frq) < 0:
                negative += 1
            else:
                positive += 1

    print(filename)
    print('positive: {}'.format(positive))
    print('negative: {}'.format(negative))
    print('_______________________')

def get_info(filename, eff_idx, sep):

    negative = 0
    positive = 0
    bigger = 0

    with open(filename) as gwas:
        headline = gwas.readline()
        for line in gwas.readlines():
            frq = '%f' % float(line.split(sep)[eff_idx])
            # print(frq)
            if float(frq) < 0:
                negative += 1
            elif float(frq) == 1:
                bigger += 1
            else:
                positive += 1

    print(filename)
    print('positive: {}'.format(positive))
    print('negative: {}'.format(negative))
    print('bigger: {}'.format(bigger))
    print('_______________________')

def open_ref(filename):

    minor = 0
    major = 0

    pattern = re.compile('(?<=EUR_AF=)\d*.\d*(?=[;,])')

    with open(filename) as ref:
        ref_lines = ref.readlines()[255:]
        for line in ref_lines:

            info = line.split('\t')[7]
            match = re.search(pattern, info)
            if match:
                frq = float(match.group().split(',')[0])
                if frq > 0.5:
                    major += 1
                else:
                    minor += 1

        print('minor: {}'.format(minor))
        print('major: {}'.format(major))


# get_frqs('/home/sevvy/PycharmProjects/CardioDiscover/Datasets/Parser/GWAS/cad.add.160614.website.txt', 5, '\t')
# get_frqs('/home/sevvy/PycharmProjects/CardioDiscover/Datasets/Parser/GWAS/HTN_all_ethnic_big.csv', 7, ';')
# get_frqs('/home/sevvy/PycharmProjects/CardioDiscover/Datasets/Parser/GWAS/tag.cpd.table.txt', 6, '\t')
#
# get_effect('/home/sevvy/PycharmProjects/CardioDiscover/Datasets/Parser/GWAS/cad.add.160614.website.txt', 8, '\t')
# get_effect('/home/sevvy/PycharmProjects/CardioDiscover/Datasets/Parser/GWAS/HTN_all_ethnic_big.csv', 9, ';')
# get_effect('/home/sevvy/PycharmProjects/CardioDiscover/Datasets/Parser/GWAS/tag.cpd.table.txt', 8, '\t')

get_info('/home/sevvy/PycharmProjects/CardioDiscover/Datasets/Parser/GWAS/tag.cpd.table.txt', 7, '\t')

#open_ref('/home/sevvy/PycharmProjects/SNPUnqDb/Datasets/ALL0.txt')
