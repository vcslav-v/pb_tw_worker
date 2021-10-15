import facebook
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import db
import models
import json

SELENOID_URL = os.environ.get('SELENOID_URL')
FB_PAGE_ID = os.environ.get('FB_PAGE_ID')
FB_NAME = os.environ.get('FB_NAME')
FB_PASS = os.environ.get('FB_PASS')
COOKIES_FB_DOMAIN = '.facebook.com'

def post(item_url: str, item_disc: str, *args):
    try:
        access_token = get_access_token()
    except:
        delete_cookies()
        access_token = get_access_token()
    cfg = {
        'page_id'      : FB_PAGE_ID,
        'access_token' : access_token,
    }

    graph = facebook.GraphAPI(cfg['access_token'])
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
        if page['id'] == cfg['page_id']:
            page_access_token = page['access_token']
    api = facebook.GraphAPI(page_access_token)

    api.put_wall_post(item_disc,
    attachment={
        'link': item_url,
    },
    profile_id=FB_PAGE_ID,
)


def get_access_token() -> str:
    capabilities = {
        'browserName': 'chrome',
        'enableVNC': True,
        'enableVideo': False,
    }
    driver = webdriver.Remote(
        command_executor=SELENOID_URL,
        desired_capabilities=capabilities,
    )
    
    driver.get('https://www.facebook.com/')
    cookies = get_cookies()
    if cookies:
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('https://www.facebook.com/')
    else:
        fb_login(driver)

    
    current_window = driver.current_window_handle
    
    driver.get('https://developers.facebook.com/tools/explorer/')
    button = WebDriverWait(driver, timeout=20).until(
        lambda l: l.find_element_by_xpath("//div[@data-hover='tooltip'][contains(.,'Generate Access Token')]")
    )
    button.click()

    for window_handle in driver.window_handles:
        if window_handle != current_window:
            driver.switch_to.window(window_handle)
            current_window = driver.current_window_handle
            break
    
    button = WebDriverWait(driver, timeout=20).until(
        lambda l: l.find_element_by_xpath("//span[contains(.,'Продолжить как Вячеслав Васильев')]")
    )
    button.click()

    input_token = WebDriverWait(driver, timeout=20).until(
        lambda l: l.find_element_by_xpath("//input[@placeholder='Маркер доступа']")
    )
    access_token = input_token.get_property('value')
    set_cookies(driver.get_cookies())
    return access_token


def fb_login(driver):
    try:
        button = WebDriverWait(driver, timeout=20).until(
            lambda l: l.find_element_by_xpath("//button[@data-testid='cookie-policy-dialog-accept-button']")
        )
        button.click()
    except:
        pass
    input_email = WebDriverWait(driver, timeout=20).until(
        lambda l: l.find_element_by_id('email')
    )
    input_email.send_keys(FB_NAME)
    input_pass = WebDriverWait(driver, timeout=20).until(
        lambda l: l.find_element_by_id('pass')
    )
    input_pass.send_keys(FB_PASS)
    button = button = WebDriverWait(driver, timeout=20).until(
        lambda l: l.find_element_by_xpath("//button[@name='login']")
    )
    button.click()


def get_cookies():
    domain_cookies = []
    with db.SessionLocal() as session:
        cookies = session.query(models.Cookie).filter_by(domain=COOKIES_FB_DOMAIN).all()
        for cookie in cookies:
            domain_cookies.append(json.loads(cookie.data))
    return domain_cookies


def set_cookies(cookies: list):
    with db.SessionLocal() as session:
        delete_cookies()
        for cookie in cookies:
            session.add(models.Cookie(domain=COOKIES_FB_DOMAIN, data=json.dumps(cookie)))
        session.commit()


def delete_cookies():
    with db.SessionLocal() as session:
        current_cookies = session.query(models.Cookie).filter_by(domain=COOKIES_FB_DOMAIN).all()
        for cookie in current_cookies:
            session.delete(cookie)
            session.commit()
