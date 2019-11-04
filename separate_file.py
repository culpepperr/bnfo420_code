# Program written by Rebecca Culpepper 4-27-19
""" Separates file based on Gene Type (Influenza Virus)
 First it looks for only one of each header (need to be removed by hand)
 Separates into two files based on Gene Type (HA and NA) and rechecks for doubles
 Then pulls 10000 random sequences from each file and separates chosen and not chosen
 into separate files (assumes approx equal split of file - based on 51/100 chance)
"""

# To edit file to make able to go through programs
import re


def write_data(fh, header, seq):
    """Functions to write output results to file"""
    fh.write(str(header))
    fh.write(str(seq))


#########################################
# Check file for only 1 of each NA and HA for each isolate
# If more found, find and remove them (use Notepad++)


def check_file(file_handle, option):
    """Checks fasta file for duplicate strains
    prints based on value in dictionary - currently set to 2, prints
    if anything other than 2 found
    option  - organism to put organism in as the third identifier
            - gene, to put gene type in as third identifier
            - anything else, no third identifier"""
    check_dict = {}
    # parse through file
    for line in file_handle:
        # if > is found assume it is header
        if line[0] == '>':
            # create header and find strain name and subtype
            header = line
            matches = re.findall("Strain Name:([AB]\/[\/A-Za-z 0-9()\\-_'.]+)", header)
            SubtypeMatch = re.findall("Subtype:([A-Za-z0-9]+)", header)
            # if none found display error
            if len(matches) <= 0:
                print("error 1")
            elif len(SubtypeMatch) <= 0:
                print("error 2")

            # if gene is option, then find gene symbol, if none found print error
            if option == 'gene':
                gene_matches = re.findall("Gene Symbol:[NAH]+", header)
                if len(gene_matches) <= 0:
                    print("error G3")
                find = matches[0] + "=" + SubtypeMatch[0] + "=" + gene_matches[0]
            # if organism is option, then find organism, if none found print error
            elif option == 'organism':
                organ = re.findall("Organism:([\/A-Za-z 0-9()\\-_'.]+)", header)
                if len(gene_matches) <= 0:
                    print("error O3")
                find = matches[0] + "=" + SubtypeMatch[0] + "=" + organ[0]
            # Otherwise look based on just strain and subtype
            else:
                find = matches[0] + "=" + SubtypeMatch[0]

            # Add to dictionary the new header determined
            check_dict[find] = check_dict.get(find, 0)+1

    # If more than 2 of each header exist display which ones
    for key, value in check_dict.items():
        if value >= 2:
            print(key + "\t" + str(value))


# Check for duplicate with different and same headers, use gene because NA and HA in same file
fh = open("All_ProteinFastaResults.fasta")
check_file(fh, 'gene')
fh.close()
print("Check for duplicates complete")

########################################################
# To separate the HA and NA sequences in two files from one big file

# Create/open files
fh = open("All_ProteinFastaResults.fasta")
fh_write_HA = open("HA_Sequences.fasta", "w")  # File to write NA to
fh_write_NA = open("NA_Sequences.fasta", "w")  # File to write HA to


# Initialize variables
seq = ''
""" Works by returning/finding header and sequence by looking until next
header is found then return what it found before that."""
# parse through file
for line in fh:
    # if > is found assume it is the header
    if line[0] == '>':
        # if seq is found/full and a match has been found to HA
        if len(seq) > 0 and matches[0] == "Gene Symbol:HA":
            write_data(fh_write_HA, header, seq)
            # Add to HA file
        # if seq is found/full and a match has been found to NA
        elif len(seq) > 0 and matches[0] == "Gene Symbol:NA":
            write_data(fh_write_NA, header, seq)
            # Add to NA file
        # reset variables
        header = line
        seq = ''
        # Determine which file it should go to
        matches = re.findall("Gene Symbol:[NAH]+", header)
    else:
        # if it is part of the sequence
        seq = seq + line

# For the last sequence in the file, because the add is at beginning of for loop, needed to add it to file
if matches[0] == "Gene Symbol:HA":
    write_data(fh_write_HA, header, seq)
    # Add to HA file
elif matches[0] == "Gene Symbol:NA":
    write_data(fh_write_NA, header, seq)
    # Add to NA file

# Close files
fh.close()
fh_write_NA.close()
fh_write_HA.close()
print("Separation of file complete")

