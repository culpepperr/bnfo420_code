# Group 1 Virus Project - Detecting Co-mutations
# Code Part 4 By Rebecca Culpepper
# Code can only handle about 50,000 sequences total before size becomes major issue (can't view)


import re
import os
# from Bio import SeqIO

# used later to fill in blanks, allow for different lengths of protein sequences
maxLen = 0

# File names central ###
tempFile = "temp.txt"
resultsFile = "chosen_output.txt"
resultsFile2 = "chosen_output.txt"
dictionaryFile = "chosen_output_sequence_dictionary_fill.txt"
filePath = "C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Chosen_modifiedSequence_3.fasta"

fh_temp = open(tempFile, "a+")
# lineCountDict = {}
line_count = 0
ceiling = 1000000


# Change error for file size of output, and what about sequences????
def write_data(fh, data, lengthCheck):
    """Functions to write output results to file"""
    # fhw = open(filename, "w")
    if lengthCheck:
        # lineCountDict[fh] = lineCountDict.get(fh, 0) + 1
        # line_count = lineCountDict.get(fh, 0)
        global line_count, ceiling
        line_count = line_count + 1
        if line_count > ceiling:
            ceiling = ceiling + 1000000
            global fh_results
            if fh == fh_results:
                fh_results.close()
                fh.close()
                global resultsFile, resultsFile2
                resultsFile = str(ceiling) + "-" + resultsFile2
                fh_results = open(resultsFile, "w")
                fh = fh_results
    if type(data) == list:
        for data_line in data:
            fh_results.write(str(data_line) + "\n")
    elif type(data) == dict:
        for key_a, value_b in data.items():
            fh.write(str(key_a) + ";" + str(value_b) + "\n")
    else:
        fh.write(str(data) + "\n")


#######################################
# Read sequence data from one file**###
#######################################
# open file into file handle
file_handle = open(filePath)

# parse through the file by line
seq = ''
header = ''
ij_count = 0
for line in file_handle:
    # if a line has > assume it is the title/header of organism and pull needed info, first pull header
    # fix to remove null problem
    if line[0] == '>' or line[0:5] == 'null>':
        ij_count = ij_count + 1.0
        if len(seq) > 0:
            write_data(fh_temp, header + ';' + seq, False)
        header = line.strip()
        # shorten header to make it easier to read.
        # to find header and label sequences, may need to be adjusted for specific data.
        #########################
        matches = re.findall("([(][AB]/[/A-Za-z 0-9()\\-_]*)", header)
        if len(matches) > 0:
            header = matches[0]
        else:
            NameMatch = re.findall("([AB]/[/A-Za-z 0-9()\\-_]+)", header)
            SubtypeMatch = re.findall("Subtype:([A-Za-z0-9]+)", header)
            # print header
            if len(SubtypeMatch) > 0 and len(NameMatch) > 0:
                header = '(' + NameMatch[0] + '(' + SubtypeMatch[0] + ')' + ')'
            elif len(NameMatch) > 0:
                header = '(' + NameMatch[0] + ')'
            else:
                # header = re.findall("(>gb:[/A-Za-z 0-9()\\-:]+)", header)[0]
                header = header
                # try:
                #     header = re.findall("(>gb:[/A-Za-z 0-9()\\-:]+)", header)[0]
                # except:
                #     header = header

        seq = ''
        # go to next line to find sequence for given header
        # then add that header and sequence to the dictionary and list
    else:
        # if it is part of the sequence
        seq = seq + line.strip()

        # Check to find length of longest sequence, used to fill in so all are same length
        if len(seq) > maxLen:
            maxLen = len(seq)

write_data(fh_temp, header + ';' + seq, False)
fh_temp.seek(0)
fh_dictionary = open(dictionaryFile, 'w')

###########################################
###########################################
# Loop through and if sequence is shorter than max, add - until length is the same.
# Move sequences dictionary from temp file to dictionary file.
for line in fh_temp:
    coord = line.find(';')
    sqnc = line[coord+1:len(line)].strip()
    while len(sqnc) < maxLen:
        sqnc = sqnc + '-'
    # fhs.seek(1)
    write_data(fh_dictionary, line[:coord] + ';' + sqnc, False)

fh_temp.close()
# Delete Temp file here
os.remove(tempFile)
print("Temp File Removed!")
fh_dictionary.close()

print(maxLen)


def pull_data_dictionary(i_x, j_y, i_m_dict, j_m_dict, pair_dict_m):
    """Use file as dictionary and instead of loading i and j into string, just count-add to dictionary directly"""
    fh_dictionary = open(dictionaryFile, 'r')
    for line_in in fh_dictionary:
        organism_a, sequence_a = line_in.split(';')
        # print organism_a, sequence_a

        i_letter = sequence_a[i_x]
        j_letter = sequence_a[j_y]
        pair_dict_m[i_letter + j_letter] = pair_dict_m.get(i_letter + j_letter, 0.0) + 1.0
        i_m_dict[i_letter] = i_m_dict.get(i_letter, 0.0) + 1.0
        j_m_dict[j_letter] = j_m_dict.get(j_letter, 0.0) + 1.0

    fh_dictionary.seek(0)
    fh_dictionary.close()
    organism_a, sequence_a = '',''

    return i_m_dict, j_m_dict, pair_dict_m


