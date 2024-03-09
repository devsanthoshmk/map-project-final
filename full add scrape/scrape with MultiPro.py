#NOT TESTED
import time
st=time.time()
import multiprocessing
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException,TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

def split_work(input_list, n):
    k, remainder = divmod(len(input_list), n)
    sublists = [input_list[i * k + min(i, remainder):(i + 1) * k + min(i + 1, remainder)] for i in range(n)]
    return sublists

def main_window(urls):

    headOption = webdriver.FirefoxOptions()
    headOption.add_argument("--headless")
    driver = webdriver.Firefox(options=headOption)
    driver.implicitly_wait(30)
    main_data(driver,urls)

def main_data(driver,urls):
    print(urls)
    n=0
    while n<len(urls):
        url=urls[n]
        
        driver.get(url)
        while True:
            l=[]
            try:
                print(driver.find_element(By.XPATH, '//h1[@class="DUwDvf lfPIob"]').text)
                l.append(driver.find_element(By.XPATH, '//h1[@class="DUwDvf lfPIob"]').text.strip())#name
                
                
                try:#type
                    ty=driver.find_element(By.XPATH,'//button[@class="DkEaL "]')
                    l.append(ty.text.strip())
                except NoSuchElementException:
                    l.append("Not Specified")

            #def statu(driver):
                try:#status
                    stat=driver.find_element(By.XPATH,'//div[@class="o0Svhf"]/span/span/span')
                    status=stat.text.strip()
                    if status == "Open" or status=="Closed" or status=="Closes soon":
                        l.append("Functioning")
                    else:
                        l.append(status)
                except NoSuchElementException:
                    l.append("Not Specified")
                
                try:#rating
                    rat=driver.find_element(By.XPATH,'//div[@class="F7nice "]/span/span[@aria-hidden="true"]')
                    l.append(rat.text.strip())
                    
                except NoSuchElementException:
                    l.append("Not Specified")
            
                try:#phone
                    phn=driver.find_element(By.XPATH,'//div[@class="RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L "]//button[@data-tooltip="Copy phone number"]//div[@class="Io6YTe fontBodyMedium kR99db "]')
                    l.append(phn.text.strip())
                except NoSuchElementException:
                    l.append("No Specified")
                
            #def address(driver):
                
                add=driver.find_element(By.CSS_SELECTOR,"div.RcCsl:nth-child(3) > button:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
                l.append(add.text.strip())#address
            #def link():

                l.append(url)#link
                data.append(l)
                # lock.acquire()
                # full_list.append(l)
                # lock.release()
                # print(l)
                break
            except (StaleElementReferenceException,TimeoutException):
                    print("staled")
        n+=1
    driver.quit()

    


loc=input("Enter input(eg: gift shop in vandavasi) : ")#"ayurvedic doctor in thoraipakkam" 
headOption = webdriver.FirefoxOptions()
headOption.add_argument("--headless")
driver = webdriver.Firefox(options=headOption)
print("...")
driver.get(f"https://www.google.com/maps/search/{loc.strip().replace(' ' ,'+')}/@13.0208721,80.1231215,13z/data=!3m1!4b1?entry=ttu")
#driver.implicitly_wait(30)
while True:
  try:  
    eles=driver.find_elements(By.CLASS_NAME,"hfpxzc")
    driver.execute_script("arguments[0].scrollIntoView();", eles[-1])
    if EC.presence_of_element_located((By.XPATH,"//div[@class='PbZDve ']//p[@class='fontBodyMedium ']//span[@class='HlvSq']")) and EC.invisibility_of_element((By.XPATH,'//div[@class="lXJj5c Hk4XGb "]/div[@class="qjESne veYFef"]')):  
        if driver.find_element(By.XPATH,"//div[@class='PbZDve ']//p[@class='fontBodyMedium ']//span[@class='HlvSq']").is_displayed():
            time.sleep(1)
            break
  except NoSuchElementException:
      continue


eles=driver.find_elements(By.CLASS_NAME,"hfpxzc")
print(len(eles))
urls=[ele.get_attribute("href") for ele in eles]
#main_data(urls)
with multiprocessing.Manager() as manager:
    
    data=manager.list([["NAME","TYPE","STATUS","RATING","PHONE NO.","ADDRESS","LINK"]])
    workers=split_work(urls,multiprocessing.cpu_count())
    worker1=workers.pop(0)
    #p1=multiprocessing.Process(target=main_data,args=(driver,workers.pop(0)))
    for sub_urls in workers:
        p2=multiprocessing.Process(target=main_window,args=(sub_urls,))
        p2.start()
    # p1.start()
    main_data(driver,worker1)
    # p1.join()
    p2.join()

    with open(f"results in {loc}.csv",'w') as r:
        writer=csv.writer(r)
        writer.writerows(data)
    r.close()
        
    

t2=time.time()
print((t2-st)/60)
# print(et2," ",(st-et2)/60)