import sys
import time
import datetime
import os
import ast
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from mysql_cryptomarketsdb import MySQLcryptomarketsDB
from selenium_networksetting import *
import json
import requests
import random
import subprocess


process = subprocess.Popen("whoami", stdout=subprocess.PIPE)
username, error = process.communicate()

g_sStudentNameAbbr = "sk"

# Number of webpages you want to scrape first. The total might be 400, but you may scrape the first 10
g_nTotalNumberOfPagesTobeVisited = 10
# Scraping frequency for 4 kinds of web pages
g_nScrapingFreqDaysProductDesc = 30 # days
g_nScrapingFreqDaysProductRating = 7 # days
g_nScrapingFreqDaysVendorProfile = 30 # days
g_nScrapingFreqDaysVendorRating = 7 # days
# market information
g_sMarketNameAbbr = "ap"
#http://apollonwmwenxcwa.onion/home.php
#g_sMarketURL1 = "http://apollonl43274j26.onion/login.php"
g_sMarketURL = "http://apollonl43274j26.onion/home.php"
g_nMarketGlobalID = 19
# local output data directory
g_sOutputDirectoryTemp = "/home/" + (username.strip()).decode('utf-8') + "/temp_scrapedhtml/"
# time to wait for human to input CAPTCHA
g_nTimeSecToWait = 30 * 24 * 60 * 60  # 30 days
# set it True if you want to use the default username and password
g_bUseDefaultUsernamePasswd = True
g_nUserName = "apollonabc" #other username "remember875"
g_nPassword = "King@abc"  #other password "address12&" pin 456654 halting guzzling swell succeeded connectedness
vendorList = []

#not used
class cCategoryToScrape:
    def __init__(self, sCategory = '', nPriority = 0, nFlagScrapeOrNot = 1):
        self.m_sCategory = sCategory
        self.m_nPriority = nPriority # lower integer values will be scraped first
        self.m_nFlagScrapeOrNot = nFlagScrapeOrNot # 1: need to scrape; 0: it has been scraped this week
#        category_html = [?sec_cat=56","?sec_cat=57","?sec_cat=58","?sec_cat=59","?sec_cat=60","?sec_cat=62","?sec_cat=63","?sec_cat=64","?sec_cat=65","?sec_cat=66","?sec_cat=75",]

g_vaCategoriesToScrape = [] # this list will store all the categories that will be scraped
c1='?cid=1' # Fraud
c3='?cid=3' # Guides & tutorials
c4='?cid=4' # Fakes
c5='?cid=5' # Digital Goods
c6='?cid=8' # Carded Items
c7='?cid=9' # Services
c8='?cid=10' # Software & Malware
c9='?cid=11' # Hosting & Security
c10='?cid=12' # Other
c12='?cid=2' # Drugs
#c1, c3, c4, c5, c6, c7, c8, c9, c10, c12
g_catCodes = [c6,c7,c8,c9,c10]


