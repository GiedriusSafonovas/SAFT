import xml.etree.cElementTree as ET
import time
import csv
import re
import os

begin = time.time()

print(os.getcwd())
root = ""
writenode = ""
xmlname = ""
nodelst = list()
data = list()
f = open("config.txt")
for i in f:
    # print(i)
    if re.match('Root',i):
        root = i.split("=")[1].strip()
    elif re.match('Write',i):
        writenode = i.split("=")[1].strip()
    elif re.match('File',i):
        xmlname = i.split("=")[1].strip()
    else:
        nodelst.append(i.strip())
        data.append("")
f.close()

x = 0
counter = 0
path = root[0:len(root)-1]
write = False
ns = 0 #namespace
filenr = 1
linesWriten = 0

f = open(os.path.join(os.getcwd(),"Output","Output" + str(filenr) + ".csv"), "w", newline='', encoding="utf-8-sig")
writer = csv.writer(f)
writer.writerow(nodelst)
context = ET.iterparse(xmlname, events = ("start", "end"))
context = iter(context)

# print(len(nodelst))
# print(len(data))
for event, elem in context:
    # print(elem.tag.split("}")[0][0:])
    if re.search('{.',elem.tag.split("}")[0][0:]) != None:
        ns = 1
    # print(ns)
    break


for event, elem in context:
    if event == "start":
        if write:
            path = path + "/" + elem.tag.split("}")[ns][0:]

        if elem.tag.split("}")[ns][0:] == root[root.rfind("/",0,root.rfind("/")-1)+1:root.rfind("/")]: #fix this
            write = True
            print(write)

    if write:
        if event == "end":
            if elem.tag.split("}")[ns][0:] == "NumberOfEntries":
                print("NumberOfEntries:", elem.text)
            if elem.tag.split("}")[ns][0:] == "TotalDebit":
                print("TotalDebit:", elem.text)
            if elem.tag.split("}")[ns][0:] == "TotalCredit":
                print("TotalCredit:", elem.text)
            for i in nodelst: #TODO: Nedaryti jei nėra dalis reikalingo node
                # print(i)
                # print(path)
                # print(i==path)
                if i == path:
                    if data[nodelst.index(i)] != "":
                        writer.writerow(data)
                        elem.clear()
                        linesWriten += 1
                        if linesWriten == 1000000:
                            f.close()
                            filenr += 1
                            f = open(os.path.join(os.getcwd(),"Output","Output" + str(filenr) + ".csv"), "w", newline='', encoding="utf-8-sig")
                            writer = csv.writer(f)
                            linesWriten = 0
                            writer.writerow(nodelst)
                        for j in range(len(data)):
                            data[j] = ""
                    data[nodelst.index(i)] = elem.text
        # print(elem.tag.split("}")[1][0:])
        # print("tag: ", elem.tag.split("}")[ns][0:])
        # print("root", root[root.rfind("/",0,root.rfind("/")-1)+1:root.rfind("/")])
            path = path[:path.rfind("/")]
            if path == writenode:
                writer.writerow(data)
                elem.clear()
                linesWriten += 1
                if linesWriten == 1000000:
                    f.close()
                    filenr += 1
                    f = open(os.path.join(os.getcwd(),"Output","Output" + str(filenr) + ".csv"), "w", newline='', encoding="utf-8-sig")
                    writer = csv.writer(f)
                    linesWriten = 0
                    writer.writerow(nodelst)
                for i in range(len(data)):
                    data[i] = ""
            if elem.tag.split("}")[ns][0:] == root[root.rfind("/",0,root.rfind("/")-1)+1:root.rfind("/")]:
                write = False
                writer.writerow(data)
                elem.clear()
                print(write)
    if write != True:
        elem.clear()



    # print('Current path is: ', path)


    x = x+1
    if x == 50000:
        counter = counter + x
        print("\r" + str(counter), end="")
        x = 0
    # print('event: ',  event)
    # print('tag: ', elem.tag)
    # print('text: ', elem.text)

f.close()
time.sleep(1)
end = time.time()
print("")
print('Time: ', end-begin)
input()
