from lxml import etree
import pandas as pd

html_content = driver.page_source
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
        phn="No Specified"
    try:
        address=stats_phn_add.xpath('./div[1]/span[2]/span[2]')[0].text
    except IndexError:
        address="Click Here->"
        
    typ=stats_phn_add.xpath('./div[1]/span[1]/span[1]')[0]
    
    full_list.append([name.get('aria-label'),typ.text,rat,Status,phn,address,f'=HYPERLINK("{name.get("href")}", "Link")'])

df=pd.DataFrame(full_list,columns=["NAME","TYPE","STATUS","RATING","PHONE NO.","ADDRESS","LINKS"])
df.to_excel(f"{loc}.xlsx", index=False)