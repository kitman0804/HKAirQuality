import os
import re
import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui


# Working directory
wd = os.path.dirname(os.path.realpath(__file__))


# Air Quality Monitoring
url = "http://epic.epd.gov.hk/EPICDI/air/station/"


# Stations
# TSEUNG KWAN from 2016-03-16
# TUEN MUN from 2014-01-01
station = ["CENTRAL/WESTERN", 
           "EASTERN", 
           "KWAI CHUNG", 
           "KWUN TONG", 
           "SHAM SHUI PO", 
           "SHATIN", 
           "TAI PO", 
           "TAP MUN", 
           "TSEUNG KWAN O", 
           "TSUEN WAN", 
           "TUEN MUN", 
           "TUNG CHUNG", 
           "YUEN LONG", 
           "CAUSEWAY BAY", 
           "CENTRAL", 
           "MONG KOK", ]


# Air quality parameters
param = ["Carbon Monoxide", "Fine Suspended Particulates", "Nitrogen Dioxide", 
         "Nitrogen Oxides", "Ozone", "Respirable Suspended Particulates", 
         "Sulphur Dioxide", ]


# Set Chrome preference
dataFolder = os.path.join(wd, "rawdata")
chromeOptions = webdriver.ChromeOptions()
prefs = {'download.default_directory': dataFolder}
chromeOptions.add_experimental_option("prefs", prefs)
chromeDriver = os.path.join(wd, "chromedriver.exe")


    

def dl_csv(station, startYear=1990, endYear=2016):
    if endYear < startYear:
        print("'endYear < startYear'")
        return None
    # Turn on driver
    driver = webdriver.Chrome(executable_path=chromeDriver, 
                              chrome_options=chromeOptions)
    
    driver.get(url)
    # Wait until the page is loaded
    wait = ui.WebDriverWait(driver, 5)
    wait.until(lambda dr: dr.find_element_by_xpath("//html").is_displayed())
    
    # Select station s
    driver.find_element_by_xpath("//a[text() = '" + station + "']").click()
    time.sleep(0.5)
    # Wait until the page is loaded
    wait = ui.WebDriverWait(driver, 5)
    wait.until(lambda dr: dr.find_element_by_xpath("//html").is_displayed())
    
    # Click all parameters
    for p in param:
        driver.find_element_by_xpath("//label[contains(text(), '" + p + "')]").click()
        time.sleep(0.5)
    
    # Click 'Hourly'
    driver.find_element_by_xpath("//input[@value='hourly']").click()
    driver.find_element_by_xpath("//a[@id='form:select']").click()
    time.sleep(0.5)
    
    # Start date and end date
    startDate = driver.find_element_by_xpath("//span[@id='form:hourlyStartDate']").text
    startDate = re.split(pattern="-", string=startDate)
    startDate = [int(x) for x in startDate]
    endDate = driver.find_element_by_xpath("//span[@id='form:hourlyEndDate']").text
    endDate = re.split(pattern="-", string=endDate)
    endDate = [int(x) for x in endDate]
    
    # Click date
    for year in range(max(startYear, startDate[2]), min(endYear, endDate[2]) + 1):
        date = [("form:dailyFromYear", year)]
        if year == startDate[2]:
            date +=[("form:dailyFromMonth", startDate[1]), 
                    ("form:dailyFromDay", startDate[0])]
        else:
            date +=[("form:dailyFromMonth", 1), 
                    ("form:dailyFromDay", 1)]
        date += [("form:dailyToYear", year)]
        if year == endDate[2]:
            date += [("form:dailyToMonth", endDate[1]), 
                     ("form:dailyToDay", endDate[0])]
        else:
            date += [("form:dailyToMonth", 12), 
                     ("form:dailyToDay", 31)]
        
        # Click from and to date
        for d in date:
            xpath = "//select[@id='%s']/option[@value='%s']" % d
            driver.find_element_by_xpath(xpath).click()
            time.sleep(0.5)
        
        # Download file
        driver.find_element_by_xpath("//a[@id='form:excel']").click()
        
        # Change file name to AIR_YEAR_STATION.csv
        t = 0
        while True:
            try:
                newfilename = "AIR_%s_%s.csv" % (str(year), re.sub("/|\s", "_", station))
                os.rename(os.path.join(dataFolder, "air_hourly.csv"), 
                          os.path.join(dataFolder, newfilename))
                print("Downloaded air quality data of %s Station in %s" % (station, str(year)))
                break
            except:
                # check if the download is complete
                time.sleep(1)
                t += 1
                if t > 120:
                    print("The download time is too long.")
                    break
        
        # Take a 10 seconds break after each download
        time.sleep(10)
    
    # Close the browser and shut down the driver
    driver.quit()




# Start downloading data from 2000 to 2016
for s in station:
    dl_csv(station=s)





