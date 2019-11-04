# Program written by Rebecca Culpepper 4-28-19
# File takes multiple sequence files - hard coded
# It finds the longest sequence in each file and adds - to adjust length so they are all the same size
# Then it checks the lengths of hard programed sequence to note fusion index and fuses two
# sequences with the same organism, strain name and subtype into one sequence (Built for HA and NA influenza virus)

import re

# Names of the files to be opened/created in next section
C_HA = "Result_Chosen HA File.fasta"
LC_HA = "LResult_Chosen HA File.fasta"
#
C_NA = "Result_Chosen NA File.fasta"
LC_NA = "LResult_Chosen NA File.fasta"
#
NC_HA = "Result_Not HA Sequences.fasta"
L_NC_HA = "LResult_Not HA Sequences.fasta"
#
NC_NA = "Result_Not NA Sequences.fasta"
L_NC_NA = "LResult_Not NA Sequences.fasta"
#
# ##################################
# Section 1: Length Check


def write_data(fh, header, data):
    """Function to write output results to file
    assumes no strip used on file except final sequence"""
    # fhw = open(filename, "w")
    fh.write(str(header))
    fh.write(str(data) + "\n")


def check_len(file_handle, fh_write):
    """Function loops through first (input) file, finds max length of sequences
    and adjust other sequences by adding '-' until they are the same length as max"""
    # parse through the file by line
    max_len = 0
    seq = ''
    # header = ''
    # Section 1.2 - Parse through file sequences and find max length
    for line in file_handle:
        # if a line has > assume it is the title/header of organism
        if line[0] == '>':
            # Determine length of each sequence
            # print(len(seq.strip()))
            # header = line
            seq = ''
        else:
            # if it is part of the sequence
            seq = seq + line
            # Check to find length of longest sequence, used to fill in so all are same length
            if len(seq.strip()) > max_len:
                max_len = len(seq.strip())
    file_handle.seek(0)
    # The last entry will be at top without this

    # With this Section 1.4 will be needed or it will miss the last entry
    seq = ''
    header = ''
    # Determine max length for section
    print(max_len)

    # Section 1.3 - Parse through file again and add - to end if less than max length, write to new file
    for line in file_handle:
        # if a line has > assume it is the title/header of organism
        if line[0] == '>':
            # if sequences is full, add - if needed and write header and seq to new file
            if len(seq) > 0:
                seq = seq.strip()
                while len(seq) < max_len:
                    seq = seq + '-'
                write_data(fh_write, header, seq)
            # reset header to next header and seq
            header = line
            seq = ''
        else:
            # if it is part of the sequence
            seq = seq + line

    # Section 1.4, to print the last entry in the files
    seq = seq.strip()
    while len(seq) < max_len:
        seq = seq + '-'
    write_data(fh_write, header, seq)

# The .strip() makes a len difference of 1.
# ********************************************************************************************************************
# # open files and call function for each set of data:
# # ChosenHA, ChosenNA, NotChosenHA, NotChosenNA
# C_HA_fh = open(C_HA, "r")
# LC_HA_fh = open(LC_HA, "w")
# check_len(C_HA_fh, LC_HA_fh)
# # All Length 605, no changes known (includes newlines characers '\n')
# #
# C_NA_fh = open(C_NA, "r")
# LC_NA_fh = open(LC_NA, "w")
# check_len(C_NA_fh, LC_NA_fh)
# # All Length 502, - added to end, unknown reason (includes newlines characers '\n')
#
# NC_HA_fh = open(NC_HA, "r")
# L_NC_HA_fh = open(L_NC_HA, "w")
# check_len(NC_HA_fh, L_NC_HA_fh)
# # All Length 605, no changes known (includes newlines characers '\n')
#
# NC_NA_fh = open(NC_NA, "r")
# L_NC_NA_fh = open(L_NC_NA, "w")
# check_len(NC_NA_fh, L_NC_NA_fh)
# # All Length 507, no changes known (includes newlines characers '\n')
# # if there is a number difference between the HA and NA run code below "Adjust for length"
#
# # Close all open files
# C_HA_fh.close()
# LC_HA_fh.close()
# C_NA_fh.close()
# LC_NA_fh.close()
# NC_HA_fh.close()
# L_NC_HA_fh.close()
# NC_NA_fh.close()
# L_NC_NA_fh.close()
# print("Length Check complete")

