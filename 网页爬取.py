import openpyxl
import selenium
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_list(url):
    """从网页中获取职位列表"""
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 30)
    job_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-job-result ul')))
    return job_list


def to_excel(job_list):
    """解析职位列表并存储到表格中"""
    job_df = pd.DataFrame(columns=['详细链接', '职位名称', '工作地址', '薪资', '职位要求', '招聘人名字', '招聘人职务',
                                   '公司logo', '公司详情', '公司名字', '公司情况', '技能要求', '福利待遇'])
    i = 0
    css = By.CSS_SELECTOR
    for job in job_list.find_elements(By.XPATH, 'li'):
        print(f'正在爬取第{i + 1}条数据')
        job_df.loc[i, '详细链接'] = job.find_element(css, '.job-card-left').get_attribute('href')
        job_df.loc[i, '职位名称'] = job.find_element(css, '.job-name').text
        job_df.loc[i, '工作地址'] = job.find_element(css, '.job-area').text
        job_df.loc[i, '薪资'] = job.find_element(css, '.salary').text
        post_list = []
        for post in job.find_elements(css, '.job-info .tag-list *'):
            post_list.append(post.text)
        job_df.loc[i, '职位要求'] = ','.join(post_list)
        recruit_name = job.find_element(css, '.info-public').text
        recruit_title = job.find_element(css, '.info-public em').text
        job_df.loc[i, '招聘人名字'] = recruit_name.replace(recruit_title, '')
        job_df.loc[i, '招聘人职务'] = recruit_title
        job_df.loc[i, '公司logo'] = job.find_element(css, '.company-logo img').get_attribute('src')
        job_df.loc[i, '公司详情'] = job.find_element(css, '.company-name a').get_attribute('href')
        job_df.loc[i, '公司名字'] = job.find_element(css, '.company-name').text
        company_list = []
        for company in job.find_elements(css, '.company-tag-list li'):
            company_list.append(company.text)
        job_df.loc[i, '公司情况'] = ','.join(company_list)
        skill_list = []
        for skill in job.find_elements(css, '.job-card-footer .tag-list li'):
            skill_list.append(skill.text)
        job_df.loc[i, '技能要求'] = ','.join(skill_list)
        job_df.loc[i, '福利待遇'] = job.find_element(css, '.info-desc').text
        i += 1

    return job_df


def loop_page(url0):
    """循环遍历所有页"""
    all_df = pd.DataFrame(columns=['详细链接', '职位名称', '工作地址', '薪资', '职位要求', '招聘人名字', '招聘人职务',
                                   '公司logo', '公司详情', '公司名字', '公司情况', '技能要求', '福利待遇'])
    for i in range(1, 11):
        url1 = url0 + '&page=' + str(i)
        print(f'开始爬取第{i}页，链接为{url1}')
        try:
            job_list = get_list(url1)
            job_df = to_excel(job_list)
        except selenium.common.exceptions.StaleElementReferenceException:
            print('网页出错，正在重新爬取')
            job_list = get_list(url1)
            job_df = to_excel(job_list)
        all_df = pd.concat([all_df, job_df])
    return all_df


def loop_station(station_list):
    """循环遍历不同职位"""
    url0 = 'https://www.zhipin.com/web/geek/job?city=100010000&position='
    for station in station_list:
        url = url0 + station[0]
        print(f'-------开始爬取{station[1]}岗位-------')
        df = loop_page(url)

        with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=station[1], index=False)


if __name__ == '__main__':
    now_time = datetime.now().strftime("%m%d-%H%M")
    file_name = f'job{now_time}.xlsx'
    workbook = openpyxl.Workbook()
    workbook.save(file_name)
    station_name = ['数据分析师', 'ETL工程师', '数据挖掘', '数据开发', '数据仓库', '数据架构师', '爬虫工程师',
                    '数据采集']
    station_id = ['100511', '100508', '100507', '100506', '100104', '100512', '100514', '100122']
    station_list = list(zip(station_id, station_name))
    station_list = station_list
    loop_station(station_list)
