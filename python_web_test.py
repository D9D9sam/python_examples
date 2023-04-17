from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def clear(element):
    value = element.get_attribute('value')
    if len(value) > 0:
        for char in value:
            element.send_keys(Keys.BACK_SPACE)

start_time = time.time()

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://qaschool.bia-tech.ru/otborochnoe-zadanie/')

entr_button = driver.find_element(By.LINK_TEXT, 'Вход')
entr_button.click()

login_field = driver.find_element(By.NAME, 'login')
login_field.send_keys('ТВОЙ_ЛОГИН')
time.sleep(1)
password_field = driver.find_element(By.NAME, 'password')
password_field.send_keys('ТВОЙ_ПАРОЛЬ')
time.sleep(5)

fio_field = driver.find_element(By.NAME, 'name')
date_field = driver.find_element(By.NAME, 'age')
phone_field = driver.find_element(By.NAME, 'phone')
email_field = driver.find_element(By.NAME, 'email')
reg_button = driver.find_element(By.LINK_TEXT, 'Зарегистрироваться')

fio_list = [
            'Демидов Алексей Евгеньевич',
            'Демидов',
            'д',
            'Demidov Aleksey Evgenevich',
            'Demidov',
            'D3m1d()v Al3ks*_ 3\/gen3&><',
            '123 567 890',
            'Дем И' + 99 * 'и' + ' Дов',
            '<blink>Hello there</blink>',
            ' ',
            '']

date_list = ['27.08.1990',
             '08.27.1990',
             '1990.08.27',
             '27.08.199',
             '7.8.1990',
             '27081990',
             '27 августа 1990 г.',
             '30.02.1990',
             '01.01.1900',
             '01.01.3000',
             'ab/#$.@0/',
             '<blink>Hello there</blink>',
             '9' + 101 * '8',
             ' ',
             '']

phone_list = ['9115553377',
              '+79115553377',
              '89115553377',
              '911555337',
              '(911)555-77-77',
              '0000000000',
              '!@#$%^&*()',
              '+7(911) 555-33-77',
              'Номер теле',
              'Number pho',
              '<blink>Hello there</blink>',
              ' ',
              '']

email_list = ['test@gmail.com',
              'test@@gmail...com',
              'testgmail.com',
              'test@gmailcom',
              't1!_t@gmail.com',
              'TEST@gmail.COM',
              'тест@джимейл.рф',
              'text@text.text',
              'текст@текст.текст',
              99 * 't' + '@gmail.com',
              '<blink>Hello there</blink>',
              ' ',
              '']

for i in fio_list:
#    time.sleep(1)
    fio_field.send_keys(i)

    for j in date_list:
#        time.sleep(1)
        date_field.send_keys(j)

        for k in phone_list:
#            time.sleep(1)
            phone_field.send_keys(k)

            for l in email_list:
#                time.sleep(1)
                email_field.send_keys(l)

                reg_button.click()

                clear(email_field)
            clear(phone_field)
        clear(date_field)
    clear(fio_field)

print("--- %s seconds ---" % int(time.time() - start_time))