import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import settings


url = 'https://lk.rt.ru/'


@pytest.fixture(autouse=True)
def driver():
    service = webdriver.ChromeService(executable_path="./webdrv/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.set_window_size(1600,900)
    driver.get(f'{url}')

    yield driver

    driver.quit()


def test_load_page_auth_by_code(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'section#page-right .card-container')))
    
    curr_url = driver.current_url

    assert curr_url.split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth'
    
    header_obj = driver.find_elements(By.CSS_SELECTOR, 'header#app-header path')

    assert len(header_obj) == 12

    left_obj = driver.find_element(By.CSS_SELECTOR, 'section#page-left .what-is-container')

    assert left_obj.find_element(By.TAG_NAME, 'h2').text == 'Личный кабинет'
    assert left_obj.find_element(By.TAG_NAME, 'p').text == 'Персональный помощник в цифровом мире Ростелекома'

    right_obj = driver.find_element(By.CSS_SELECTOR, 'section#page-right .card-container')

    assert right_obj.find_element(By.ID, 'card-title').text == 'Авторизация по коду'
    assert right_obj.find_element(By.CSS_SELECTOR, 'p#card-description').text == 'Укажите почту или номер телефона, на которые необходимо отправить код подтверждения'
    assert right_obj.find_element(By.CSS_SELECTOR, 'input#address').get_attribute('type') == 'text'
    assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'E-mail или мобильный телефон'
    assert right_obj.find_element(By.CSS_SELECTOR, 'button#otp_get_code').text == 'Получить код'
    assert right_obj.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').text == 'Войти с паролем'
    assert right_obj.find_element(By.CSS_SELECTOR, 'div.auth-policy span').text == 'Нажимая кнопку «Получить код», вы принимаете условия'
    assert right_obj.find_element(By.ID, 'rt-auth-agreement-link').text == 'пользовательского соглашения'
    assert right_obj.find_element(By.ID, 'rt-auth-agreement-link').get_attribute('href') == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html'
    assert right_obj.find_element(By.ID, 'oidc_tinkoff').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_tinkoff/login'
    assert right_obj.find_element(By.ID, 'oidc_ya').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_ya/login'
    assert right_obj.find_element(By.ID, 'oidc_vk').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_vk/login'
    assert right_obj.find_element(By.ID, 'oidc_mail').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_mail/login'
    assert right_obj.find_element(By.ID, 'oidc_ok').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_ok/login'
    EC.element_to_be_clickable(((By.CSS_SELECTOR, 'div#faq-open a')))
    assert right_obj.find_element(By.CSS_SELECTOR, 'div#faq-open a').text == 'Помощь'

    footer_obj = driver.find_element(By.CSS_SELECTOR, 'footer#app-footer')

    assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-left .rt-footer-side-item').text == '© 2024 ПАО «Ростелеком». 18+'
    EC.element_to_be_clickable(((By.CSS_SELECTOR, 'span#cookies-tip-open')))
    list_of_obj = footer_obj.find_elements(By.CSS_SELECTOR, 'a.rt-footer-agreement-link')
    assert list_of_obj[0].get_attribute('href') == 'https://www.rt.ru/legal'
    assert list_of_obj[1].get_attribute('href') == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html'
    assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-right').text.split('\n')[0] == 'Служба поддержки'
    assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-right').text.split('\n')[1] == '8 800 100 0 800'


