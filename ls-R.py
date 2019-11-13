import os,pprint
# for line in os.walk("E:/nsd1905"):
#     print(line)

# for path,folders,files in os.walk("E:/nsd1905"):
#     print("%s:\n%s\n%s" % (path,folders,files))

for path,folders,files in os.walk("E:/nsd1905"):
    print("%s:" % path)
    for d in folders:
        print(d,end="\t")
    for f in files:
        print(f,end="\t")
    print('\n')