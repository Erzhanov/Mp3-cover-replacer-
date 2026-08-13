#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, COMM, ID3NoHeaderError
from PIL import Image
import threading

class MP3CoverReplacer:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Өңдеу / MP3 Editor - Обложка және Исполнитель")
        self.root.geometry("1080x1920")
        self.root.configure(bg="#f0f0f0")
        
        # Пайдалану ақпараты
        self.mp3_files = []
        self.cover_image = None
        self.is_processing = False
        self.artist_text = None
        self.title_text = None
        self.album_text = None
        self.year_text = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Интерфейс элементтерін құру"""
        
        # Негізгі фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Прокрутка үшін Canvas
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Атауы
        title_label = ttk.Label(scrollable_frame, text="MP3 Өңдеу / MP3 Editor",
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # MP3 файлдарын таңдау
        ttk.Label(scrollable_frame, text="1. MP3 файлдарын таңдаңыз:", 
                 font=("Arial", 11, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.mp3_listbox = tk.Listbox(scrollable_frame, height=6, width=80)
        self.mp3_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # Скролл панелі
        mp3_scrollbar = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=self.mp3_listbox.yview)
        mp3_scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.mp3_listbox.config(yscrollcommand=mp3_scrollbar.set)
        
        # MP3 таңдау батоны
        btn_frame1 = ttk.Frame(scrollable_frame)
        btn_frame1.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        ttk.Button(btn_frame1, text="📁 MP3 файлдарын таңдау",
                  command=self.select_mp3_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame1, text="🗑️ Тазалау",
                  command=self.clear_mp3_files).pack(side=tk.LEFT, padx=5)
        
        # Обложка таңдау
        ttk.Label(scrollable_frame, text="2. Жаңа обложканы таңдаңыз (міндетті емес):",
                 font=("Arial", 11, "bold")).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.cover_label = ttk.Label(scrollable_frame, text="Обложка таңдалмаған",
                                     foreground="red")
        self.cover_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=5)
        
        ttk.Button(scrollable_frame, text="🖼️ Обложка суретін таңдау (JPG/PNG)",
                  command=self.select_cover_image).grid(row=6, column=0, columnspan=2, pady=5, sticky=tk.W, padx=5)
        
        # Метаданные өндеу
        ttk.Label(scrollable_frame, text="3. MP3 Метаданысын өндеңіз (міндетті емес):",
                 font=("Arial", 11, "bold")).grid(row=7, column=0, sticky=tk.W, pady=(10, 5))
        
        # Исполнитель
        ttk.Label(scrollable_frame, text="Исполнитель / Artist:").grid(row=8, column=0, sticky=tk.W, padx=5)
        self.artist_text = ttk.Entry(scrollable_frame, width=50)
        self.artist_text.grid(row=8, column=1, padx=5, pady=3, sticky=(tk.W, tk.E))
        
        # Трек аты
        ttk.Label(scrollable_frame, text="Трек аты / Title:").grid(row=9, column=0, sticky=tk.W, padx=5)
        self.title_text = ttk.Entry(scrollable_frame, width=50)
        self.title_text.grid(row=9, column=1, padx=5, pady=3, sticky=(tk.W, tk.E))
        
        # Альбом
        ttk.Label(scrollable_frame, text="Альбом / Album:").grid(row=10, column=0, sticky=tk.W, padx=5)
        self.album_text = ttk.Entry(scrollable_frame, width=50)
        self.album_text.grid(row=10, column=1, padx=5, pady=3, sticky=(tk.W, tk.E))
        
        # Жыл
        ttk.Label(scrollable_frame, text="Жыл / Year:").grid(row=11, column=0, sticky=tk.W, padx=5)
        self.year_text = ttk.Entry(scrollable_frame, width=50)
        self.year_text.grid(row=11, column=1, padx=5, pady=3, sticky=(tk.W, tk.E))
        
        # Прогресс индикатор
        ttk.Label(scrollable_frame, text="4. Прогресс:",
                 font=("Arial", 11, "bold")).grid(row=12, column=0, sticky=tk.W, pady=(10, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(scrollable_frame, variable=self.progress_var,
                                           maximum=100, length=400)
        self.progress_bar.grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(scrollable_frame, text="Дайын / Ready")
        self.status_label.grid(row=14, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        # Лог бөлігі
        ttk.Label(scrollable_frame, text="Логи / Log:",
                 font=("Arial", 11, "bold")).grid(row=15, column=0, sticky=tk.W, pady=(10, 5))
        
        self.log_text = tk.Text(scrollable_frame, height=6, width=80)
        self.log_text.grid(row=16, column=0, columnspan=2, padx=5, pady=5)
        
        log_scrollbar = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=16, column=2, sticky=(tk.N, tk.S))
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        # Батондар
        btn_frame2 = ttk.Frame(scrollable_frame)
        btn_frame2.grid(row=17, column=0, columnspan=2, pady=20)
        
        self.execute_btn = ttk.Button(btn_frame2, text="▶️ ОРЫНДАУ / EXECUTE",
                                      command=self.execute_replacement)
        self.execute_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame2, text="🗑️ Логты тазалау",
                  command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame2, text="❌ Шығу",
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    def select_mp3_files(self):
        """MP3 файлдарын таңдау"""
        files = filedialog.askopenfilenames(
            title="MP3 файлдарын таңдаңыз",
            filetypes=[("MP3 файлдары", "*.mp3"), ("Барлық файлдар", "*.*")]
        )
        
        if files:
            self.mp3_files.extend(files)
            self.mp3_listbox.delete(0, tk.END)
            for file in self.mp3_files:
                self.mp3_listbox.insert(tk.END, os.path.basename(file))
            self.log(f"✓ {len(files)} MP3 файл таңдалды")
    
    def clear_mp3_files(self):
        """MP3 тізімін тазалау"""
        self.mp3_files.clear()
        self.mp3_listbox.delete(0, tk.END)
        self.log("MP3 тізімі тазалаңыз")
    
    def select_cover_image(self):
        """Обложка суретін таңдау"""
        file = filedialog.askopenfilename(
            title="Обложка суретін таңдаңыз",
            filetypes=[("Суреттер", "*.jpg *.jpeg *.png *.JPG *.JPEG *.PNG"),
                      ("JPEG файлдары", "*.jpg *.jpeg"), 
                      ("PNG файлдары", "*.png"),
                      ("Барлық файлдар", "*.*")]
        )
        
        if file:
            self.cover_image = file
            filename = os.path.basename(file)
            self.cover_label.config(text=f"✓ Таңдалды: {filename}", foreground="green")
            self.log(f"✓ Обложка таңдалды: {filename}")
    
    def log(self, message):
        """Логка жазу"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.update()
    
    def clear_log(self):
        """Логты тазалау"""
        self.log_text.delete(1.0, tk.END)
    
    def replace_cover_in_mp3(self, mp3_path, cover_path=None, artist=None, title=None, album=None, year=None):
        """MP3 файлының обложкасын және метаданысын өзгерту"""
        try:
            # ID3 тегтерін оқу
            try:
                audio = ID3(mp3_path)
            except ID3NoHeaderError:
                audio = ID3()
            
            # Обложканы өзгерту
            if cover_path:
                # Сурет файлын окылау
                with open(cover_path, 'rb') as f:
                    cover_data = f.read()
                
                # Сурет түрін анықтау
                mime_type = "image/jpeg"
                if cover_path.lower().endswith('.png'):
                    mime_type = "image/png"
                
                # Ескі обложкаларды өшіру
                for key in list(audio.keys()):
                    if key.startswith('APIC'):
                        del audio[key]
                
                # Жаңа обложканы қосу
                audio['APIC:Cover'] = APIC(
                    encoding=3,
                    mime=mime_type,
                    type=3,
                    desc='Cover',
                    data=cover_data
                )
            
            # Исполнителіні өзгерту
            if artist:
                audio['TPE1'] = TPE1(encoding=3, text=[artist])
            
            # Трек атын өзгерту
            if title:
                audio['TIT2'] = TIT2(encoding=3, text=[title])
            
            # Альбомды өзгерту
            if album:
                audio['TALB'] = TALB(encoding=3, text=[album])
            
            # Жылды өзгерту
            if year:
                audio['TDRC'] = TDRC(encoding=3, text=[year])
            
            # Сохранение
            audio.save(mp3_path, v2_version=3)
            return True, "Дұрыс орындалды"
            
        except Exception as e:
            return False, str(e)
    
    def execute_replacement(self):
        """Ауыстыруды орындау"""
        if not self.mp3_files:
            messagebox.showerror("Қате", "MP3 файлдарын таңдаңыз!")
            return
        
        # Өндеу параметрлерін тексеру
        has_cover = bool(self.cover_image)
        has_artist = bool(self.artist_text.get().strip())
        has_title = bool(self.title_text.get().strip())
        has_album = bool(self.album_text.get().strip())
        has_year = bool(self.year_text.get().strip())
        
        if not (has_cover or has_artist or has_title or has_album or has_year):
            messagebox.showerror("Қате", 
                               "Обложка немесе метаданысын (исполнитель, трек т.б) таңдаңыз!")
            return
        
        # Фонда орындау
        thread = threading.Thread(target=self.process_files)
        thread.start()
    
    def process_files(self):
        """Файлдарды өңдеу"""
        self.is_processing = True
        self.execute_btn.config(state=tk.DISABLED)
        
        total = len(self.mp3_files)
        success_count = 0
        error_count = 0
        
        # Өндеу параметрлерін жинау
        artist = self.artist_text.get().strip() if self.artist_text.get() else None
        title = self.title_text.get().strip() if self.title_text.get() else None
        album = self.album_text.get().strip() if self.album_text.get() else None
        year = self.year_text.get().strip() if self.year_text.get() else None
        
        self.log(f"\n{'='*60}")
        self.log(f"ӨҢДЕУ БАСТАЛДЫ / PROCESSING STARTED")
        self.log(f"Барлығы: {total} файл / Total: {total} files")
        self.log(f"{'='*60}")
        
        if self.cover_image:
            self.log(f"🖼️  Обложка: {os.path.basename(self.cover_image)}")
        if artist:
            self.log(f"🎤 Исполнитель: {artist}")
        if title:
            self.log(f"🎵 Трек: {title}")
        if album:
            self.log(f"💿 Альбом: {album}")
        if year:
            self.log(f"📅 Жыл: {year}")
        
        self.log(f"{'='*60}\n")
        
        for index, mp3_path in enumerate(self.mp3_files):
            filename = os.path.basename(mp3_path)
            self.status_label.config(text=f"Өңдеу: {filename}")
            
            success, message = self.replace_cover_in_mp3(
                mp3_path, 
                cover_path=self.cover_image,
                artist=artist,
                title=title,
                album=album,
                year=year
            )
            
            if success:
                self.log(f"✓ [{index+1}/{total}] {filename} - ОК")
                success_count += 1
            else:
                self.log(f"✗ [{index+1}/{total}] {filename} - ҚАТЕ: {message}")
                error_count += 1
            
            # Прогресс жаңарту
            progress = (index + 1) / total * 100
            self.progress_var.set(progress)
            self.root.update()
        
        # Қорытынды
        self.log(f"\n{'='*60}")
        self.log(f"ОРЫНДАЛДЫ / COMPLETED")
        self.log(f"✓ Сәтті: {success_count}")
        self.log(f"✗ Қате: {error_count}")
        self.log(f"{'='*60}\n")
        
        self.status_label.config(text="Дайын / Ready")
        self.execute_btn.config(state=tk.NORMAL)
        self.is_processing = False
        
        messagebox.showinfo("Орындалды", 
                          f"✓ Сәтті: {success_count}\n✗ Қате: {error_count}")

def main():
    root = tk.Tk()
    app = MP3CoverReplacer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
