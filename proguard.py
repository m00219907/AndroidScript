import random

# D1 Gσ6C
# D2 ρβpP
# D3 μυuU
# D8 αβγδεζηθικλμνξοπρστυφχψωΓΔΘΛΞΟΠΣΦΨΩ

outfile = open("dict.txt", "w", encoding='utf-8')
resultList=[]
for i in range(50000):
    count = random.randint(1,3)#D8(1,3) other(2,7)
    result=''
    for m in range(count):
        result += random.choice('αβγδεζηθικλμνξοπρστυφχψωΓΔΘΛΞΟΠΣΦΨΩ')
    if result not in resultList:
        resultList.append(result)
        outfile.write(result)
        outfile.write('\n')
        if len(resultList)==8000:break;
outfile.close()
