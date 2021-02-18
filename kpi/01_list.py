list1 = [["物料代码", "售价"], ["A001", 60], ["A002", 59], ["A003", 65], ["A004", 62]]
list2 = [["物料代码", "系列", "保本价"], ["A001", "俊越1", 30], ["A002", "俊越2", 32], ["A003", "俊越3", 28]]

sum_max = 0
number = 0
for i in range(len(list1)):
    for y in range(len(list2)):
        if list1[i][0] == list2[y][0]:
            list1[i].append(list2[y][1])
            list1[i].append(list2[y][2])
            # 再添加计算列，利润
            if i != 0:
                list1[i].append(round((list1[i][1] - list1[i][3]) / list1[i][1], 4))

            else:
                list1[i].append("利润率")

            break
        else:
            # 判断是不是list2循环最后一个，如果是，这list1中加入空值
            if y == len(list2) - 1:
                list1[i].append(0)
                list1[i].append(0)
                list1[i].append(0)
    if i != 0:
        if list1[i][4] != 0:
            number += 1
            sum_max += list1[i][4]

print(list1)
print(round(sum_max / number, 4))
