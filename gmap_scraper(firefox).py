import time
st=time.time()
import subprocess
def install_library(library_name):
    try:
        print(f"So Installing {library_name}...")
        subprocess.check_call(['pip', 'install', library_name])
        print(f"Successfully installed {library_name}")
    except subprocess.CalledProcessError as e:
        file_name="logs.txt"
        file=open(file_name,'w')
        file.write(e)
        file.close()
        print(f"Failed to install {library_name}/nContact Creator/nGMAIL: connectwithsanthosh@gmail.com\nUPLOAD {file_name} In Current Program Directory For Better Analysis")
        input("Press Enter To Exit...")
        exit()

try:
    from lxml import etree
except ModuleNotFoundError:
    print("This Takes Few Moments For First Time Only")
    print("Module Not Found!!!")
    install_library("lxml")
    from lxml import etree
try:
    import pandas as pd
except:
    print("Module Not Found!!!")
    install_library("pandas")
    import pandas as pd
try:
    from selenium import webdriver
except:
    print("Module Not Found!!!")
    install_library("selenium")
    from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import StaleElementReferenceException,TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import multiprocessing

loc=input("Enter input(eg: gift shop in vandavasi) : ")
print("Wait A Moment Getting Data From Gmaps For You...")
def page_html(loc,mp):
    headOption = webdriver.FirefoxOptions()
    headOption.add_argument("--headless")
    driver = webdriver.Firefox(options=headOption)
    #print("...")
    driver.get(f"https://www.google.com/maps/search/{loc.strip().replace(' ' ,'+')}/@13.0208721,80.1231215,13z/data=!3m1!4b1?entry=ttu")
    driver.implicitly_wait(30)
    while True:
        try:  
            ele=driver.find_elements(By.CLASS_NAME,"hfpxzc")
            driver.execute_script("arguments[0].scrollIntoView();", ele[-1])
            if EC.presence_of_element_located((By.XPATH,"//div[@class='PbZDve ']//p[@class='fontBodyMedium ']//span[@class='HlvSq']")) and EC.invisibility_of_element((By.XPATH,'//div[@class="lXJj5c Hk4XGb "]/div[@class="qjESne veYFef"]')):  
                if driver.find_element(By.XPATH,"//div[@class='PbZDve ']//p[@class='fontBodyMedium ']//span[@class='HlvSq']").is_displayed():
                    #time.sleep(1)
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
    print("Almost There")
    p1.join()

    temp=driver_list[0]
    #print(temp[1])
    for i in range(1,len(driver_list)):
        #print(driver_list[i][1])
        temp=driver_list[i] if driver_list[i][1]>temp[1] else temp
    html_content=temp[0]
    # print("\nmax: ",temp[1])
    print("\n")





tree = etree.HTML(html_content)
NAME=tree.xpath('//a[@class="hfpxzc"]')
TYPE=tree.xpath('//div[@class="bfdHYd Ppzolf OFBs3e  "]/div[4]/div[1]/div/div/div[2]/div[4]/div[1]/span[1]/span')
RATTING=tree.xpath('//div[@class="bfdHYd Ppzolf OFBs3e  "]//span[@class="e4rVHe fontBodyMedium"]')
STATUS_PHN_ADD=tree.xpath('//div[@class="bfdHYd Ppzolf OFBs3e  "]//div[@class="UaQhfb fontBodyMedium"]/div[4]')

full_list=[]
for name,rats,stats_phn_add in zip(NAME,RATTING,STATUS_PHN_ADD):
    try:#reviews
        rat=rats.xpath('.//span[@class="ZkP5Je"]')[0].get('aria-label')
    except IndexError:
        rat=rats.text
    try:#status
        status=stats_phn_add.xpath('./div[2]/span/span/span[1]')[0].text.strip().split()[0]
        if status == "Open" or status=="Closed" or status=="Closes":
            Status="Functioning"
        else:
            Status=stats_phn_add.xpath('./div[2]/span/span/span[1]')[0].text
    except IndexError:
        Status="Not Specified"
    try:#phone
        phn=stats_phn_add.xpath('./div[2]/span[2]/span[2]')[0].text
    except IndexError:
        phn="Not Specified"
    try:
        address=stats_phn_add.xpath('./div[1]/span[2]/span[2]')[0].text
    except IndexError:
        address="Click Here->"
        
    typ=stats_phn_add.xpath('./div[1]/span[1]/span[1]')[0]
    
    full_list.append([name.get('aria-label'),typ.text,rat,Status,phn,address,f'=HYPERLINK("{name.get("href")}", "Link")'])

df=pd.DataFrame(full_list,columns=["NAME","TYPE","STATUS","RATING","PHONE NO.","ADDRESS","LINKS"])
df.to_excel(f"{loc}(approx).xlsx", index=False)
print(f"Your Excel Is Ready Check The Current Direcctory For {loc}(approx).xlsx\nIf You Have Any Issues Please Write To connectwithsanthoshmk@gmail.com")
t2=time.time()
print(t2-st)