def test_load_page_auth_std(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'section#page-right .card-container')))
    
    curr_url = driver.current_url

    assert curr_url.split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth'

    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    assert curr_url.split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate'
    
    header_obj = driver.find_elements(By.CSS_SELECTOR, 'header#app-header path')

    assert len(header_obj) == 12

    left_obj = driver.find_element(By.CSS_SELECTOR, 'section#page-left .what-is-container')

    assert left_obj.find_element(By.TAG_NAME, 'h2').text == 'Личный кабинет'
    assert left_obj.find_element(By.TAG_NAME, 'p').text == 'Персональный помощник в цифровом мире Ростелекома'

    right_obj = driver.find_element(By.CSS_SELECTOR, 'section#page-right .card-container')

    assert right_obj.find_element(By.ID, 'card-title').text == 'Авторизация'
    assert len(right_obj.find_elements(By.CSS_SELECTOR, '.rt-tabs div')) == 4
    assert right_obj.find_element(By.ID, 't-btn-tab-phone').text == 'Телефон'
    assert right_obj.find_element(By.ID, 't-btn-tab-mail').text == 'Почта'
    assert right_obj.find_element(By.ID, 't-btn-tab-login').text == 'Логин'
    assert right_obj.find_element(By.ID, 't-btn-tab-ls').text == 'Лицевой счёт'
    assert right_obj.find_element(By.CSS_SELECTOR, 'input#username').get_attribute('type') == 'text'
    assert right_obj.find_element(By.CSS_SELECTOR, 'input#password').get_attribute('type') == 'password'
    assert right_obj.find_element(By.CSS_SELECTOR, 'input.rt-rt-checkbox__input').get_attribute('type') == 'checkbox'
    assert right_obj.find_element(By.CSS_SELECTOR, '.rt-checkbox__label').text == 'Запомнить меня'
    assert right_obj.find_element(By.ID, 'forgot_password').text == 'Забыл пароль'
    assert right_obj.find_element(By.ID, 'forgot_password').get_attribute('href').split('?')[0] == '/auth/realms/b2c/login-actions/reset-credentials'
    assert right_obj.find_element(By.CSS_SELECTOR, 'button#kc-login').text == 'Войти'
    assert right_obj.find_element(By.CSS_SELECTOR, 'button#back_to_otp_btn').text == 'Войти по временному коду'
    assert right_obj.find_element(By.CSS_SELECTOR, 'div.auth-policy span').text == 'Нажимая кнопку «Войти», вы принимаете условия'
    assert right_obj.find_element(By.ID, 'rt-auth-agreement-link').text == 'пользовательского соглашения'
    assert right_obj.find_element(By.ID, 'rt-auth-agreement-link').get_attribute('href') == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html'
    assert right_obj.find_element(By.ID, 'oidc_tinkoff').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_tinkoff/login'
    assert right_obj.find_element(By.ID, 'oidc_ya').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_ya/login'
    assert right_obj.find_element(By.ID, 'oidc_vk').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_vk/login'
    assert right_obj.find_element(By.ID, 'oidc_mail').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_mail/login'
    assert right_obj.find_element(By.ID, 'oidc_ok').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_ok/login'
    EC.element_to_be_clickable(((By.CSS_SELECTOR, 'div#faq-open a')))
    assert right_obj.find_element(By.CSS_SELECTOR, 'div#faq-open a').text == 'Помощь'

    # Вкладки
    driver.find_element(By.ID, 't-btn-tab-phone').click()
    assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'Мобильный телефон'
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'Электронная почта'
    driver.find_element(By.ID, 't-btn-tab-login').click()
    assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'Логин'
    driver.find_element(By.ID, 't-btn-tab-ls').click()
    assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'Лицевой счёт'

    footer_obj = driver.find_element(By.CSS_SELECTOR, 'footer#app-footer')

    assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-left .rt-footer-side-item').text == '© 2024 ПАО «Ростелеком». 18+'
    EC.element_to_be_clickable(((By.CSS_SELECTOR, 'span#cookies-tip-open')))
    list_of_obj = footer_obj.find_elements(By.CSS_SELECTOR, 'a.rt-footer-agreement-link')
    assert list_of_obj[0].get_attribute('href') == 'https://www.rt.ru/legal'
    assert list_of_obj[1].get_attribute('href') == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html'
    assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-right').text.split('\n')[0] == 'Служба поддержки'
    assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-right').text.split('\n')[1] == '8 800 100 0 800'


