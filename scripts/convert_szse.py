import json
import csv

# 存储结果的数组
result = []

# 打开并按行读取文件
with open('x.json', 'r', encoding='utf-8') as file:
    for line in file:
        # 解析每一行的 JSON 数据
        data = json.loads(line)
        
        # 提取 data 中每个 item 的所需字段
        for item in data.get('data', []):
            secCode = item.get('secCode')[0] if isinstance(item.get('secCode'), list) else item.get('secCode')
            secName = item.get('secName')[0] if isinstance(item.get('secName'), list) else item.get('secName')
            title = item.get('title')
            publishTime = item.get('publishTime')
            
            # 将提取的内容存储到数组中
            result.append({
                'secCode': secCode,
                'secName': secName,
                'title': title,
                'publishTime': publishTime
            })

# 根据 secCode 去重并排序
unique_result = list({item['secCode']: item for item in result}.values())
unique_result.sort(key=lambda x: x['secCode'])

# 将结果写入 y.csv 文件
with open('y.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # 写入表头
    csvwriter.writerow(['secCode', 'secName', 'title', 'publishTime'])
    # 写入数据
    for item in unique_result:
        csvwriter.writerow([item['secCode'], item['secName'], item['title'], item['publishTime']])

# 打印结果
print(unique_result)