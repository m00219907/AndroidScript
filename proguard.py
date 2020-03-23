import random

outfile = open("dict.txt", "w")
resultList=[]
for i in range(20000):
    count = random.randint(2,10)
    result=''
    for m in range(count):
        result += random.choice('iIlL1')
    if result not in resultList:
        resultList.append(result)
        outfile.write(result)
        outfile.write('\n')
        if len(resultList)==8000:break;
outfile.close()