def test_return_to_auth_by_code(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'section#page-right .card-container')))
    
    curr_url = driver.current_url

    assert curr_url.split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth'

    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    assert curr_url.split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate'

    driver.find_element(By.CSS_SELECTOR, 'button#back_to_otp_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'button#standard_auth_btn')))

    curr_url = driver.current_url

    assert curr_url.split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate'
    
    header_obj = driver.find_elements(By.CSS_SELECTOR, 'header#app-header path')

    assert len(header_obj) == 12

    left_obj = driver.find_element(By.CSS_SELECTOR, 'section#page-left .what-is-container')

    assert left_obj.find_element(By.TAG_NAME, 'h2').text == 'Личный кабинет'
    assert left_obj.find_element(By.TAG_NAME, 'p').text == 'Персональный помощник в цифровом мире Ростелекома'

    right_obj = driver.find_element(By.CSS_SELECTOR, 'section#page-right .card-container')

    assert right_obj.find_element(By.ID, 'card-title').text == 'Авторизация по коду'
    assert right_obj.find_element(By.CSS_SELECTOR, 'p#card-description').text == 'Укажите почту или номер телефона, на которые необходимо отправить код подтверждения'
    assert right_obj.find_element(By.CSS_SELECTOR, 'input#address').get_attribute('type') == 'text'
    assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'E-mail или мобильный телефон'
    assert right_obj.find_element(By.CSS_SELECTOR, 'button#otp_get_code').text == 'Получить код'
    assert right_obj.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').text == 'Войти с паролем'
    assert right_obj.find_element(By.CSS_SELECTOR, 'div.auth-policy span').text == 'Нажимая кнопку «Получить код», вы принимаете условия'
    assert right_obj.find_element(By.ID, 'rt-auth-agreement-link').text == 'пользовательского соглашения'
    assert right_obj.find_element(By.ID, 'rt-auth-agreement-link').get_attribute('href') == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html'
    assert right_obj.find_element(By.ID, 'oidc_tinkoff').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_tinkoff/login'
    assert right_obj.find_element(By.ID, 'oidc_ya').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_ya/login'
    assert right_obj.find_element(By.ID, 'oidc_vk').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_vk/login'
    assert right_obj.find_element(By.ID, 'oidc_mail').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_mail/login'
    assert right_obj.find_element(By.ID, 'oidc_ok').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_ok/login'
    EC.element_to_be_clickable(((By.CSS_SELECTOR, 'div#faq-open a')))
    assert right_obj.find_element(By.CSS_SELECTOR, 'div#faq-open a').text == 'Помощь'

    footer_obj = driver.find_element(By.CSS_SELECTOR, 'footer#app-footer')

    assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-left .rt-footer-side-item').text == '© 2024 ПАО «Ростелеком». 18+'
    EC.element_to_be_clickable(((By.CSS_SELECTOR, 'span#cookies-tip-open')))
    list_of_obj = footer_obj.find_elements(By.CSS_SELECTOR, 'a.rt-footer-agreement-link')
    assert list_of_obj[0].get_attribute('href') == 'https://www.rt.ru/legal'
    assert list_of_obj[1].get_attribute('href') == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html'
    assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-right').text.split('\n')[0] == 'Служба поддержки'
    assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-right').text.split('\n')[1] == '8 800 100 0 800'


def test_redirect_to_auth_std(driver):
    url_list = ['https://b2c.passport.rt.ru', 'https://rostelecomid.rt.ru', 'https://id.rt.ru']

    for ele in url_list:
        driver.get(ele)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                    (By.CSS_SELECTOR, 'section#page-right .card-container')))
        
        curr_url = driver.current_url

        assert curr_url.split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate'
        
        header_obj = driver.find_elements(By.CSS_SELECTOR, 'header#app-header path')

        assert len(header_obj) == 12

        left_obj = driver.find_element(By.CSS_SELECTOR, 'section#page-left .what-is-container')

        assert left_obj.find_element(By.TAG_NAME, 'h2').text == 'Личный кабинет'
        assert left_obj.find_element(By.TAG_NAME, 'p').text == 'Персональный помощник в цифровом мире Ростелекома'

        right_obj = driver.find_element(By.CSS_SELECTOR, 'section#page-right .card-container')

        assert right_obj.find_element(By.ID, 'card-title').text == 'Авторизация'
        assert len(right_obj.find_elements(By.CSS_SELECTOR, '.rt-tabs div')) == 4
        assert right_obj.find_element(By.ID, 't-btn-tab-phone').text == 'Телефон'
        assert right_obj.find_element(By.ID, 't-btn-tab-mail').text == 'Почта'
        assert right_obj.find_element(By.ID, 't-btn-tab-login').text == 'Логин'
        assert right_obj.find_element(By.ID, 't-btn-tab-ls').text == 'Лицевой счёт'
        assert right_obj.find_element(By.CSS_SELECTOR, 'input#username').get_attribute('type') == 'text'
        assert right_obj.find_element(By.CSS_SELECTOR, 'input#password').get_attribute('type') == 'password'
        assert right_obj.find_element(By.CSS_SELECTOR, 'input.rt-rt-checkbox__input').get_attribute('type') == 'checkbox'
        assert right_obj.find_element(By.CSS_SELECTOR, '.rt-checkbox__label').text == 'Запомнить меня'
        assert right_obj.find_element(By.ID, 'forgot_password').text == 'Забыл пароль'
        assert right_obj.find_element(By.ID, 'forgot_password').get_attribute('href').split('?')[0] == '/auth/realms/b2c/login-actions/reset-credentials'
        assert right_obj.find_element(By.CSS_SELECTOR, 'button#kc-login').text == 'Войти'
        assert right_obj.find_element(By.CSS_SELECTOR, 'button#back_to_otp_btn').text == 'Войти по временному коду'
        assert right_obj.find_element(By.CSS_SELECTOR, 'div.auth-policy span').text == 'Нажимая кнопку «Войти», вы принимаете условия'
        assert right_obj.find_element(By.ID, 'rt-auth-agreement-link').text == 'пользовательского соглашения'
        assert right_obj.find_element(By.ID, 'rt-auth-agreement-link').get_attribute('href') == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html'
        assert right_obj.find_element(By.ID, 'oidc_tinkoff').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_tinkoff/login'
        assert right_obj.find_element(By.ID, 'oidc_ya').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_ya/login'
        assert right_obj.find_element(By.ID, 'oidc_vk').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_vk/login'
        assert right_obj.find_element(By.ID, 'oidc_mail').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_mail/login'
        assert right_obj.find_element(By.ID, 'oidc_ok').get_attribute('href').split('?')[0] == 'https://b2c.passport.rt.ru/auth/realms/b2c/broker/oidc_ok/login'
        EC.element_to_be_clickable(((By.CSS_SELECTOR, 'div#faq-open a')))
        assert right_obj.find_element(By.CSS_SELECTOR, 'div#faq-open a').text == 'Помощь'

        # Вкладки
        driver.find_element(By.ID, 't-btn-tab-phone').click()
        assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'Мобильный телефон'
        driver.find_element(By.ID, 't-btn-tab-mail').click()
        assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'Электронная почта'
        driver.find_element(By.ID, 't-btn-tab-login').click()
        assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'Логин'
        driver.find_element(By.ID, 't-btn-tab-ls').click()
        assert right_obj.find_element(By.CSS_SELECTOR, '.rt-input__placeholder').text == 'Лицевой счёт'

        footer_obj = driver.find_element(By.CSS_SELECTOR, 'footer#app-footer')

        assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-left .rt-footer-side-item').text == '© 2024 ПАО «Ростелеком». 18+'
        EC.element_to_be_clickable(((By.CSS_SELECTOR, 'span#cookies-tip-open')))
        list_of_obj = footer_obj.find_elements(By.CSS_SELECTOR, 'a.rt-footer-agreement-link')
        assert list_of_obj[0].get_attribute('href') == 'https://www.rt.ru/legal'
        assert list_of_obj[1].get_attribute('href') == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html'
        assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-right').text.split('\n')[0] == 'Служба поддержки'
        assert footer_obj.find_element(By.CSS_SELECTOR, '.rt-footer-right').text.split('\n')[1] == '8 800 100 0 800'