def captcha_login(aBrowserDriver):
    aUsernameElement = aBrowserDriver.find_element_by_name("l_username")
    aPasswordElement = aBrowserDriver.find_element_by_name("l_password")
    aBrowserDriver.find_element_by_class_name()
    aUsernameElement.send_keys(g_nUserName)
    aPasswordElement.send_keys(g_nPassword)
    aCaptchaElements = aBrowserDriver.find_elements_by_name("capt_code")
    # captcha_file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.png'
    captcha_file_name = "{}_{}.png".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), random.randint(1000, 9999))
    captcha_file_path = '/home/rob/screenshots/' + captcha_file_name
    with open(captcha_file_path, 'wb') as cp:
        cp.write(aCaptchaElements[1].screenshot_as_png)
    # Copy file to telegram system

    def getRandomString():
        return random.choice("abcdefghijklmnopqrstuvwxyz")

    captcha_IO = selenium_setup_firefox_network()
    captcha_IO.get("https://app.captchas.io/demo/index")
    while True:

        if 'Please enter your registered email' in captcha_IO.page_source:
            emailID = captcha_IO.find_element_by_id("email").send_keys(getRandomString())
            time.sleep(3)
            captcha_IO.find_element_by_name('s').click()
            time.sleep(5)
        else:
            def ubuntu_keys():
                pyautogui.press('esc')
            captcha_IO.find_element_by_xpath("//div[contains(@id,'drag_upload_file')]/p/input").click()
            ubuntu_keys()
            captcha_IO.execute_script('document.getElementById("selectfile").style.visibility="visible";')
            captcha_IO.execute_script('document.getElementById("selectfile").style.display="block";')
            captcha_IO.find_element_by_xpath('//input[@id="selectfile"]').send_keys(captcha_file_path)
            time.sleep(15)
            answer = captcha_IO.find_element_by_xpath("//b").text.strip()
            print(answer)
            captcha_IO.quit()
            break
    aCaptchaElements[0].send_keys(answer)
    aBrowserDriver.find_element_by_class_name("btn.btn-success.btn-md").click()
    if("The Captcha code you have entered is wrong" in aBrowserDriver.page_source ):
        captcha_login(aBrowserDriver)
    time.sleep(5)
    return True

def Login(aBrowserDriver):
    aBrowserDriver.get(g_sMarketURL)
    # takes you to the capture input
    print("Login page")
    aWaitNextPage = WebDriverWait(aBrowserDriver, g_nTimeSecToWait)  # Wait up to x seconds (30 days).
    # what until the currecy rate of bitcoin is clickable
    aUsernameElement = aBrowserDriver.find_element_by_name("l_username")
    aPasswordElement = aBrowserDriver.find_element_by_name("l_password")
    # aUsernameElement = aBrowserDriver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div[2]/form/fieldset/div[1]/input")
    # aPasswordElement = aBrowserDriver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div[2]/form/fieldset/div[2]/input")
    aUsernameElement.send_keys(g_nUserName)
    aPasswordElement.send_keys(g_nPassword)
    aWaitNextPage.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/nav/div/ul[1]/li[7]/a")))


def NavigateToOnePage(aBrowserDriver, sPageLink):
    # "aBrowserDriver" : web driver
    # "sPageLink" : the link of the web page
    #print("NavigateToOnePage",sPageLink)
    while True:
        aBrowserDriver.get(sPageLink)
        # Wait up to x seconds (30 days).

        # Get the page title
        sPageTitle = aBrowserDriver.title
        #new if statement aWaitNextPage.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id,'currency-rate')]")))
        #<h1 class="page-header">Login</h1>
        if '(Privoxy@localhost)' in sPageTitle:
            # 502 - No server or forwarder data received (Privoxy@localhost)
            # 503 - Forwarding failure (Privoxy@localhost)
            # 504 - Connection timeout (Privoxy@localhost)
            aWaitNextPage = WebDriverWait(aBrowserDriver, g_nTimeSecToWait)  # Wait up to x seconds (30 days).
            aWaitNextPage.until(EC.element_to_be_clickable((By.LINK_TEXT, "Privoxy")))
        elif sPageTitle == 'Login - Apollon Market':
            captcha_login(aBrowserDriver)
        else:
            aWaitNextPage = WebDriverWait(aBrowserDriver, g_nTimeSecToWait)
            aWaitNextPage.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/nav/div/ul[1]/li[7]/a")))
            break
        # Sleep for a while and then go to next page
        time.sleep(1)
        # Wait for 1 second before scraping next page.
    time.sleep(1)

