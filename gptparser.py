from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

class Gptparser:
    def __init__(self,url):
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=C:\\Users\\p1233456\\AppData\\Local\\Google\\Chrome\\User Data")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("detach", True)
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.get(url)
        self.beforeid = ''

    def ask(self,content):
        self.driver.find_element(By.ID, "prompt-textarea").send_keys(content)
        elements = self.driver.find_element(By.XPATH, f"//textarea[@id='prompt-textarea']/parent::*/button")
        elements.click()
        return self.receive()

    def receive(self):
        while True:
            try:
                if self.beforeid == '':
                    time.sleep(10)
                    self.driver.find_element(By.XPATH, f"//textarea[@id='prompt-textarea']/parent::*/button/span[@data-state='closed']")    
                    conversation_divs = self.driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'conversation')]")
                    target = conversation_divs[-1]
                    #self.beforeid = target.id
                    break
                else:
                    conversation_divs = self.driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'conversation')]")
                    target = conversation_divs[-1]
                    if self.beforeid != target.id:
                        self.driver.find_element(By.XPATH, f"//textarea[@id='prompt-textarea']/parent::*/button/span[@data-state='closed']")    

                        self.beforeid = target.id
                        break
            except:
                continue
        
        conversation_divs = self.driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'conversation')]")
        paragraphs = conversation_divs[-1].find_elements(By.TAG_NAME, 'p')
        
        print("응답")
        answers = []
        for paragraph in paragraphs:
            print(paragraph.text)
            answers.append(paragraph.text)

        return answers