def test_send_auth_code_to_email(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'input#address').send_keys(settings.valid_mail_otp)
    driver.find_element(By.CSS_SELECTOR, 'button#otp_get_code').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'input#rt-code-input')))

    # Костыльный простой метод проверки получения кода - если нет ввода в rt-sdi-container__input-value (первый), то нету кода
    # Но общее ожидание - 120 сек
    # И необходимо "вмешательство" пользователя
    for i in range(12):
        sleep(10)
        input_ele = driver.find_element(By.CSS_SELECTOR, '.rt-sdi-container__input-value').text
        if input_ele != '':
            break
    else:
        raise Exception('Пользователем не был получен код подтверждения.')


def test_send_auth_code_to_phone(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'input#address').send_keys(settings.valid_phone_otp)
    driver.find_element(By.CSS_SELECTOR, 'button#otp_get_code').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'input#rt-code-input')))

    # Костыльный простой метод проверки получения кода - если нет ввода в rt-sdi-container__input-value (первый), то нету кода
    # Но общее ожидание - 120 сек
    # И необходимо "вмешательство" пользователя
    for i in range(12):
        sleep(10)
        input_ele = driver.find_element(By.CSS_SELECTOR, '.rt-sdi-container__input-value').text
        if input_ele != '':
            break
    else:
        raise Exception('Пользователем не был получен код подтверждения.')


def test_send_auth_code_to_inv_email(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'input#address').send_keys('exampleemail.ru')
    driver.find_element(By.CSS_SELECTOR, 'button#otp_get_code').click()


def test_send_auth_code_to_inv_phone(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'input#address').send_keys('123456789')
    driver.find_element(By.CSS_SELECTOR, 'button#otp_get_code').click()


