from django.shortcuts import render, redirect
import os
from .forms import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from bestinstaday.settings import BASE_DIR

from bs4 import BeautifulSoup
from numerize import numerize
import json
import pickle
import numpy as np


def getInfo(profile):
    
    path_bin = os.environ.get("GOOGLE_CHROME_BIN")
    path = os.environ.get("CHROMEDRIVER_PATH")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = path_bin
   
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    #service = Service(executable_path=path)
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)
    page = driver.get("https://www.instagram.com/")
    
    try:
        wait = WebDriverWait(driver, 10, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        res = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
        inputs = True

    except:
        inputs = False
        driver.refresh()

    if inputs == True:
        username=driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        username.clear()
        username.send_keys("bestinstaday")
    
        pwd=driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        pwd.clear()
        pwd.send_keys("PASSWORD")
    
        login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", login)
        try:
            wait = WebDriverWait(driver, 10, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
            res = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='sqdOP  L3NKy   y3zKF     ']")))
            btn = True

        except:
            btn = False
            driver.refresh()
    
        if btn == True:
            btn = driver.find_element(By.CSS_SELECTOR, "button[class='sqdOP  L3NKy   y3zKF     ']")
            driver.execute_script("arguments[0].click();", btn)
        
            page = driver.get("https://www.instagram.com/{}/?__a=1".format(profile))
        
            soup = BeautifulSoup(driver.page_source, "html.parser").get_text()
            try:
                data = json.loads(soup)
                followers = int(data["graphql"]["user"]["edge_followed_by"]["count"])
                posts = int(data["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])
                driver.close()
                driver.quit()
                return posts, followers
            
            except:
                driver.close()
                driver.quit()
                return -1
        
        else:
            driver.close()
            driver.quit()
            return -1
    
    else:
        driver.close()
        driver.quit()
        return -1



def predict_engagement(posts, followers):

    scaler_path = os.path.join(BASE_DIR, "scaler.p")
    model_path = os.path.join(BASE_DIR, "best_model.p")

    scaler = pickle.load(open(scaler_path, 'rb'))
    loaded_model = pickle.load(open(model_path, 'rb'))

    days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"} 
    
    engegments = {}
    best_post_per_week = 1
    best_eng = 0
    for post_per_week in range(1, 8):
        for day in range(1, 8):
            for hour in range(24):
                X0 = np.array([[posts, followers, hour, day, float(post_per_week)/7]])
                X0 = scaler.transform(X0)
                eng_pred = loaded_model["model"].predict(X0)[0]
                
                if post_per_week in engegments.keys():
                    engegments[post_per_week][(day, hour)] = eng_pred
                else:
                    engegments[post_per_week] = {(day, hour): eng_pred}
                
                if eng_pred > best_eng:
                    best_eng = eng_pred
                    best_post_per_week = post_per_week
    
    
    engegments = engegments[best_post_per_week]
        
    engegments = dict(sorted(engegments.items(), key=lambda item: item[1], reverse=True))
    engegments = list(engegments.items())[:5]
    engegments = [(days[v[0][0]], v[0][1], round(v[1],2)) for v in engegments]
    
    return best_post_per_week, engegments



# Create your views here.
def home(request):

    form = AnalyzeForm()
    section = ''
    if request.method == 'POST':

        if 'search' in request.POST.keys():
            section = 'predict'

            analyzeData = AnalyzeForm(request.POST)
            form = AnalyzeForm(request.POST)
            
            if analyzeData.is_valid():
                username = analyzeData.cleaned_data["search"]
                username = username.lower()
                data = getInfo(username)

                if data != -1:
                    posts, followers = data
                    nb_posts_per_week, predicted_data = predict_engagement(posts, followers)
                    data = numerize.numerize(followers), numerize.numerize(posts)

                    context = {
                        'form': form,
                        'username': username,
                        'data': data,
                        'posts_per_week': nb_posts_per_week,
                        'predicted_data': predicted_data,
                        'section': section
                    }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                    return render(request, "index.html", context)

    return render(request, "index.html", {'form': form, 'section': section})