#################################################################
# Double Check for strain copies using above function
# fh_HA = open("HA_Sequences.fasta", 'r')
# fh_NA = open("NA_Sequences.fasta", 'r')
#
# check_file(fh_HA, 'none')
# check_file(fh_NA, 'none')
# print("Double check for duplicates complete")


#########################################
# To pull random 10000 into separate files
# imports and open/create needed files
import random
fh_HA = open("HA_Sequences.fasta", 'r')
fh_NA = open("NA_Sequences.fasta", 'r')
fh_write_HA = open("Chosen_HA_Sequences.fasta", "w")
fh_write_NA = open("Chosen_NA_Sequences.fasta", "w")
fh_write_HA_2 = open("Not_HA_Sequences.fasta", "w")
fh_write_NA_2 = open("Not_NA_Sequences.fasta", "w")

# Initialize variables
strainList = []
counter = 0
seq = ''
# parse through file
for line in fh_HA:
    # if line has >, header
    if line[0] == '>':
        # Pull random number 1 to 100 (used to create better chances to get full 10000
        random_int = random.randint(1, 100)
        # if random number <=51 and counter isn't full and a sequence is found
        if random_int <= 51 and counter < 10000 and len(seq) > 0:
            # pull the header info needed to add to list
            matches = re.findall("Strain Name:([AB]\/[\/A-Za-z 0-9()\\-_'.]+)", header)
            SubtypeMatch = re.findall("Subtype:([A-Za-z0-9]+)", header)
            organ = re.findall("Organism:([\/A-Za-z 0-9()\\-_'.]+)", header)
            # write header and sequences in "Chosen" file
            write_data(fh_write_HA, header, seq)
            # Add shortened header to "Chosen" list for pulling from second file
            strainList.append(matches[0] + '=' + SubtypeMatch[0] + "=" + organ[0])
            counter += 1
            # Add to HA chosen file
        elif len(seq) > 0:
            # If not chosen (>51) then add to Not Chosen file
            write_data(fh_write_HA_2, header, seq)
        # reset variables
        header = line
        seq = ''
    else:
        # if it is part of the sequence
        seq = seq + line

# For the last entry in fasta file, if random num <=51 add to Chosen File
if random_int <= 51 and counter < 10000:
    write_data(fh_write_HA, header, seq)
    counter += 1
    # Add to HA file
# Otherwise add to not chosen file
else:
    write_data(fh_write_HA_2, header, seq)

#############
# To Pull from second file sequences that match headers from first file
#####
# Reset reused variables
seq, header = '', ''
chosen = False
counter2 = 0
# parse file
for line2 in fh_NA:
    # if header is found
    if line2[0] == '>':
        # if a sequence found and header on chosen list write to second Chosen file
        if len(seq) > 0 and chosen:
            write_data(fh_write_NA, header, seq)
            counter2 += 1
            chosen = False
            # Add to NA chosen file
        # otherwise add to second not chosen file
        elif len(seq) > 0 and not chosen:
            write_data(fh_write_NA_2, header, seq)
        # New header and sequence
        header = line2
        seq = ''
        # Find shortened header/identifier to compare to list of chosens
        matches = re.findall("Strain Name:([AB]\/[\/A-Za-z 0-9()\\-_'.]+)", header)
        SubtypeMatch = re.findall("Subtype:([A-Za-z0-9]+)", header)
        organ = re.findall("Organism:([\/A-Za-z 0-9()\\-_'.]+)", header)
        to_find = matches[0] + '=' + SubtypeMatch[0] + "=" + organ[0]
        # If identifier on Chosen list, make it true (to be added to file in above code)
        if strainList.__contains__(to_find):
            chosen = True
            # print('found')
    else:
        # if it is part of the sequence
        seq = seq + line2

# For last sequence in file, if not all have been found and chosen then add to chosen file
if counter2 < 10000 and chosen:
    write_data(fh_write_NA, header, seq)
    counter2 += 1
    # Add to NA file
# Otherwise add to other file
else:
    write_data(fh_write_NA_2, header, seq)

# Double check for repeats
# dict2 = {}
# for thing in strainList:
#     dict2[thing] = dict2.get(thing, 0) + 1
#
# for key, value in dict2.items():
#     if value >= 2 or value <= 0:
#         print(key + " " + str(value))

# Close open files
fh_HA.close()
fh_NA.close()
fh_write_NA.close()
fh_write_HA.close()
fh_write_HA_2.close()
fh_write_NA_2.close()

# Double check counts by printing
print(counter)
print(counter2)
print(strainList)
print(len(strainList))
print("Random 10000 separation complete")