##################################
# Section 1.5: Remove error from alignment
# Why - at beginning and end of sequences???


def find_dashes(file_name, title):
    file_name = open(file_name)
    header, seq = '', ''
    double_count, zero_count, end_count, total_count, none_count = 0, 0, 0, 0, 0
    double, zero, end = [], [], []
    for line in file_name:
        if line[0] == '>':
            total_count += 1
            if len(header) > 0 and len(seq) > 0:
                if seq[0] == '-' and seq[len(seq)-1] == '-':
                    double_count += 1
                else:
                    double.append((header, len(seq)))
                if seq[0] == '-':
                    zero_count += 1
                else:
                    zero.append((header, len(seq)))
                if seq[len(seq)-1] == '-':
                    end_count += 1
                else:
                    end.append((header, len(seq)))
                if seq[0] != '-' and seq[len(seq) - 1] != '-':
                    none_count += 1
            header = line
            seq = ''
        else:
            seq = seq + line.strip()

    if len(header) > 0 and len(seq) > 0:
        if seq[0] == '-' and seq[len(seq) - 1] == '-':
            double_count += 1
        if seq[0] == '-':
            zero_count += 1
        if seq[len(seq) - 1] == '-':
            end_count += 1
        else:
            print(header)
            print(len(seq))
        if seq[0] != '-' and seq[len(seq) - 1] != '-':
            none_count += 1

    print(title)
    # print("Double Count: " + str(double_count))
    # for entry in double: print(entry)
    print("Zero Count: " + str(zero_count))
    # for entry in zero: print(entry)
    # print("End Count: " + str(end_count))
    # for entry in end: print(entry)
    print("None Count: " + str(none_count))
    print("Total Count: " + str(total_count))
    print("\n")
    file_name.close()

# ******************************************************************************************************
# find_dashes("Chosen_Fuse.fasta", "Chosen Fuse File")
# find_dashes("Not_Chosen_Fuse.fasta", "Not Chosen Fuse File")

# Trim off beginning 6 -----
# fh = open("Result_Not NA Sequences.fasta")
# header, seq = '', ''
# double_count, zero_count, end_count, total_count, none_count = 0, 0, 0, 0, 0
# double, zero, end = [], [], []
# for line in fh:
#     if line[0] == '>':
#         total_count += 1
#         if len(header) > 0 and len(seq) > 0:
#             if seq[0:6] == '------' and seq[len(seq)-1] == '-':
#                 double_count += 1
#             else:
#                 double.append((header, len(seq)))
#             if seq[0:6] == '------':
#                 zero_count += 1
#             else:
#                 zero.append((header, len(seq)))
#             if seq[len(seq)-1] == '-':
#                 end_count += 1
#             else:
#                 end.append((header, len(seq)))
#             if seq[0:6] != '------' and seq[len(seq) - 1] != '-':
#                 none_count += 1
#         header = line
#         seq = ''
#     else:
#         seq = seq + line.strip()
#
# if len(header) > 0 and len(seq) > 0:
#     if seq[0:6] == '------' and seq[len(seq) - 1] == '-':
#         double_count += 1
#     if seq[0:6] == '------':
#         zero_count += 1
#     if seq[len(seq) - 1] == '-':
#         end_count += 1
#     else:
#         print(header)
#         print(len(seq))
#     if seq[0:6] != '------' and seq[len(seq) - 1] != '-':
#         none_count += 1
#
# print("Not_NA_Sequences_File")
# print("Zero Count: " + str(zero_count))
# for entry in zero: print(entry)
# print("None Count: " + str(none_count))
# print("Total Count: " + str(total_count))
# print("\n")
#
# fh.close()
########
# Section 1.5.2 Remove extra -
#   Remove first 6 letters from each sequence in Not NA Sequences


def not_na_remove():
    remove_fh = open(L_NC_NA)
    new_fh = open("ALResult_Not NA Sequences.fasta", "w")
    header, seq = '', ''
    for line in remove_fh:
        if line[0] == '>':
            if len(header) > 0 and len(seq) > 0:
                seq = seq[6:]
                write_data(new_fh, header, seq.strip())
            header = line
            seq = ''
        else:
            seq = seq + line

    if len(header) > 0 and len(seq) > 0:
        seq = seq[6:]
        write_data(new_fh, header, seq.strip())

    new_fh.close()
    remove_fh.close()

