from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import date

def save_info_on_page(wd, name_li, vacancies_li, applicants_li, ballot_criteria_li):
    # find all school cards
    school_cards = wd.find_elements(By.XPATH, "//div[@class='moe-ballot-card m-b:m  ']")
    for school_card in school_cards:
        name_li.append(school_card.find_element(By.XPATH, ".//h3").text)
        vacancies_li.append(school_card.find_element(By.XPATH, ".//div[@class='info-item'][1]/p[2]").text)
        applicants_li.append(school_card.find_element(By.XPATH, ".//div[@class='info-item'][2]/p[2]").text)
        try:
            # ballot_vacancies =  phase.find_elements(By.XPATH, ".//div[@class='info-block-balloted info-block d:f jc-sb clearfix']//p[@class='info-data']")[0].text
            # ballot_applicants = phase.find_elements(By.XPATH, ".//div[@class='info-block-balloted info-block d:f jc-sb clearfix']//p[@class='info-data']")[1].text
            ballot_criteria_li.append(school_card.find_element(By.XPATH, "./div[2]/p[2]").text)
        except:
            ballot_criteria_li.append("-")
    
    return name_li, vacancies_li, applicants_li


# Sets the day to current date
day = date.today().strftime("%d/%m/%Y")

# existing csv file to be appended to
csv_path = "results_2023.csv"
schools_df = pd.read_csv(csv_path)

# Instantiate chrome web driver
wd = webdriver.Chrome()
url = "https://www.moe.gov.sg/primary/p1-registration/vacancies-and-balloting"
wd.get(url)

# wait for school cards to be loaded
WebDriverWait(wd, 20).until(
EC.visibility_of_element_located(
    (By.XPATH, "//div[@class='moe-ballot-card m-b:m  ']")
    )
)

# create action chain object
action = ActionChains(wd)

naviagte_bar = wd.find_element(By.XPATH, "//div[@class='moe-detail-pagination m-l:m d:f fl:r'][1]")
num_pgs = int(naviagte_bar.find_element(By.CLASS_NAME, 'pag-text').text[-2:])

name_li = []
vacancies_li = []
applicants_li = []
ballot_criteria_li = []

# for each page, get the school name, vacancies and applicants
for i in range(1, num_pgs+1):
    name_li, vacancies_li, applicants_li = save_info_on_page(wd, name_li, vacancies_li, applicants_li, ballot_criteria_li)
    # get button
    button = wd.find_element(By.XPATH, "//button[@class='btn-pagination btn-pag-next'][1]")
    # perform the operation
    action.move_to_element(button).click().perform()

# find phase name to label column
phase_name = wd.find_element(By.XPATH, "//p[@class='info-title']").text[-2:]

# append new columns to df
schools_df['school_name'] = name_li
schools_df[f'{day} phase {phase_name} vacancies'] = vacancies_li  
schools_df[f'{day} phase {phase_name} applicants'] = applicants_li
schools_df[f'{day} phase {phase_name} ballot_criteria'] = ballot_criteria_li

# save df as csv
schools_df.to_csv(csv_path, index=False)