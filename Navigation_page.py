from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import Global_var
from Insert_On_Datbase import insert_in_Local,create_filename
import sys, os
import ctypes
import string
import requests
import urllib.request
import urllib.parse
import re


def ChromeDriver():
    File_Location = open("D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\scop.oil.gov.iq\\Location For Database & Driver.txt", "r")
    TXT_File_AllText = File_Location.read()
    Chromedriver = str(TXT_File_AllText).partition("Driver=")[2].partition("\")")[0].strip()
    # chrome_options = Options()
    # chrome_options.add_extension('D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\scop.oil.gov.iq\\Browsec-VPN.crx')  # ADD EXTENSION Browsec-VPN
    # browser = webdriver.Chrome(executable_path=str(Chromedriver),
    #                            chrome_options=chrome_options)
    browser = webdriver.Chrome(executable_path=str(Chromedriver))
    browser.get(
        """https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    for Add_Extension in browser.find_elements_by_xpath('/html/body/div[4]/div[2]/div/div/div[2]/div[2]/div'):
        Add_Extension.click()
        break
    import wx
    app = wx.App()
    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 30 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(30)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    browser.get("http://www.scop.oil.gov.iq/index.php?name=monaksa")
    browser.set_window_size(1024, 600)
    browser.maximize_window()
    # browser.switch_to.window(browser.window_handles[1])
    # browser.close()
    # browser.switch_to.window(browser.window_handles[0])
    # time.sleep(2)
    time.sleep(1)
    #     time.sleep(20)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    # browser.get('http://www.scop.oil.gov.iq/index.php?name=monaksa')

    # browser.set_window_size(1024 , 600)
    # browser.maximize_window()
    # browser.switch_to.window(browser.window_handles[1])
    # browser.close()
    # browser.switch_to.window(browser.window_handles[0])

    for Search_button in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/center[1]/input'):
        Search_button.click()
        break
    a = True
    while a == True:
        try:
            Tender_href = []
            for Search_icon in range(2, 60, 1):
                xpath_date = "/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[" + str(Search_icon) + "]/td[5]/center"
                for publish_date in browser.find_elements_by_xpath(str(xpath_date)):
                    pubdate = publish_date.get_attribute("innerText").strip()
                    a = False
                    if pubdate == "":
                        Scrap_data(browser, Tender_href)
                        print("Tender Date Dead")
                        a = False
                    else:
                        datetime_object = datetime.strptime(pubdate, '%Y-%m-%d')
                        publish_date1 = datetime_object.strftime("%Y-%m-%d")
                        if publish_date1 >= Global_var.From_Date:
                            for search_icon_href in browser.find_elements_by_xpath("/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[" + str(Search_icon) + "]/td[8]/a"):
                                Tender_href.append(search_icon_href.get_attribute('href'))
                        else:
                            print("Tender Date Dead")
                            Scrap_data(browser, Tender_href)
                            a = False

            Scrap_data(browser, Tender_href)
        except Exception as e:
            print(e)
            a = True


def Translate(text_without_translate):
    String2 = ""
    try:
        String2 = str(text_without_translate)
        url = "https://translate.google.com/m?hl=en&sl=auto&tl=en&ie=UTF-8&prev=_m&q=" + str(String2) + ""
        response1 = requests.get(str(url))
        response2 = response1.url
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        headers = {'User-Agent': user_agent , }
        request = urllib.request.Request(response2 , None , headers)  # The assembled request
        time.sleep(2)
        response = urllib.request.urlopen(request)
        htmldata: str = response.read().decode('utf-8')
        trans_data = re.search(r'(?<=dir="ltr" class="t0">).*?(?=</div>)' , htmldata).group(0)
        return trans_data
    except:
        return String2


def Scrap_data(browser, Tender_href):

    a = True
    while a == True:
        try:
            for href in Tender_href:
                browser.get(href)
                Global_var.Total += 1
                SegFeild = []
                for data in range(42):
                    SegFeild.append('')

                get_htmlSource = ""
                for outerHTML in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td/center'):
                    get_htmlSource = outerHTML.get_attribute('outerHTML')
                    get_htmlSource = get_htmlSource.replace('href="upload/', 'href="http://www.scop.oil.gov.iq/upload/')
                    break

                # Purchaser
                for Name_of_Directorate in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[2]/td[2]'):
                    Name_of_Directorate = Name_of_Directorate.get_attribute('innerText').replace('&nbsp;', '').strip()
                    Name_of_Directorate = Translate(Name_of_Directorate)
                    SegFeild[12] = Name_of_Directorate.strip().upper()
                    break

                # Title
                for Tender_Subject in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[3]/td[2]'):
                    Tender_Subject = Tender_Subject.get_attribute('innerText').replace('&nbsp;', '').strip()
                    Tender_Subject = Translate(Tender_Subject)
                    Tender_Subject = string.capwords(str(Tender_Subject))
                    SegFeild[19] = Tender_Subject
                    break

                # Email
                for Email in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[4]/td[2]/div'):
                    Email = Email.get_attribute('innerText').replace('&nbsp;', '').strip()
                    SegFeild[1] = Email.strip()
                    break

                # tender NO
                for Bid_number in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[5]/td[2]'):
                    Bid_number = Bid_number.get_attribute('innerText').replace('&nbsp;', '').strip()
                    SegFeild[13] = Bid_number.strip()
                    break

                # Release Date
                Release_Date = ""
                for Release_Date in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[6]/td[2]'):
                    Release_Date = Release_Date.get_attribute('innerText').replace('&nbsp;', '').strip()
                    break

                # Extention Date
                Extention_Date = ""
                for Extention_Date in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[8]/td[2]'):
                    Extention_Date = Extention_Date.get_attribute('innerText').replace('&nbsp;', '').strip()
                    Extention_Date = Translate(Extention_Date)
                    if Extention_Date == "Extension does not have":
                        Extention_Date = "Extension does not have"
                    else:pass
                    break

                # Document

                for Attachment in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[9]/td[2]'):
                    Attachment = Attachment.get_attribute('outerHTML').replace('مرفق رقم','Attachment ').replace('href="upload/', 'href="http://www.scop.oil.gov.iq/upload/')
                    SegFeild[5] = Attachment
                    break

                # Close Date
                try:
                    for Close_Date in browser.find_elements_by_xpath('/html/body/div[2]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[7]/td[2]'):
                        Close_Date = Close_Date.get_attribute('innerText').replace('&nbsp;', '').strip()
                        datetime_object = datetime.strptime(Close_Date, "%Y-%m-%d")
                        mydate = datetime_object.strftime("%Y-%m-%d")
                        SegFeild[24] = mydate
                except:
                    SegFeild[24] = ""

                SegFeild[18] = "Subject: " + str(SegFeild[19]) + "<br>\n""Directorate_Name: " + str(SegFeild[12]) + "<br>\n""Release Date: " + str(Release_Date) + "<br>\n""Extention Date: " + str(Extention_Date) + "<br>\n""Close Date: " + str(SegFeild[24])

                SegFeild[7] = "IQ"

                SegFeild[2] = "Oil Complex Building, Port Said Street, P.O. Box 198, Baghdad, Iraq <br>\n Tel : +964 1 817 7000 <br>\n Fax : +964 1 876 3744"

                SegFeild[1] = 'info@scop.oil.gov.iq'

                # notice type
                SegFeild[14] = "2"

                SegFeild[22] = "0"

                SegFeild[26] = "0.0"

                SegFeild[27] = "0"  # Financier

                SegFeild[28] = str(href)

                # Source Name
                SegFeild[31] = 'scop.oil.gov.iq'

                for Segdata in range(len(SegFeild)):
                    print(Segdata, end=' ')
                    print(SegFeild[Segdata])
                    SegFeild = [SegFeild.replace("&quot;", "\"") for SegFeild in SegFeild]
                    SegFeild = [SegFeild.replace("&QUOT;", "\"") for SegFeild in SegFeild]
                    SegFeild = [SegFeild.replace("&nbsp;", " ") for SegFeild in SegFeild]
                    SegFeild = [SegFeild.replace("&NBSP;", " ") for SegFeild in SegFeild]
                    SegFeild = [SegFeild.replace("&amp;amp", "&") for SegFeild in SegFeild]
                    SegFeild = [SegFeild.replace("&AMP;AMP", "&") for SegFeild in SegFeild]
                    SegFeild = [SegFeild.replace("&amp;", "&") for SegFeild in SegFeild]
                    SegFeild = [SegFeild.replace("&AMP;", "&") for SegFeild in SegFeild]
                a = False
                check_date(get_htmlSource, SegFeild)
                print(" Total: " + str(Global_var.Total) + " Duplicate: " + str(
            Global_var.duplicate) + " Expired: " + str(Global_var.expired) + " Inserted: " + str(
            Global_var.inserted) + " Skipped: " + str(
            Global_var.skipped) + " Deadline Not given: " + str(
            Global_var.deadline_Not_given) + " QC Tenders: " + str(Global_var.QC_Tender),'\n')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n", exc_tb.tb_lineno)
            a = True
        ctypes.windll.user32.MessageBoxW(0, "Total: " + str(Global_var.Total) + "\n""Duplicate: " + str(
            Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(
            Global_var.inserted) + "\n""Skipped: " + str(
            Global_var.skipped) + "\n""Deadline Not given: " + str(
            Global_var.deadline_Not_given) + "\n""QC Tenders: " + str(Global_var.QC_Tender) + "",
                                         "scop.oil.gov.iq", 1)
        Global_var.Process_End()
        browser.close()
        sys.exit()


def check_date(get_htmlSource, SegFeild):
    tender_date = str(SegFeild[24])
    nowdate = datetime.now()
    date2 = nowdate.strftime("%Y-%m-%d")
    try:
        if tender_date != '':
            deadline = time.strptime(tender_date , "%Y-%m-%d")
            currentdate = time.strptime(date2 , "%Y-%m-%d")
            if deadline > currentdate:
                insert_in_Local(get_htmlSource, SegFeild)
            else:
                print("Tender Expired")
                Global_var.expired += 1
        else:
            print("Deadline was not given")
            Global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" , exc_tb.tb_lineno)


ChromeDriver()