def check_data_dictionary(pair_match, second_freq):
    """Use to pull data to check for pair."""
    organism_list = []
    organism_count, organism_total, second_count = 0, 0, 0
    fh_dictionary = open(dictionaryFile, 'r')
    for line_in_c in fh_dictionary:
        organism_b, sequence_b = line_in_c.split(';')
        organism_total += 1
        if sequence_b[i] == pair_match[0] and sequence_b[j] == pair_match[1] and pair_match != '--':
            # Ignore -- matches, they technically don't exist
            # write_data(fh_results, (organism_b, i, j, pair_match), True)
            organism_list.append(organism_b)
            organism_count += 1
        elif sequence_b[i] == second_freq[1][0] and sequence_b[j] == second_freq[1][1] and pair_match != '--':
            second_count += 1

    write_data(fh_results, "****  " + str(i) + pair_match[0] + ",\t" + str(j) + pair_match[1], True)
    write_data(fh_results, "\t\t" + str(organism_count) + "/" + str(organism_total) + " Sequences have it", False)
    write_data(fh_results, "\t\t" + "Second Frequency: " + str(second_freq[0]) + ";\t" + str(i) + second_freq[1][0]
               + "\t" + str(j) + second_freq[1][1], False)

    for entry in organism_list:
        write_data(fh_results, "\t\t\t\t" + entry, True)

    fh_dictionary.seek(0)
    fh_dictionary.close()
    organism_b, sequence_b = '', ''
    del organism_list[:]


# Open file to store results in
fh_results = open(resultsFile, "w")
# Loop through columns of the sequences, i and j, and compare each column to the others
for i in range(0, len(seq)-1):
    # list to store the i column
    # loop through sequences and add protein to column list

    # Repeat the same process for j, find column from 1 after i to end
    for j in range(i+1, len(seq)):
        # add proteins from column to column list counts
        pairDict = {}
        # Dictionary to hold count of single proteins in i and j column respectively
        i_dict = {}
        j_dict = {}
        # total number of pairs, length of the column
        ij_total = 0.0
        # count variables in each column and pairs
        i_dict, j_dict, pairDict = pull_data_dictionary(i, j, i_dict, j_dict, pairDict)

        ##################################

        # Checkpoint to check dictionary contents ###
        # print i_dict
        # print j_dict

        ###########################
        # Data check prints #######
        # find pair frequency:
        # find frequency of seeing two amino acids together in i and j position of each sequence
        # for key, item in pairDict.items():
        #     # print "Frequency: " + key + " - " + str(item/ij_total)
        #     write_data('output.txt', "Frequency: " + key + " - " + str(item/ij_total))
        # find individual frequency:
        # find frequency of seeing an amino acid is either i or j position of each sequence
        # for key, item in i_dict.items():
        #     # print "Frequency of i: " + key + " - " + str(item/len(i_list))
        #     write_data('output.txt', "Frequency of i: " + key + " - " + str(item/len(i_list)))
        # for key, item in j_dict.items():
        #     # print "Frequency of j: " + key + " - " + str(item/len(j_list))
        #     write_data('output.txt', "Frequency of j: " + key + " - " + str(item/len(j_list)))
        ####

        # find co-occurrence of each:
        # find co-occurrence through given equation: f(x(i),y(j))**2 / f(x(i))*f(y(j))
        # print"Co-occurrence Frequency: "
        # ####write_data('output.txt', "Co-occurrence Frequency: ")####
        # If the frequency of xy pair is less than 5% (.05) then ignore it
        # list to store and retrieve found co-occurrence frequencies pairs
        freqList = []
        secondFreq = (-1, "XX")
        for key, item in pairDict.items():
            if item/ij_count > 0.05:
                x = i_dict.get(key[0], 0.0)
                y = j_dict.get(key[1], 0.0)
                Freq = ((item/ij_count)**2.0) / ((x/ij_count)*(y/ij_count))
                # print(key + " - " + str(Freq))
                # ####write_data('output.txt', key + " - " + str(Freq))
                if secondFreq[0] < Freq < 1.0:
                    secondFreq = (Freq, key)
                if Freq == 1.0:
                    freqList.append(key)

        # using the i, j coordinates and pairDict to create tuples of the network connections
        for string in freqList:
            check_data_dictionary(string, secondFreq)

        # separate results into sections
        # ####write_data('output.txt', "###############################################")
        print("Part Done " + str(i) + " - " + str(j))

# write_data("output.txt", coordinateList)
fh_results.close()
print("Done")

# How to delete temporary files that are no longer needed
# Only open file as needed? Have close be part of the method?
# remove ticks on the side of code
# go through file edit one line at a time and delete and repaste line to remove temp file??
# Protein sequences
# HA and NA
# Human Influenza A
