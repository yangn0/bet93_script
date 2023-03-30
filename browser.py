from selenium import webdriver

import os

class Browser:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options, executable_path=f'./chromedriver.exe')
        self.driver.get(os.path.join(os.getcwd(), 'index.html'))
        #self.driver.get('file:///Users/edz/Desktop/oojj/sansanpao_20220305/index.html')

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass

    def execute_script(self, script: str):
        return self.driver.execute_script(script=script)



if __name__ == '__main__':
    browser = Browser()
    pass