# ********************************************************************************************************
# not_na_remove()
# # Confirm zero count (first letter) not a -
# find_dashes("ALResult_Not NA Sequences.fasta", "Not NA Sequences")
# # Change file name for future use in code
# L_NC_NA = "ALResult_Not NA Sequences.fasta"

#   Move -'s at beginning of files behind M - Both HA files
# LC_HA
# L_NC_HA


def change_align_ha(remove, new):
    remove_fh = open(remove)
    new_fh = open(new, "w")
    header, seq = '', ''
    for line in remove_fh:
        if line[0] == '>':
            if len(header) > 0 and len(seq) > 0:
                for num in range(1, 5):
                    if seq[num] == 'M':
                        index = num
                        seq = seq[index] + seq[0:index] + seq[index + 1:]
                        break
                write_data(new_fh, header, seq.strip())
            header = line
            seq = ''
        else:
            seq = seq + line

    if len(header) > 0 and len(seq) > 0:
        for num in range(1, 5):
            if seq[num] == 'M':
                index = num
                break
        seq = seq[index] + seq[0:index] + seq[index + 1:]
        write_data(new_fh, header, seq.strip())

    new_fh.close()
    remove_fh.close()


# change_align_ha(LC_HA, "ALResult_Chosen HA File.fasta")
# # Confirm zero count is none
# find_dashes("ALResult_Chosen HA File.fasta", "Chosen HA Sequences")
# change_align_ha(L_NC_HA, "ALResult_Not HA Sequences.fasta")
# # Confirm zero count is none
# find_dashes("ALResult_Not HA Sequences.fasta", "Not HA Sequences")
# #

# #########################################################
# # Find sequence lengths, find position for beginning and end of HA and NA sequences Chosen Files
HAseq = len("M-KAILVV--LLYTF-------ATANADTLCIGYHANNSTDTVDTVLEKNVTVTHSVNLL"
            "EDKHNGKLCKLRGVAPLHLGKCNIAGWILGNPECESLSTASSWSYIVETSSSDNGTCYPG"
            "DFIDYEELREQLSSVSSFERFEIFPKTSSWPNHDSNKGVTAACPHAGAKSFYKNLIWL--"
            "VKKGNSYPKLSKSYINDKGKEVLVLWGIHHPSTSADQQSLYQNADAYVFVGTSRYSKKFK"
            "PEIAIRPKVRDQEGRMNYYWTLVEPGDKITFEATGNLVVPRYAFAMERNAGSGIIISDTP"
            "V-HDCNTTCQTPKGAIN---TSLPFQNIHPITIGNCPKYVKSTKLRLATGLRNVPSIQ--"
            "--S--------RGLFGAIAGFIEGGWTGMVDGWYGYHHQNEQGSGYAADLKSTQNAIDKI"
            "TNKVNSVIEKMNTQFTAVGKEFNHLEKRIENLNKKVDDGFLDIWTYNAELLVLLENERTL"
            "DYHDSNVKNLYEKVRSQLKNNAKEIGNGCFEFYHKCDNTCMESVKNGTYDYPKYSEEAKL"
            "NREEIDGVKLESTRIYQILAIYSTVASSLVLIVSLGAISFWMCS--NGSLQCRICI".strip())
NAseq = len("MNPNQKIITIGSVCMTIGMANLILQIGNIISIWISHSIQLG---------NQNQIETCNQ-SVIT--YENNTWVNQTYVNISNT-NFAA--GQSVV"
            "SVKLAGNSSLCPVSGWAIYSKDNSIRIGSKGDVFVIREPFISCSPLECRTFFLTQGALLNDKHSNGTIKDRSPYRTLMSCPIGEVPSPYNSRFESV"
            "AWSASACHDGINWLTIGISGPDNGAVAVLKYNGIITDTIKSWRNNILRTQESECACVNGSCFTVMTDGPSDGQASYKIFRIEKGKIVKSVEMNAPN"
            "-YHYEECSCYPDSSEITCVCRDNWHGSNRPWVSFN-QNLEYQIGYICSGIFGDNPRPNDK--TGSC-GPVSSNG-ANGVKGFSFKYGNGVWIGRTK"
            "SISSRNGFEMIWDPNGWTGTDNNFSI-KQDIVGINEWSGYSGSFVQHPELTGLDCIRPCFWVELIRGRP-KEN-TIWTSGSSISFCGVNSDTVGWS"
            "WPDGAELPFTIDK-".strip())
