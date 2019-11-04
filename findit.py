# Find /count co-mutations from step 4 output files

fileList = ['C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\2000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\3000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\4000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\5000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\6000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\7000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\8000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\9000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\10000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\11000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\12000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\13000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\14000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\15000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\16000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\17000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\18000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\19000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\20000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\21000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\22000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\23000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\24000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\25000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\26000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\27000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\28000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\29000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\30000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\31000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\32000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\33000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\34000000-chosen_output.txt',
            'C:\\Users\\Rebecca\\Desktop\\Class\\Project\\Not Data Run\\35000000-chosen_output.txt']
resultList = []
fh_out = open("not_output_short.txt", "w")
count = 0


def find_it(input_file):
    global fh_out, count
    print("Working...")
    for line in input_file:

        if line[0] == '*':
            # pull next two lines
            nextline = input_file.readline()
            lastline = input_file.readline()
            fh_out.write(line + nextline + lastline + "\n")
            count += 1
    print("File Done")


for file in fileList:
    fh = open(file)
    find_it(fh)

print("All Files Completed")
print("Total Number Found: " + str(count))



# Find sections of sequence comutations are in,
# input is short file created above

input = open("chosen_output_short.txt")

limit1 = 596
# limit2 = 494
hacount = 0
bothcount = 0
nacount = 0
not_count = 0
keep = {}
for line in input:
    if line[0] == "*":
        line_list = line.strip().split(',')
        # print(list)
        x1 = line_list[0].strip().split("  ")[1]
        y2 = line_list[1].strip()
        num1 = x1[:len(x1) - 1]
        num2 = y2[:len(y2) - 1]
        # Includes co-mutations that are 100% found, conserved, not necessarily co-mutations
        # keep[x1] = keep.get(x1, "") + y2 + " "
        # print(num1 + " " + num2)
        list2 = input.readline().strip().split(" ")
        input.readline()
        list_object = list2[0].split("/")
        if list_object[0] == list_object[1]:
            not_count += 1
            continue
        # else:
        if x1[len(x1)-1] == "-" and y2[len(y2)-1] == '-':
            not_count += 1
            continue
        keep[x1] = keep.get(x1, "") + y2 + " "
        if int(num1) < limit1 and int(num2) < limit1:
            hacount += 1
        if int(num1) < limit1 and int(num2) >= limit1:
            bothcount += 1
        if int(num1) >= limit1 and int(num2) >= limit1:
            nacount += 1

print("HA Count: " + str(hacount))
print("Both Count: " + str(bothcount))
print("NA Count: " + str(nacount))
print("Not count: " + str(not_count))


out = open("table.txt", "w")
for key in sorted(keep.keys()):
    item = keep.get(key)
    hastring, bothstring, nastring = "", "", ""
    for thing in item.strip().split(" "):
        num_item = int(thing[:len(thing)-1])
        num_key = int(key[:len(key)-1])
        if num_key < limit1 and num_item < limit1:
            hastring = hastring + thing + " "
        if num_key < limit1 and num_item >= limit1:
            bothstring = bothstring + thing + " "
        if num_key >= limit1 and num_item >= limit1:
            nastring = nastring + thing + " "
    out.write(key + " : " + hastring + "||" + bothstring + "||" + nastring + "\n")