# The main function, the entry point
if __name__ == '__main__':

    # query the SQL server to retrieve some basic information
    aMySQLcrptmktDB = MySQLcryptomarketsDB()
    aMySQLcrptmktDB.m_sStudentNameAbbr = g_sStudentNameAbbr
    aMySQLcrptmktDB.m_sMarketNameAbbr = g_sMarketNameAbbr
    aMySQLcrptmktDB.m_nScrapingFreqDaysProductDesc   = g_nScrapingFreqDaysProductDesc
    aMySQLcrptmktDB.m_nScrapingFreqDaysProductRating = g_nScrapingFreqDaysProductRating
    aMySQLcrptmktDB.m_nScrapingFreqDaysVendorProfile = g_nScrapingFreqDaysVendorProfile
    aMySQLcrptmktDB.m_nScrapingFreqDaysVendorRating  = g_nScrapingFreqDaysVendorRating
    # aMySQLcrptmktDB.MySQLQueryBasicInfor()
    g_nMarketGlobalID = aMySQLcrptmktDB.m_nMarketGlobalID
    if g_bUseDefaultUsernamePasswd == True:
        g_sMarketUserName = aMySQLcrptmktDB.m_sMarketUserName # this username and passwd are retrieved from DB server
        g_sMarketPassword = aMySQLcrptmktDB.m_sMarketPassword
        g_sMarketURL = "http://apollonl43274j26.onion/home.php"

    # Setup Firefox browser for visiting .onion sites through Tor (AWS proxy)
    aBrowserDriver = selenium_setup_firefox_network()
    # aBrowserDriver.set_window_rect(990, 640, 465, 560) # x,y,width,height; screen width 1853, height 1145

    # Visit the BitBazaar Market sites and Login
    # Login(aBrowserDriver)
    NavigateToOnePage(aBrowserDriver, g_sMarketURL)
    print("Login successful")

    cat_code = '?cid=1'
    sCat_Link = g_sMarketURL + cat_code
    print(cat_code)
    NavigateToOnePage(aBrowserDriver, sCat_Link)
    # Storing all the page URLs
    AllPages = aBrowserDriver.find_elements_by_class_name("page-link")
    APLinks = []
    for i in AllPages:
        sProductHref = i.get_attribute("href")
        if sProductHref not in APLinks:
            APLinks.append(sProductHref)
    #print(APLinks[-1][APLinks[-1].find("&pg=")+4:])

    vAllPageLinks = []
    # Scrape Starts from this page
    maxIndexofPage = int(APLinks[-1][APLinks[-1].find("&pg=")+4:])
    nIdxOfPage = 1
    for i in range(nIdxOfPage, maxIndexofPage + 1):
        # the string should look like
        #http://apollonwmwenxcwa.onion/home.php?cid=2&pg=1982
        sOnePageLink = sCat_Link + "&pg=" + str(i)
        if sOnePageLink not in vAllPageLinks:
            vAllPageLinks.append(sOnePageLink)
    print("Total number of pages: %d" % maxIndexofPage)

    for sOnePageLink in vAllPageLinks:
        nPageIndex = nIdxOfPage
        nIdxOfPage += 1
        print("page %d" % nPageIndex)
        NavigateToOnePage(aBrowserDriver, sOnePageLink)

        # For each product in this page, insert them into the list of all products.
        #<a href="listing.php?ls_id=20560">
        vElementsProducts = aBrowserDriver.find_elements_by_xpath("//a[contains(@href,'listing.php?ls_id=')]")
        vAllProductsInThisPage = []
        for aElementOneProduct in vElementsProducts:
            sProductHref = aElementOneProduct.get_attribute("href")
            if sProductHref not in vAllProductsInThisPage:
                vAllProductsInThisPage.append(sProductHref)
                #print(sProductHref)

        # For each vendor in this page, insert them into the list of all vendors.
        #<a href="user.php?u_id=SteroidWarehouse">
        vElementsVendors = aBrowserDriver.find_elements_by_xpath("//a[contains(@href,'user.php?u_id=')]")
        vAllVendorsInThisPage = []
        for aElementOneVendor in vElementsVendors:
            sVendorHref = aElementOneVendor.get_attribute("href")
            if sVendorHref not in vAllVendorsInThisPage:
                vAllVendorsInThisPage.append(sVendorHref)
                #print(sVendorHref)

        # 1. Scrape the product information
        for sProductHref in vAllProductsInThisPage:
            sProductMarketID = sProductHref.partition('ls_id=')[2]
            #print(sProductMarketID)
            # bWhetherScraping = aMySQLcrptmktDB.CheckWhetherScrapingProductDescription(sProductMarketID)
            bWhetherScraping = True
            if bWhetherScraping:

                NavigateToOnePage(aBrowserDriver, sProductHref)
                # Save the html
                sCurrentUTCTime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
                aMySQLcrptmktDB.m_sCurrentUTCTime = sCurrentUTCTime
                sLocalOutputFileName = sCurrentUTCTime + '_' + str(g_nMarketGlobalID).zfill(
                    2) + '_' + sProductMarketID + '_pd'
                sLocalOutputFileNameFullPath = g_sOutputDirectoryTemp + sLocalOutputFileName
                # Get screen shot of Product Description
                #aBrowserDriver.get_screenshot_as_file(sLocalOutputFileNameFullPath + "_img.png")
                aFile = open(sLocalOutputFileNameFullPath, "w")
                aFile.write(aBrowserDriver.page_source)
                aFile.close()
                # aMySQLcrptmktDB.UpdateDatabaseUploadFileProductDescription(sLocalOutputFileName,
                #                                                            sLocalOutputFileNameFullPath,
                #                                                            sProductMarketID)
                os.remove(sLocalOutputFileNameFullPath)


            ## scraping product ratings.
            # bWhetherScraping = aMySQLcrptmktDB.CheckWhetherScrapingProductRating(sProductMarketID)
            bWhetherScraping = True
            if bWhetherScraping:
                NavigateToOnePage(aBrowserDriver, sProductHref)
                sElementProductFeedback = aBrowserDriver.find_element_by_xpath("//a[contains(@href,'&tab=4')]")
                sProductFeedbackHref = sElementProductFeedback.get_attribute("href")
                NavigateToOnePage(aBrowserDriver, sProductFeedbackHref)

                paginationRow = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")
                if len(paginationRow) == 0:
                    continue
                lastPageNumber = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")[-1].find_element_by_xpath("a").get_attribute("href").split("=")[-1]
                for page in range(1,int(lastPageNumber)+1):
                    productFeedbackPageLink = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")[-1].find_element_by_xpath("a").get_attribute("href").partition("pg=")[0]+"pg="+str(page)
                    NavigateToOnePage(aBrowserDriver, productFeedbackPageLink)
                    sCurrentUTCTime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
                    aMySQLcrptmktDB.m_sCurrentUTCTime = sCurrentUTCTime
                    sLocalOutputFileName = sCurrentUTCTime + '_' + str(g_nMarketGlobalID).zfill(
                        2) + '_' + sProductMarketID + '_pr_'+ str(page)
                    sLocalOutputFileNameFullPath = g_sOutputDirectoryTemp + sLocalOutputFileName
                    aFile = open(sLocalOutputFileNameFullPath, "w")
                    aFile.write(aBrowserDriver.page_source)
                    aFile.close()
                    # aMySQLcrptmktDB.UpdateDatabaseUploadFileProductRating(sLocalOutputFileName,
                    #                                                       sLocalOutputFileNameFullPath,
                    #                                                       sProductMarketID)
                    os.remove(sLocalOutputFileNameFullPath)

        print("Products %d" % len(vAllProductsInThisPage))


        # 1. Scrape the vendor profile page
        for sVendorHref in vAllVendorsInThisPage:
            sVendorMarketID = sVendorHref.partition('id=')[2]
            NavigateToOnePage(aBrowserDriver, str(sVendorHref))
            #print(sVendorMarketID)
            # bWhetherScraping = aMySQLcrptmktDB.CheckWhetherScrapingVendorProfile(sVendorMarketID)
            bWhetherScraping = True
            if bWhetherScraping:

                sCurrentUTCTime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
                aMySQLcrptmktDB.m_sCurrentUTCTime = sCurrentUTCTime
                sLocalOutputFileName = sCurrentUTCTime + '_' + str(g_nMarketGlobalID).zfill(
                    2) + '_' + sVendorMarketID + '_vp'
                sLocalOutputFileNameFullPath = g_sOutputDirectoryTemp + sLocalOutputFileName
                # Save the html
                aFile = open(sLocalOutputFileNameFullPath, "w")
                aFile.write(aBrowserDriver.page_source)
                aFile.close()

                ## Scraping PGP key file.
                pgpTabHref = aBrowserDriver.find_element_by_xpath("//a[contains(@href,'&tab=6')]").get_attribute("href")
                NavigateToOnePage(aBrowserDriver, pgpTabHref)
                sLocalOutputFileNamePGP = sCurrentUTCTime + '_' + str(g_nMarketGlobalID).zfill(
                    2) + '_' + sVendorMarketID + '_vp_pgp'
                sLocalOutputFileNamePGPFullPath = g_sOutputDirectoryTemp + sLocalOutputFileNamePGP
                ## saving PGP file.
                aFile = open(sLocalOutputFileNamePGPFullPath, "w")
                aFile.write(aBrowserDriver.page_source)
                aFile.close()

                ## Moving pgp file to jaguar and removing local files.
                sSCP_Command = 'sshpass -p \'' + aMySQLcrptmktDB.m_sServerPasswd + '\' scp ' + sLocalOutputFileNamePGPFullPath + ' ' + \
                    aMySQLcrptmktDB.m_sServerUser + '@' + aMySQLcrptmktDB.m_sServerHost + ':' + aMySQLcrptmktDB.m_sRemoteRootDirectoryVendorProfile
                # os.system(sSCP_Command)
                sCommandRemoveLocalFilesPGP = 'rm ' + sLocalOutputFileNamePGPFullPath
                os.system(sCommandRemoveLocalFilesPGP)

                # Move file to server, and update the sql database
                # aMySQLcrptmktDB.UpdateDatabaseUploadFileVendorProfile(sLocalOutputFileName,
                #                                                       sLocalOutputFileNameFullPath, sVendorMarketID)
                sCommandRemoveLocalfiles = 'rm ' + sLocalOutputFileNameFullPath
                os.system(sCommandRemoveLocalfiles)

            # scrape vendors positive feedback
            # bWhetherScraping = aMySQLcrptmktDB.CheckWhetherScrapingVendorRating(sVendorMarketID)
            bWhetherScraping = True
            if bWhetherScraping:
                NavigateToOnePage(aBrowserDriver, sVendorHref)
                aBrowserDriver.find_elements_by_xpath("//li")[26].click()
                paginationRow = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")
                if len(paginationRow) != 0:
                    lastPageNumber = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")[
                        -1].find_element_by_xpath("a").get_attribute("href").split("=")[-1]
                    for page in range(1, int(lastPageNumber) + 1):
                        vendorFeedbackPageLink = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")[-1].find_element_by_xpath("a").get_attribute("href").partition("pg=")[0]+"pg="+str(page)
                        NavigateToOnePage(aBrowserDriver, vendorFeedbackPageLink)
                        sCurrentUTCTime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
                        aMySQLcrptmktDB.m_sCurrentUTCTime = sCurrentUTCTime
                        sLocalOutputFileName = sCurrentUTCTime + '_' + str(g_nMarketGlobalID).zfill(
                            2) + '_' + sVendorMarketID + '_vr_positive_' + str(page)
                        sLocalOutputFileNameFullPath = g_sOutputDirectoryTemp + sLocalOutputFileName
                        aFile = open(sLocalOutputFileNameFullPath, "w")
                        aFile.write(aBrowserDriver.page_source)
                        aFile.close()
                        # aMySQLcrptmktDB.UpdateDatabaseUploadFileVendorRating(sLocalOutputFileName,
                        #                                                      sLocalOutputFileNameFullPath,
                        #                                                      sVendorMarketID)
                        sCommandRemoveLocalfiles = 'rm ' + sLocalOutputFileNameFullPath
                        os.system(sCommandRemoveLocalfiles)

                # scrape vendors neutral feedback
                aBrowserDriver.find_elements_by_xpath("//li")[27].click()
                paginationRow = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")
                if len(paginationRow) != 0:
                    lastPageNumber = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")[
                        -1].find_element_by_xpath("a").get_attribute("href").split("=")[-1]
                    for page in range(1, int(lastPageNumber) + 1):
                        vendorFeedbackPageLink = \
                        aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")[
                            -1].find_element_by_xpath("a").get_attribute("href").partition("pg=")[0] + "pg=" + str(page)
                        NavigateToOnePage(aBrowserDriver, vendorFeedbackPageLink)
                        sCurrentUTCTime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
                        aMySQLcrptmktDB.m_sCurrentUTCTime = sCurrentUTCTime
                        sLocalOutputFileName = sCurrentUTCTime + '_' + str(g_nMarketGlobalID).zfill(
                            2) + '_' + sVendorMarketID + '_vr_neutral_' + str(page)
                        sLocalOutputFileNameFullPath = g_sOutputDirectoryTemp + sLocalOutputFileName
                        aFile = open(sLocalOutputFileNameFullPath, "w")
                        aFile.write(aBrowserDriver.page_source)
                        aFile.close()
                        # aMySQLcrptmktDB.UpdateDatabaseUploadFileVendorRating(sLocalOutputFileName,
                        #                                                      sLocalOutputFileNameFullPath,
                        #                                                      sVendorMarketID)
                        sCommandRemoveLocalfiles = 'rm ' + sLocalOutputFileNameFullPath
                        os.system(sCommandRemoveLocalfiles)

                # scrape vendors negative feedback
                aBrowserDriver.find_elements_by_xpath("//li")[28].click()
                paginationRow = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")
                if len(paginationRow) != 0:
                    lastPageNumber = aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")[
                        -1].find_element_by_xpath("a").get_attribute("href").split("=")[-1]
                    for page in range(1, int(lastPageNumber) + 1):
                        vendorFeedbackPageLink = \
                            aBrowserDriver.find_elements_by_xpath("//li[contains(@class,'page-item')]")[
                                -1].find_element_by_xpath("a").get_attribute("href").partition("pg=")[
                                0] + "pg=" + str(page)
                        NavigateToOnePage(aBrowserDriver, vendorFeedbackPageLink)
                        sCurrentUTCTime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
                        aMySQLcrptmktDB.m_sCurrentUTCTime = sCurrentUTCTime
                        sLocalOutputFileName = sCurrentUTCTime + '_' + str(g_nMarketGlobalID).zfill(
                            2) + '_' + sVendorMarketID + '_vr_negative_' + str(page)
                        sLocalOutputFileNameFullPath = g_sOutputDirectoryTemp + sLocalOutputFileName
                        aFile = open(sLocalOutputFileNameFullPath, "w")
                        aFile.write(aBrowserDriver.page_source)
                        aFile.close()
                        # aMySQLcrptmktDB.UpdateDatabaseUploadFileVendorRating(sLocalOutputFileName,
                        #                                                      sLocalOutputFileNameFullPath,
                        #                                                      sVendorMarketID)
                        sCommandRemoveLocalfiles = 'rm ' + sLocalOutputFileNameFullPath
                        os.system(sCommandRemoveLocalfiles)


        print("Vendors %d" % len(vAllVendorsInThisPage))



    print("All jobs are done! Thanks for nothing!")
    time.sleep(10)
    aBrowserDriver.quit()
