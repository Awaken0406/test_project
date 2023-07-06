import pygame
import os
import random
import tkinter as tk



def Play():
    name = random.choice(file_names)
    pygame.mixer.music.load(dir_path + name)
    pygame.mixer.music.play()
    print(name,'playing...')

def Stop():
    pygame.mixer.music.stop()


def Pause():
    pygame.mixer.music.pause()

def Continue():
    pygame.mixer.music.unpause()

 # 获取目录下的文件名列表,并过滤!!!文件
dir_path = 'D:/Users/chenyongsen/Music/'
file_names = [f for f in os.listdir(dir_path) if not f.startswith('!!!')]
pygame.init()


# 创建主窗口
root = tk.Tk()
root.title('My GUI')
# 添加标签
label = tk.Label(root, text='Music Play')
label.pack()
# 添加按钮
button = tk.Button(root, text='Play!', command=Play)
button.pack()
button = tk.Button(root, text='Stop!', command=Stop)
button.pack()
button = tk.Button(root, text='Pause!', command=Pause)
button.pack()
button = tk.Button(root, text='Continue!', command=Continue)
button.pack()
# 进入主循环
root.mainloop()




