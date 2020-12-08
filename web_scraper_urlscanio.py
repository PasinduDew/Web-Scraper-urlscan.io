from selenium import webdriver
import tldextract
import time
from selenium.webdriver.chrome.options import Options
from datetime import datetime

now = datetime.now()
dateStr = now.strftime("%Y%m%d")


def writeToFile(filename, data_rows):
    with open(filename, 'a', encoding = 'utf-8', newline="") as file:
        
        for row in data_rows:
            file.write(row + "\n")


def createValidDomain(extracted_domain):
    if extracted_domain == "": return None
    parts = tldextract.extract(extracted_domain)

    if parts[0] == "":
        return parts[1] + "." + parts[2]
    else:
        return parts[0] + "." + parts[1] + "." + parts[2]


options = Options()
options.headless = True
path = r'E:\\Scrapy\\test_scrapy\\test\\chromedriver.exe'
# path = r'/usr/bin/chromedriver'

driver = webdriver.Chrome(executable_path = path, options = options)

driver.get('https://urlscan.io/')
driver.implicitly_wait(15)

print(createValidDomain("www.incenza.com/6-parfums/16-parfum-femme/623-flower-by-kenzo/1024-flower-by-ke..."))

prevDomains = set()
maxBuffer = 50
removeBuffer = 15
sleepTime = 8

while True:
    
    try:
        table = driver.find_element_by_xpath('//*[@id="scans"]/div/table/tbody')
        rows = table.find_elements_by_tag_name("tr")
        domains = set()

        for row in rows: 
            try:
                col = row.find_elements_by_tag_name("td")[1]
                extractedDomain = col.find_element_by_tag_name("a").get_attribute('text')
            
                domain = createValidDomain(extractedDomain)

                if domain != None and domain not in prevDomains:
                    domains.add(domain)
                # print(extractedDomain)
                print(domain)
                print("--------------------------------------------------------")
                
            except:
                print ("Error Occured: Unable to Find the Element")
                continue  
            
            

        if maxBuffer < (len(prevDomains) + len(domains)): 
            temp = list(prevDomains)
            prevDomains.clear()
            tempBuffer = set(temp[removeBuffer : ])
            prevDomains = prevDomains.union(tempBuffer)
            # print(">> ************* Removed " + str(removeBuffer) + " From Domains Buffer ****************")
            # print(">> ************* Pre Domains Set Length: " + str(len(prevDomains)))

        prevDomains = prevDomains.union(domains)
        # print(">> Pre Domains Set Length: " + str(len(prevDomains)))
        # print(">> Current Domains Set Length: " + str(len(domains)))

        writeToFile("urlscan_io_" + dateStr + ".csv", domains)

        

    except:
        print("Error Occured: Unable to Find Elements (Table or Rows). Waiting 1 Second...")
        time.sleep(1)
        continue

    time.sleep(sleepTime)