print("Chosen File")
print("Length of HA - " + str(HAseq) + "\nLength of NA - " + str(NAseq))
######################
# CHOSEN FILES       #
# Length of HA - 596 #
# Length of NA - 494 #
######################

#########################################################
# Merge Chosen Files


def write_data_2(fh, header, data):
    """Functions to write output results to file
    if nothing input then skip, otherwise assume that
    .strip() has been used on all strings"""
    # fhw = open(filename, "w")
    if len(header) <= 0 or len(data) <= 0:
        return
    else:
        fh.write(str(header + "\n"))
        fh.write(str(data) + "\n")
        fh.write("\n")


def find_match(second_file, title):
    """Function used to find match to header in another fasta file
    works by returning/finding header and sequence by looking until next
    header is found then return what it found before that."""
    # Initialize variables/ open files
    seq2 = ""
    header2 = ""
    match_fh = open(second_file, "r")
    # parse through lines of file
    for lines in match_fh:
        # If > found assume its header
        if lines[0] == ">":
            # header2 = lines
            # If a header has been found, pull strain name, orgainism and subtype for new header
            if len(header2) > 0:
                matches2 = re.findall("(Strain Name:[AB]\/[\/A-Za-z 0-9()\\-_'.]+)", header2)
                subtype_match2 = re.findall("(Subtype:[A-Za-z0-9]+)", header2)
                organ2 = re.findall("(Organism:[\/A-Za-z 0-9()\\-_'.]+)", header2)
                header2 = ">" + organ2[0] + "|" + matches2[0] + "|" + subtype_match2[0]
            # if new header equals input header then return it and the sequence
            if header2 == title:
                match_fh.close()
                print("match")
                return header2, seq2
            # Reset the header and seq
            header2 = lines
            seq2 = ""

        else:
            # if it is part of the sequence
            seq2 = seq2 + lines

    # to return the last entry in the file, since loop won't be able to return it
    matches2 = re.findall("(Strain Name:[AB]\/[\/A-Za-z 0-9()\\-_'.]+)", header2)
    subtype_match2 = re.findall("(Subtype:[A-Za-z0-9]+)", header2)
    organ2 = re.findall("(Organism:[\/A-Za-z 0-9()\\-_'.]+)", header2)
    header2 = ">" + organ2[0] + "|" + matches2[0] + "|" + subtype_match2[0]
    match_fh.close()
    return header2, seq2


def fusion(first_fh, fused_fh, compare_file):
    """Function to fuse two sequences with the same header together
    works by finding header and sequence by looking until next
    header is found then return what it found before that."""
    # initialize
    ha_seq = ""
    ha_header = ""
    # parse through file
    for line in first_fh:
        # if a > is found assume it is header
        if line[0] == ">":
            # ha_header = line
            # if the header is found (length > 0)
            if len(ha_header) > 0:
                # pull needed information from header to make new one
                matches = re.findall("(Strain Name:[AB]\/[\/A-Za-z 0-9()\\-_'.]+)", ha_header)
                subtype_match = re.findall("(Subtype:[A-Za-z0-9]+)", ha_header)
                organ = re.findall("(Organism:[\/A-Za-z 0-9()\\-_'.]+)", ha_header)
                ha_header = ">" + organ[0] + "|" + matches[0] + "|" + subtype_match[0]
            # print(ha_header)
            # Call find_match function, input the file to search and the new header created.
            na_header, na_seq = find_match(compare_file, ha_header)
            # if return is equal then write to new file with two sequences fused
            if na_header == ha_header:
                write_data_2(fused_fh, ha_header, ha_seq.strip() + "\n" + na_seq.strip())
            # reset variables
            ha_header = line
            ha_seq = ""

        else:
            # if it is part of the sequence
            ha_seq = ha_seq + line

    # To return/write the last entries in the files, won't get written in loop
    matches = re.findall("(Strain Name:[AB]\/[\/A-Za-z 0-9()\\-_'.]+)", ha_header)
    subtype_match = re.findall("(Subtype:[A-Za-z0-9]+)", ha_header)
    organ = re.findall("(Organism:[\/A-Za-z 0-9()\\-_'.]+)", ha_header)
    ha_header = ">" + organ[0] + "|" + matches[0] + "|" + subtype_match[0]
    na_header, na_seq = find_match(compare_file, ha_header)
    if na_header == ha_header:
        # print("matches2")
        # print(ha_header)
        write_data_2(fused_fh, ha_header, ha_seq.strip() + "\n" + na_seq.strip())

    # Close Files
    first_fh.close()
    fused_fh.close()


