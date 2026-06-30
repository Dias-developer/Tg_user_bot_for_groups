from random import randint
from captcha.image import ImageCaptcha
captcha_len = 5

def generate_captcha_text():
    numbers = []
    for i in range(captcha_len):
        numbers.append(randint(0, 9))
    captcha_text = "".join(numbers)
    return captcha_text

class Captcha:
    captcha_text = ''
    captcha_image = 0
    def __init__(self):
        image = ImageCaptcha(width=280, height=90)
        self.captcha_text = generate_captcha_text()
        self.captcha_image = image.generate(self.captcha_text)