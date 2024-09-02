import csv

# 读取 szse.csv 文件中的内容
szse_data = []
with open('listed_companies/szse.csv', 'r', encoding='utf-8') as szse_file:
    szse_reader = csv.reader(szse_file)
    for row in szse_reader:
        szse_data.append(row)

# 读取 y.csv 文件中的内容
y_data = {}
with open('y.csv', 'r', encoding='utf-8') as y_file:
    y_reader = csv.reader(y_file)
    next(y_reader)  # 跳过表头
    for row in y_reader:
        secCode = row[0]
        y_data[secCode] = row

# 循环遍历 szse.csv 中的行，检查是否在 y.csv 中
output_data = []
for row in szse_data:
    secCode = row[0]
    if secCode in y_data:
        output_data.append(y_data[secCode])
    else:
        # 如果不在 y.csv 中，就补空
        output_data.append([secCode, row[1], '', ''])

# 将结果写入新的 output.csv 文件中
with open('output.csv', 'w', newline='', encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file)
    # 写入表头
    csv_writer.writerow(['secCode', 'secName', 'title', 'publishTime'])
    # 写入数据
    csv_writer.writerows(output_data)

print("数据处理完成，结果已保存到 output.csv 文件中。")