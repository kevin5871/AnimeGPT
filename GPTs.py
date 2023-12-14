from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from gtts import gTTS 
import os 
from infer.modules.vc.modules import VC
from configs.config import Config
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import tkinter as tk
from tkinter import font
from tkinter import messagebox



# 세팅
language = 'ja'
model_name = "suzuran.pth"
index_path = "C:\\Users\\p1233456\\Desktop\\Anime GPT\\assets\\weights\\added_IVF460_Flat_nprobe_1_suzuran_v2.index"
audio_path = "C:\\Users\\p1233456\\Desktop\\Anime GPT\\audio\\sample.mp3"

config = Config()
vc = VC(config)
vc.get_vc(model_name,0.33,0.33)

chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:\\Users\\p1233456\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = 'https://chat.openai.com/g/g-0LErf1xuT-seujeuran'
driver.get(url)
time.sleep(3)

def ask(driver, content):
    driver.find_element(By.ID, "prompt-textarea").send_keys(content)
    elements = driver.find_element(By.XPATH, f"//textarea[@id='prompt-textarea']/parent::*/button")
    elements.click()
    return receive(driver)

def receive(driver):
    time.sleep(10)
    while True:
        try:
            driver.find_element(By.XPATH, f"//textarea[@id='prompt-textarea']/parent::*/button/span[@data-state='closed']")            
            break
        except:
            time.sleep(1)
            continue
    
    conversation_divs = driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'conversation')]")
    paragraphs = conversation_divs[-1].find_elements(By.TAG_NAME, 'p')
    answers = ['','']

    if len(paragraphs) == 1:
        answers[1] = paragraphs[0].text.split('\n')[1]
        answers[0] = paragraphs[0].text.split('\n')[0]
    else:
        answers[1] = paragraphs[1].text
        answers[0] = paragraphs[0].text

    text2speech(answers[0])
    return answers[1]
    

def text2speech(txt):
    gTTS(text=txt, lang=language, slow=False).save(audio_path)
    opt1,opt2 = vc.vc_single(
        sid=0,
        input_audio_path=audio_path,
        f0_up_key=8,
        f0_file="",
        f0_method="rmvpe",
        file_index=index_path,
        file_index2="",
        index_rate=0,
        filter_radius=3.0,
        resample_sr=0,
        rms_mix_rate=0.25,
        protect=0.33
    )
    sd.play(opt2[1], opt2[0])

# Create the main window
root = tk.Tk()
root.title("Question and Answer Application")
self_font = font.Font(family='경기천년제목', size=20)

# Set the size of the window to match the image dimensions
root.geometry("1365x768")

# Load the background image
background_image = tk.PhotoImage(file='C:\\Users\\p1233456\\Desktop\\Anime GPT\\lisa.png')
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create the output text area
output_text = tk.Text(root, bg="blue", fg="white", font=("Helvetica", 20))
output_text.place(x=50, y=500, width=1265, height=200)
output_text.insert('1.0', "스즈란")
output_text.config(state=tk.DISABLED)

# Create the input text area
input_text = tk.Text(root, bg="green", fg="white", font=("Helvetica", 20))
input_text.place(x=50, y=700, width=1000, height=50)


# Function to handle the submission of input
def submit_input():
    # Get the input text
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please enter a question.")
        return
    
    # For demonstration, we'll just echo the input in the output area.
    # In a real application, you could process this input and generate an answer.
    output_text.config(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)
    output_text.insert('1.0', ask(driver, user_input))  # This is where the answer would go
    output_text.config(state=tk.DISABLED)
    input_text.delete('1.0', tk.END)

# Create the submit button
submit_button = tk.Button(root, bg="white", fg="black", command=submit_input)
submit_button.place(x=1000, y=700, width=100, height=50)

# Start the GUI loop
root.mainloop()
