import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk

RESIZE_BOYUT = (300,400) 
RESIM_KLASORU = 'resimler'
KAPAK_RESMI = 'kapak.jpg'
GRID_BOYUTU = (5, 2)

pencere = tk.Tk()
pencere.title("Hafıza Oyunu")
pencere.resizable(False, False) 

kart_dugmeleri = []     
kart_resimleri = []     
acik_kartlar = []       
eslesen_kart_sayisi = 0
resim_nesneleri = {}

def resimleri_yukle_ve_karistir():
    global kart_resimleri
    
    tum_resimler = [f for f in os.listdir(RESIM_KLASORU) if f != KAPAK_RESMI and f.endswith(('.jpg', '.jpeg', '.png'))]

    cift_sayisi = (GRID_BOYUTU[0] * GRID_BOYUTU[1]) // 2 # (5*2)/2 = 5
    
    secilen_resimler = tum_resimler[:cift_sayisi]
    kart_resimleri = secilen_resimler * 2 
    random.shuffle(kart_resimleri) 

    img_kapak = Image.open(os.path.join(RESIM_KLASORU, KAPAK_RESMI))
    img_kapak = img_kapak.resize(RESIZE_BOYUT)
    resim_nesneleri['kapak'] = ImageTk.PhotoImage(img_kapak)

    for resim_adi in secilen_resimler:
        img = Image.open(os.path.join(RESIM_KLASORU, resim_adi))
        img = img.resize(RESIZE_BOYUT)
        resim_nesneleri[resim_adi] = ImageTk.PhotoImage(img)

def kart_tiklandi(index):
    global eslesen_kart_sayisi

    dugme = kart_dugmeleri[index]
    resim_adi = kart_resimleri[index]

    if dugme['state'] == 'disabled' or index in acik_kartlar:
        return

    if len(acik_kartlar) == 2:
        return

    resim = resim_nesneleri[resim_adi]
    dugme.config(image=resim)
    
    acik_kartlar.append(index)

    if len(acik_kartlar) == 1:
        return
        
    if len(acik_kartlar) == 2:
        index1 = acik_kartlar[0]
        index2 = acik_kartlar[1]
        
        resim_adi1 = kart_resimleri[index1]
        resim_adi2 = kart_resimleri[index2]
        
        if resim_adi1 == resim_adi2:
            print("Eşleşti!")
            
            kart_dugmeleri[index1].config(state='disabled')
            kart_dugmeleri[index2].config(state='disabled')
            
            acik_kartlar.clear()
            
            eslesen_kart_sayisi += 1
            if eslesen_kart_sayisi == (GRID_BOYUTU[0] * GRID_BOYUTU[1]) // 2:
                messagebox.showinfo("Tebrikler!", "Tebrikler! Oyunu kazandın!")
                pencere.quit()
        else:
            print("Eşleşmedi...")
            pencere.after(1000, geri_kapat)

def geri_kapat():
    index1 = acik_kartlar[0]
    index2 = acik_kartlar[1]
    
    kapak_img = resim_nesneleri['kapak']
    
    kart_dugmeleri[index1].config(image=kapak_img)
    kart_dugmeleri[index2].config(image=kapak_img)
    
    acik_kartlar.clear()


resimleri_yukle_ve_karistir()

for satir in range(GRID_BOYUTU[1]): 
    for sutun in range(GRID_BOYUTU[0]): 
        
        index = (satir * GRID_BOYUTU[0]) + sutun
        
        dugme = tk.Button(pencere, 
                          image=resim_nesneleri['kapak'], 
                          command=lambda i=index: kart_tiklandi(i))
        
        dugme.grid(row=satir, column=sutun, padx=5, pady=5)
        
        kart_dugmeleri.append(dugme)

pencere.mainloop()