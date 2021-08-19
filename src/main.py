from datetime import datetime,date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.action_chains  import ActionChains
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from selenium.webdriver.support.ui import Select
import sqlite3
import os
from pathlib import Path
import ann

URL = "https://www.dofus.com/fr/achat-kamas/cours-kama-ogrines"
DB_NAME = os.path.abspath(os.path.expanduser("mainDB.db"))

def scrap_data(last_date: datetime) -> 'dict[datetime,float]':
    result = {}
    options = webdriver.chrome.options.Options()
    #options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=options)
    driver.get(URL)
    time.sleep(2)
    driver.find_element_by_xpath('//button[normalize-space()="tout refuser"]').click()
    chartElements = driver.find_elements_by_class_name('highcharts-container')
    for elt in chartElements:
        print(elt.text)

    select = Select(driver.find_element_by_name("rates_period"))
    select.select_by_value("3months")
    time.sleep(2)

    chart_legend_split = driver.find_elements_by_class_name("highcharts-legend-item")

    ## Print the legend useless here
    #for legend_item in chart_legend_split:
    #    print(legend_item)
    #    print(legend_item.find_element_by_tag_name('text').text)
    
    # C'est le cours moyen pour le faire disparaître
    chart_legend_split[0].click()

    highcharts_markers = driver.find_elements_by_class_name("highcharts-markers")
    #print(len(highcharts_markers)) Il y en a 2 sûrement pour les deux séries
    
    for serie in highcharts_markers[1:]:
        # On cherche les markers et pour chaque on place le curseur dessus pour afficher le tooltip dont on récupère les valeurs
        for marker in serie.find_elements_by_tag_name("path"):
            hover = ActionChains(driver).move_to_element(marker)
            hover.perform()
            time.sleep(0.001)
            a = driver.find_elements_by_class_name("highcharts-tooltip")
            for elt in a:
                b = elt.find_element_by_tag_name("text")
                print(b.text)
                c = b.text.split()
                try:
                    date = datetime.strptime(c[2],"%d/%m/%Y")
                    if date > last_date:
                        result[date] = float(c[5])
                    else:
                        break
                except IndexError as e:
                    print(e)
                    print(c)
    driver.close()
    #print(f"Result :\n{result}")
    return result


def analyse(data: 'dict[datetime,float]') -> None:
    fig, axs = plt.subplots(3)
    sorted_dict = {k: v for k, v in sorted(data.items(), key=lambda item: item[0])}
    # x = []
    # y = []
    # mi = min([datetime.timestamp(k) for k in data.keys()])
    # for k,v in sorted(data.items()):
    #     for i in range(24):
    #         x.append(datetime.timestamp(k) + i*3600 - mi)
    #         y.append(v)
    x = list([datetime.timestamp(x) for x in sorted_dict.keys()])
    y  = list(sorted_dict.values())
    #x = np.linspace(0,10,10000)
    #y = [np.sin(2*np.pi*25*t) for t in x]
    axs[0].plot(x,y)

    xf = fftfreq(len(x), x[1]-x[0])
    yf  = fft(y)
    m = max(yf)
    yf = [y for x,y in zip(xf,yf) if x > 0]
    xf = [x for x in xf if x > 0]
    axs[1].plot(xf,yf)

    # x2 = np.linspace(min(x),max(x),10000)
    # print([(x,y.real) for x,y in zip(xf,yf) if abs(y)>150 and x>0])
    # y2 = [sum([y.real*np.sin(2*np.pi*x*t) for x,y in zip(xf,yf) if y > 1 and x > 0]) for t in x2]

    # axs[2].plot(x2,y2)


    plt.show()

def save_data_databse(cur: sqlite3.Cursor, data: 'dict[datetime,float]') -> None:
    
    for key,value in data.items():
        print(f"INSERT INTO stocks VALUES {(str(key),value)};")
        cur.execute(f"INSERT INTO daily VALUES {(str(key),value)};")

def get_last_record_date(cur: sqlite3.Cursor) -> datetime:
    request = "SELECT max(date) FROM daily;"
    cur.execute(request)
    res = cur.fetchall()
    return datetime.strptime(res[0][0],"%Y-%m-%d %H:%M:%S")

def get_records_from_database(cur: sqlite3.Cursor, start=date(2000, 1, 1), stop=datetime.now()):
    request = f"SELECT * FROM daily WHERE date < '{stop}' AND date > '{start}';"
    print(request)
    cur.execute(request)
    res = {}
    for elt in cur.fetchall():
        res[datetime.strptime(elt[0],"%Y-%m-%d %H:%M:%S")]= elt[1]
    return res

def main() -> None:
    db_exists= False
    if os.path.isfile(DB_NAME):
        db_exists = True
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    if not db_exists:
        cur.execute('''CREATE TABLE daily
               (date text, rate real)''')

    # last_date = get_last_record_date(cur)
    # result = scrap_data(last_date)
    # save_data_databse(cur,result)
    # con.commit()


    
    records = get_records_from_database(cur)
    #analyse(records)
    y = list(records.values())
    print(len(y))
    x_data = [y[i:i+10] for i in range(0,len(y)-10)]
    print(x_data[-1])
    ann.func(x_data,y[10:len(y)],75)
    con.commit()
    con.close()

if __name__ == "__main__":
    main()