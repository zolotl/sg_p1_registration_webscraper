from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def save_info_on_page(wd, schools_df):
    # find all school cards
    school_cards = wd.find_elements(By.XPATH, "//div[@class='moe-vacancies-ballot-card m-b:m moe-vacancies-ballot-card--dot-active-in-phase']")
    for school_card in school_cards:
        school_info = {}
        school_info["school_name"] = school_card.find_element(By.CLASS_NAME, "moe-vacancies-ballot-card__color-dot--green").text

        toggle_down = school_card.find_element(By.XPATH, ".//a[@class='icon-chevron-down moe-vacancies-ballot-card__toggler']")
        action.move_to_element(toggle_down).click().perform()
        school_info["total_vacancies"] = school_card.find_element(By.CLASS_NAME, "moe-vacancies-ballot-card__total-vacancies").find_element(By.TAG_NAME, 'p').text
        phases = school_card.find_elements(By.CLASS_NAME, "moe-vacancies-ballot-card__phase")
        # Get info for each phase
        for i, phase in enumerate(phases):
            vacancies = '-'
            applicants = '-'
            ballot_vacancies = '-'
            ballot_applicants = '-'
            ballot_criteria = '-'

            try:
                vacancies = phase.find_elements(By.XPATH, ".//p[@class='info-data']")[0].text
                applicants = phase.find_elements(By.XPATH, ".//p[@class='info-data']")[1].text

                if phase.find_element(By.XPATH, ".//div[@class='moe-vacancies-ballot-card__balloting']/p[1]/span").text == 'Yes':
                    ballot_vacancies =  phase.find_elements(By.XPATH, ".//div[@class='info-block-balloted info-block d:f jc-sb clearfix']//p[@class='info-data']")[0].text
                    ballot_applicants = phase.find_elements(By.XPATH, ".//div[@class='info-block-balloted info-block d:f jc-sb clearfix']//p[@class='info-data']")[1].text
                    ballot_criteria = phase.find_element(By.XPATH, ".//div[@class='moe-vacancies-ballot-card__balloting']/p[2]/span").text

            except:
                vacancies = '-'
                applicants = '-'
                ballot_vacancies = '-'
                ballot_applicants = '-'
                ballot_criteria = '-'

            
            phases_dict = {
                0 : "1",
                1 : "2A", 
                2 : "2B", 
                3 : "2C", 
                4 : "2C S"
            }
                
            # Enter data into the dict
            school_info[f"phase {phases_dict[i]} vacancies"] = vacancies
            school_info[f"phase {phases_dict[i]} applicants"] = applicants
            school_info[f"phase {phases_dict[i]} ballot_vacancies"] = ballot_vacancies
            school_info[f"phase {phases_dict[i]} ballot_applicants"] = ballot_applicants
            school_info[f"phase {phases_dict[i]} ballot_criteria"] = ballot_criteria

            # Add to df
        schools_df.loc[len(schools_df)] = school_info


schools_df = pd.DataFrame(columns=["school_name", "total_vacancies", 
                                   "phase 1 vacancies", "phase 1 applicants", "phase 1 ballot_vacancies", "phase 1 ballot_applicants", "phase 1 ballot_criteria",
                                   "phase 2A vacancies",  "phase 2A applicants", "phase 2A ballot_vacancies", "phase 2A ballot_applicants", "phase 2A ballot_criteria",
                                   "phase 2B vacancies",  "phase 2B applicants", "phase 2B ballot_vacancies", "phase 2B ballot_applicants", "phase 2B ballot_criteria",
                                   "phase 2C vacancies",  "phase 2C applicants", "phase 2C ballot_vacancies", "phase 2C ballot_applicants", "phase 2C ballot_criteria",
                                   "phase 2C S vacancies", "phase 2C S applicants", "phase 2C S ballot_vacancies", "phase 2C S ballot_applicants", "phase 2C S ballot_criteria"
                                   ])

# Instantiate chrome web driver
wd = webdriver.Chrome()
url = "https://www.moe.gov.sg/primary/p1-registration/past-vacancies-and-balloting-data"
wd.get(url)

# wait for school cards to be loaded
WebDriverWait(wd, 20).until(
EC.visibility_of_element_located(
    (By.XPATH, "//div[@class='moe-vacancies-ballot-card m-b:m moe-vacancies-ballot-card--dot-active-in-phase']")
    )
)

# create action chain object
action = ActionChains(wd)

naviagte_bar = wd.find_element(By.XPATH, "//div[@class='secondary-filter-block desktop(d:f) desktop(fl:r) desktop(fl:n) desktop(pos:r) m-b:0  b:0 r:0'][1]")
num_pgs = int(naviagte_bar.find_element(By.CLASS_NAME, 'pag-text').text[-2:])

for i in range(1, num_pgs+1):
    save_info_on_page(wd, schools_df)
    # get button
    button = wd.find_element(By.XPATH, "//button[@class='btn-pagination btn-pag-next'][1]")
    # perform the operation
    action.move_to_element(button).click().perform()

schools_df.to_csv('results_2022.csv', index=False)