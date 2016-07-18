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
           #"TSEUNG KWAN O", 
           "TSUEN WAN", 
           #"TUEN MUN", 
           "TUNG CHUNG", 
           "YUEN LONG", 
           "CAUSEWAY BAY", 
           "CENTRAL", 
           "MONG KOK"]


# Air quality parameters
param = ["Carbon Monoxide", "Fine Suspended Particulates", "Nitrogen Dioxide", 
         "Nitrogen Oxides", "Ozone", "Respirable Suspended Particulates", 
         "Sulphur Dioxide"]


# Set Chrome preference
dataFolder = os.path.join(wd, "rawdata")
chromeOptions = webdriver.ChromeOptions()
prefs = {'download.default_directory': dataFolder}
chromeOptions.add_experimental_option("prefs", prefs)
chromeDriver = os.path.join(wd, "chromedriver.exe")


    

def dl_csv(station, fromYear=2016, toYear=2016):
    # Turn on driver
    driver = webdriver.Chrome(executable_path=chromeDriver, 
                              chrome_options=chromeOptions)
    
    driver.get(url)
    # Wait until the page is loaded
    wait = ui.WebDriverWait(driver, 5)
    wait.until(lambda dr: dr.find_element_by_xpath("//html").is_displayed())
    
    # Select station s
    driver.find_element_by_xpath("//a[contains(text(), '" + station + "')]").click()
    time.sleep(0.5)
    # Wait until the page is loaded
    wait = ui.WebDriverWait(driver, 5)
    wait.until(lambda dr: dr.find_element_by_xpath("//html").is_displayed())
    
    # Click all parameters
    for p in param:
        driver.find_element_by_xpath("//label[contains(text(), '" + p + "')]").click()
        time.sleep(0.5)
    
    # Click 'Hourly'
    driver.find_element_by_xpath("//label[contains(text(), 'Hourly')]").click()
    time.sleep(0.5)
    
    # Click date
    for year in range(fromYear, toYear + 1):
        date = [("form:dailyFromYear", year), 
                ("form:dailyFromMonth", 1), 
                ("form:dailyFromDay", 1), 
                ("form:dailyToYear", year)]
        if year == 2016:
            # Date updated to 2016-03-31
            date += [("form:dailyToMonth", 3), 
                     ("form:dailyToDay", 31)]
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
    
    # Take a 10 seconds break
    time.sleep(10)
    
    # Shutdown driver
    driver.quit()


dl_csv(station="MONG KOK", fromYear=1999, toYear=1999)




# Start downloading data
for s in station:
    dl_csv(station=s, fromYear=2000, toYear=2016)