# ###############******************************************************************************************
# # Fuse Chosen files together, call above function
# file_1 = "ALResult_Chosen HA File.fasta"
# file_2 = "LResult_Chosen NA File.fasta"
# Chosen_Fuse = "Chosen_Fuse.fasta"
#
# file_1_fh = open(file_1, "r")
# CF_fh = open(Chosen_Fuse, "w")
# fusion(file_1_fh, CF_fh, file_2)
# print("Chosen fusion complete")
# file_1_fh.close()
# CF_fh.close()


#################################
# Find sequence lengths, find position for beginning and end of HA and NA sequences Not Chosen Files
HAseq = len("M-KAILVV--LLYTFVT--------ANADTLCIGYHANNSTDTVDTVLEKNVTVTHSVNL"
            "LEDKHNGKLCKLRGVAPLHLGKCNIAGWILGNPECESLSTASSWSYIVETSSSDNGTCYP"
            "GDFIDYEELREQLSSVSSFERFEIFPKTSSWPNHDSNKGVTAACPHAGAKSFYKNLIWL-"
            "-VKKGNSYPKLSKSYINDKGKEVLVLWGIHHPSTSADQQSLYQNADAYVFVGTSRYSKKF"
            "KPEIAIRPKVRDQEGRMNYYWTLVEPGDKITFEATGNLVVPRYAFAMERNAGSGIIISDT"
            "PV-HDCNTTCQTPKGAIN---TSLPFQNIHPITIGKCPKYVKSTKLRLATGLRNVPSIQ-"
            "---S---------RGLFGAIAGFIEGGWTGMVDGWYGYHHQNEQGSGYAADLKSTQHAID"
            "EITNKVNSVIEKMNTQFTAVGKEFNHLEKRIENLNKKVDDGFLDIWTYNAELLVLLENER"
            "TLDYHDSNVKNLYEKVRSQLKNNAKEIGNGCFEFYHKCDNTCMESVKNGTYDYPKYSEEA"
            "KLNREEIDGVKLESTRIYQILAIYSTVASSLVLVVSLGAISFWMCSNGSLQCRICI".strip())
NAseq = len("MNPNQKIITIGSVCMTIGMANLILQIGNIISIWISHSIQLGN------QNQIE-"
            "----TCNQSVITYENNTWVNQTYVNISNTNFAA--GQSVVSVKLAGNSSLCPVSGWAIYS"
            "KDNSIRIGSKGDVFVIREPFISCSPLECRTFFLTQGALLNDKHSNGTIKDRSPYRTLMSC"
            "PIGEVPSPYNSRFESVAWSASACHDGINWLTIGISGPDNGAVAVLKYNGIITDTIKSWRN"
            "NILRTQESECACVNGSCFTVMTDGPSDGQASYKIFRIEKGKIVKSVEMNAPN-YHYEECS"
            "CYPDSSEITCVCRDNWHGSNRPWVSFN-QNLEYQIGYICSGIFGDNPRPNDK--TGSC-G"
            "PVSS-NG-ANGVKGFSFKYGNGVWIGRTKSISSRNGFEMIWDPNGWTGTDNNFSI-KQDI"
            "VGINEWSGYSGSFVQHPELTGLDCIRPCFWVELIRGRP-KEN-TIWTSGSSISFCGVNSD"
            "TVGWSWPDGAELPFTIDK-".strip())
print("Not Chosen file")
print("Length of HA - " + str(HAseq) + "\nLength of NA - " + str(NAseq))
######################
# NOT CHOSEN FILES   #
# Length of HA - 596 #
# Length of NA - 493 #
######################
# ##################**************************************************************************************************
# # # Fuse Not Chosen files together, using above functions
# file_1 = "ALResult_Not HA Sequences.fasta"
# file_2 = "ALResult_Not NA Sequences.fasta"
# NC_Fuse = "Not_Chosen_Fuse.fasta"
#
# file_1_fh = open(file_1, "r")
# CF_fh = open(NC_Fuse, "w")
# fusion(file_1_fh, CF_fh, file_2)
# print("Not Chosen fusion complete")
# file_1_fh.close()
# CF_fh.close()
# #################
