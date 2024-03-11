import multiprocessing
import time
st=time.time()
# import multiprocessing
# import threading
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import StaleElementReferenceException,TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

loc=input("Enter input(eg: gift shop in vandavasi) : ")#"ayurvedic doctor in thoraipakkam"

def page_html(loc,mp):
    headOption = webdriver.FirefoxOptions()
    headOption.add_argument("--headless")
    driver = webdriver.Firefox(options=headOption)
    print("...")
    driver.get(f"https://www.google.com/maps/search/{loc.strip().replace(' ' ,'+')}/@13.0208721,80.1231215,13z/data=!3m1!4b1?entry=ttu")
    driver.implicitly_wait(30)
    while True:
        try:  
            ele=driver.find_elements(By.CLASS_NAME,"hfpxzc")
            driver.execute_script("arguments[0].scrollIntoView();", ele[-1])
            if EC.presence_of_element_located((By.XPATH,"//div[@class='PbZDve ']//p[@class='fontBodyMedium ']//span[@class='HlvSq']")) and EC.invisibility_of_element((By.XPATH,'//div[@class="lXJj5c Hk4XGb "]/div[@class="qjESne veYFef"]')):  
                if driver.find_element(By.XPATH,"//div[@class='PbZDve ']//p[@class='fontBodyMedium ']//span[@class='HlvSq']").is_displayed():
                    # time.sleep(1)
                    break
        except NoSuchElementException:
            continue
    ele=driver.find_elements(By.CLASS_NAME,"hfpxzc")
    source_html= driver.page_source
    driver.quit()
    driver_list.append([source_html,len(ele)])

#mutiprocessing
html_content=None
with multiprocessing.Manager() as manager:
    
    driver_list=manager.list([])
    for _ in range(multiprocessing.cpu_count()-1):
        p1=multiprocessing.Process(target=page_html,args=(loc,True,))
        p1.start()
    page_html(loc,False)
    p1.join()

    temp=driver_list[0]
    print(temp[1])
    for i in range(1,len(driver_list)):
        print(driver_list[i][1])
        temp=driver_list[i] if driver_list[i][1]>temp[1] else temp
    html_content=temp[0]
    print("\nmax: ",temp[1])
t2=time.time()
print(t2-st)
