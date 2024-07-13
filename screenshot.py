import pyautogui
import cv2
import numpy as np
import pickle


def capture_screen():
    # Capture the screen
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    return screen

