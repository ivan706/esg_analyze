import requests
import json
import re
import time
import os
import csv
import yaml
import logging

# 创建一个logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('error.log')
fh.setLevel(logging.ERROR)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)

def get_esg_data(company_code):
    """
    发送GET请求到指定的URL，并从JSONP响应中提取公司是否发布过社会责任报告

    参数:
    company_code (str): 股票代码，将被插入到URL中。

    返回:
    response.text: 从JSONP响应中提取的数据。
    """
    url, headers, params = construct_url_and_header(company_code)
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.text
    except Exception as e:
        logger.error(f"Failed to get ESG data: {e}")
        raise

def get_sse_config():
    """
    从配置文件中读取SSE的配置信息。

    返回:
    config['SSE']: SSE的配置信息。
    """
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config['SSE']

def construct_url_and_header(company_code):
    """
    构造URL和请求头。

    参数:
    company_code (str): 股票代码，将被插入到URL中。

    返回:
    url: 构造完成的请求url。
    headers: 构造完成的请求头。
    params: 构造完成的请求参数。
    """
    sse_config = get_sse_config()
    url = sse_config['host']
    headers = sse_config['header']
    params = sse_config['parameters']
    params['productId'] = params['productId'].format(company_code=company_code)
    return url, headers, params

def parse_data(data):
    """
    从JSONP响应中使用正则，按照jsonp的callback函数名提取JSON数据。

    参数:
    data (str): JSONP响应。
    """
    try:
        data = re.sub(r'^jsonpCallback\(|\)$', '', data)
        data = json.loads(data)
        return data
    except Exception as e:
        logger.error(f"Failed to parse data: {e}")
        raise

def extract_esg_data(data):
    """
    从数据中提取公司社会责任信息数据。

    参数:
    data (dict): 从JSONP响应中提取的数据。
    """
    try:
        companies = data['result']
        return companies
    except Exception as e:
        logger.error(f"Failed to extract ESG data: {e}")
        raise

def write_esgs_to_file(esgs):
    """
    将省份的上市公司社会责任信息写入到文件中。

    参数:
    province_name (str): 省份名称，将被用作文件名。
    province_code (str): 省份代码，将被用作文件名。
    companies (list): 公司信息列表，每个公司是一个字典。
    """
    if not os.path.exists('./esgs'):
        os.makedirs('./esgs')

    filename = "./esgs/shangzheng.csv"
    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 表头
        writer.writerow(['股票代码', '公司简称', '最近一次发布报告名称', '发布日期'])
        # 数据
        for company in esgs:
            writer.writerow([company['SECURITY_CODE'], company['SECURITY_NAME'], company['TITLE'], company['SSEDATE']])


if __name__ == '__main__':
    _companies = []
    with open('listed_companies/sse.csv', 'r') as f:
        reader = csv.reader(f)
        _companies = [(int(row[0]), row[1]) for row in reader]
    # _companies = [(600000, '浦发银行')]
    esgs = []
    
    for _company in _companies:
        try:
            data = get_esg_data(_company[0])
            data = parse_data(data)
            esg_data = extract_esg_data(data)
        except Exception as e:
            logger.error(f"Failed to get ESG data for {_company[0]}:{_company[1]}")
            esg_data = []
        print(esg_data)
        if len(esg_data) > 0:
            esgs.extend([esg_data[0]])
        else:
            esgs.extend([{'SECURITY_CODE': _company[0], 'SECURITY_NAME': _company[1], 'TITLE': 'N/A', 'SSEDATE': 'N/A'}])
        time.sleep(1)
    
    write_esgs_to_file(esgs)
    
