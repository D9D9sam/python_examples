from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

def clear(element):
    value = element.get_attribute('value')
    if len(value) > 0:
        for char in value:
            element.send_keys(Keys.BACK_SPACE)

data = [[3, 4, 5],
        [3, 3, 3],
        [3, 5, 3],
        [0, 0, 0],
        [-1, -1, -1],
        ['a', '+', 'c']]

driver = webdriver.Chrome()
driver.get('https://playground.learnqa.ru/puzzle/triangle')
driver.maximize_window()
driver.execute_script("window.scrollTo(0, 1000)")

sleep(5)        # В будущем нужно заменить стратегию ожидания прогрузки кнопки

button_show = driver.find_element(By.XPATH, '//*[@id="puzzle"]/div[2]/div[2]/div[6]/button[1]')

side_a = driver.find_element(By.CLASS_NAME, 'js_a')
side_b = driver.find_element(By.CLASS_NAME, 'js_b')
side_c = driver.find_element(By.CLASS_NAME, 'js_c')

button_show.click()
sleep(1)

for i in range(len(data)):
    side_a.send_keys(data[i][0])
    side_b.send_keys(data[i][1])
    side_c.send_keys(data[i][2])
    button_show.click()
    sleep(1)
    clear(side_a)
    clear(side_b)
    clear(side_c)

sleep(5)