def test_auth_with_auth_code(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'input#address').send_keys(settings.valid_mail_otp)
    driver.find_element(By.CSS_SELECTOR, 'button#otp_get_code').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'input#rt-code-input')))

    pre_code_url = driver.current_url

    # Костыльный простой метод проверки авторизации - ждём, пока не "исчезнет" поле ввода кода rt-sdi-container__input-value
    # Но общее ожидание - 120 сек
    # И необходимо "вмешательство" пользователя, опять
    WebDriverWait(driver, 120).until_not(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, '.rt-sdi-container__input-value')))

    curr_url = driver.current_url
    assert pre_code_url != curr_url


def test_auth_with_inv_auth_code(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'input#address').send_keys(settings.valid_mail_otp)
    driver.find_element(By.CSS_SELECTOR, 'button#otp_get_code').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'input#rt-code-input')))

    input_obj = driver.find_elements(By.CSS_SELECTOR, '.rt-input input')
    
    for i in range(len(input_obj)):
        input_obj[i].send_keys(i)

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный код. Повторите попытку'


def test_auth_with_phone(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-phone').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.valid_phone_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.valid_phone_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    pre_code_url = driver.current_url
    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'button#kc-login')))
    curr_url = driver.current_url
    assert pre_code_url != curr_url


def test_auth_with_mail(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.valid_mail_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.valid_mail_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    pre_code_url = driver.current_url
    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'button#kc-login')))
    curr_url = driver.current_url
    assert pre_code_url != curr_url


def test_auth_with_login(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-login').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.valid_login_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.valid_login_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    pre_code_url = driver.current_url
    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'button#kc-login')))
    curr_url = driver.current_url
    assert pre_code_url != curr_url


def test_auth_with_ls(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-ls').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.valid_ls_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.valid_ls_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    pre_code_url = driver.current_url
    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located(
                                   (By.CSS_SELECTOR, 'button#kc-login')))
    curr_url = driver.current_url
    assert pre_code_url != curr_url


def test_auth_with_inv_phone(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-phone').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.inv_phone_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.inv_phone_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'form-error-message')))

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'


def test_auth_with_inv_mail(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.inv_mail_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.inv_mail_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'form-error-message')))

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'


def test_auth_with_inv_login(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-login').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.inv_login_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.inv_login_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'form-error-message')))

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'


def test_auth_with_inv_ls(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-ls').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.inv_ls_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.inv_ls_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'form-error-message')))

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'


def test_auth_with_empty_phone(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-phone').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(Keys.DELETE)
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.valid_phone_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'username-meta')))

    assert driver.find_element(By.ID, 'username-meta').text == 'Введите номер телефона'


def test_auth_with_empty_mail(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(Keys.DELETE)
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.valid_mail_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'username-meta')))

    assert driver.find_element(By.ID, 'username-meta').text == 'Введите адрес, указанный при регистрации'


def test_auth_with_empty_login(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-login').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(Keys.DELETE)
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.valid_login_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'username-meta')))

    assert driver.find_element(By.ID, 'username-meta').text == 'Введите логин, указанный при регистрации'


def test_auth_with_empty_ls(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-ls').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(Keys.DELETE)
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(settings.valid_ls_std[1])
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'username-meta')))

    assert driver.find_element(By.ID, 'username-meta').text == 'Введите номер вашего лицевого счета'


def test_auth_with_phone_empty_pass(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-phone').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.valid_phone_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(Keys.DELETE)
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'password-meta')))

    assert driver.find_element(By.ID, 'password-meta').text == 'Введите пароль'


def test_auth_with_mail_empty_pass(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.valid_mail_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(Keys.DELETE)
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'password-meta')))

    assert driver.find_element(By.ID, 'password-meta').text == 'Введите пароль'


def test_auth_with_login_empty_pass(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.valid_login_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(Keys.DELETE)
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'password-meta')))

    assert driver.find_element(By.ID, 'password-meta').text == 'Введите пароль'


def test_auth_with_ls_empty_pass(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'section#page-right .card-container')))
    driver.find_element(By.CSS_SELECTOR, 'button#standard_auth_btn').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'button#back_to_otp_btn')))

    driver.find_element(By.ID, 't-btn-tab-ls').click()
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(settings.valid_ls_std[0])
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(Keys.DELETE)
    driver.find_element(By.CSS_SELECTOR, 'button#kc-login').click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                   (By.ID, 'password-meta')))

    assert driver.find_element(By.ID, 'password-meta').text == 'Введите пароль'