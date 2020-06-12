"""
CIRCLE-ELD App
By Sandy Lord
github: sandyjameslord
"""
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox as mb
from watson_developer_cloud import TextToSpeechV1
import keys
import pydub
import pydub.playback
from PIL import ImageTk, Image
import circle_data as cd
import wave
import time
#import pyaudio







class WorksheetThreeApp(tk.Tk):

    def __init__(self, theme, unit_number, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.theme = theme
        self.unit_number = unit_number
        self.title_font = tkfont.Font(family='Helvetica', size=80, weight="bold")
        self.instructions_title_font = tkfont.Font(family='Helvetica', size=65, weight='bold')
        self.big_button_font = tkfont.Font(family='Helvetica', size=60, weight='bold')
        self.small_button_font = tkfont.Font(family='Helvetica', size=25, weight='bold')
        self.smaller_button_font = tkfont.Font(family='Helvetica', size=18, weight='bold')
        self.image_title_font = tkfont.Font(family='Helvetica', size=35, weight='bold')
        self.italicize_text_font = tkfont.Font(family='Helvetica', size=12, weight='bold', slant='italic')
        self.instructions_font = tkfont.Font(family='Helvetica', size=40, weight='bold')
        self.huge_button_font = tkfont.Font(family='Helvetica', size=80, weight='bold')
        self.SIZE = "1500x1000"
        container = tk.Frame(self)
        container.master.geometry(self.SIZE)
        container.master.title("Worksheet Three: 'Listening and Responding'")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages_to_view = (WorksheetThree, Instructions)
        for F in pages_to_view:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Instructions")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class WorksheetThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open("circle_images/indiv_background_for_now.jpg"))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename

        def create_data():
            database = r"circle_db.db"
            conn = cd.create_connection(database)
            theme_names = ['body', 'color', 'fall', 'geography', 'house', 'plants', 'space', 'transportation', 'water', 'worldculture']
            themes = []
            for th in theme_names:
                local_theme = []
                with conn:
                    images = cd.create_theme_infos(conn, th)
                    local_theme.append(images)
                themes.append(local_theme)
            return themes
        self.theme = controller.theme
        self.unit_number = controller.unit_number
        self.data = create_data()
        self.CURRENT_THEME_NAME = self.theme
        self.CURRENT_UNIT_NUMBER = self.unit_number
        self.CURRENT_UNIT = []
        self.CURRENT_UNIT_IMAGES = []
        self.CURRENT_UNIT_PASCAL = []
        self.CURRENT_UNIT_NAME = ""
        for item in self.data:
            for vocab in item[0]:
                if vocab.theme == self.CURRENT_THEME_NAME and vocab.unit == self.CURRENT_UNIT_NUMBER:
                    if vocab.vocabulary not in self.CURRENT_UNIT:
                        self.CURRENT_UNIT.append(vocab.vocabulary)
                    image_word = ""
                    local_word = vocab.vocabulary.lower()
                    for char in local_word:
                        if char.isalnum():
                            image_word += char
                        else:
                            image_word += "_"
                    if image_word not in self.CURRENT_UNIT_IMAGES:
                        self.CURRENT_UNIT_IMAGES.append(image_word)
                    local_pascal_word = ""
                    local_pascal_words = vocab.vocabulary.split(" ")
                    for word in local_pascal_words:
                        word.capitalize()
                        local_pascal_word += word
                    if local_pascal_word not in self.CURRENT_UNIT_PASCAL:
                        self.CURRENT_UNIT_PASCAL.append(local_pascal_word)
        toplabel = tk.Label(self, text="Worksheet Two: Listening and Speaking", font=controller.image_title_font)
        toplabel.pack(side="top", pady=2)

        textab = []
        textbc = []

        for theme in self.data:
            for vocab in theme[0]:
                if self.CURRENT_UNIT_NUMBER == vocab.unit and vocab.theme == self.CURRENT_THEME_NAME:
                    textab.append(vocab.ab_question)
                    textbc.append(vocab.bc_question)

        sent_label = tk.Label(self, font=controller.small_button_font, wraplength=1200, width=100, justify='left')
        path_standardized_images = "circle_images/" + self.CURRENT_THEME_NAME.capitalize() + "Images/" + self.CURRENT_THEME_NAME.capitalize() + "StandardizedImages/"
        path_thumbnail_images = "circle_images/" + self.CURRENT_THEME_NAME.capitalize() + "Images/" + self.CURRENT_THEME_NAME.capitalize() + "Thumbnails/"
        image1 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[0] + "01.jpg"))
        image2 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[0] + "02.jpg"))
        image3 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[1] + "01.jpg"))
        image4 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[1] + "02.jpg"))
        image5 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[2] + "01.jpg"))
        image6 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[2] + "02.jpg"))
        image7 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[3] + "01.jpg"))
        image8 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[3] + "02.jpg"))
        image9 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[4] + "01.jpg"))
        image10 = ImageTk.PhotoImage(Image.open(path_standardized_images + self.CURRENT_UNIT_IMAGES[4] + "02.jpg"))
        small_holder = ImageTk.PhotoImage(Image.open("circle_images/small_blue_holder.jpg"))
        image_at_hand_label = tk.Label(self)
        playback_button = tk.Button(self, text="Play again", font=controller.image_title_font)
        def to_speak(text_to_speak, voice_to_use, file_name):
            tts = TextToSpeechV1(iam_apikey=keys.text_to_speech_key)
            with open(file_name, 'wb') as audio_file:
                audio_file.write(tts.synthesize(text_to_speak,
                                                accept='audio/wav', voice=voice_to_use).get_result().content)
            sound = pydub.AudioSegment.from_wav(file_name)
            pydub.playback.play(sound)

        def set_image_and_text_and_playback_button(image_number, text_to_speak, voice_to_use, file_name, ab_or_bc):
            image_at_hand_label['image'] = small_holder
            image_at_hand_label['image'] = image_number
            image_at_hand_label.pack()
            numba = int(str(image_number)[-1]) - 2
            if ab_or_bc == "ab":
                sent_label['text'] = ""*200
                sent_label['text'] = text_to_speak
                sent_label.pack(padx=10, pady=10)
            else:
                sent_label['text'] = ""*200
                sent_label['text'] = text_to_speak
                sent_label.pack(padx=10, pady=10)

            playback_button['command'] = lambda: to_speak(text_to_speak, voice_to_use, file_name)
            playback_button.pack(padx=10, pady=10)

        def text_to_speech(text_to_speak, voice_to_use, file_name, image_number, ab_or_bc):
            set_image_and_text_and_playback_button(image_number, text_to_speak, voice_to_use, file_name, ab_or_bc)
            controller.after(0, to_speak(text_to_speak, voice_to_use, file_name))

        thumbnail1 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[0] + "01thm.jpg"))
        thumbnail2 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[0] + "02thm.jpg"))
        thumbnail3 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[1] + "01thm.jpg"))
        thumbnail4 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[1] + "02thm.jpg"))
        thumbnail5 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[2] + "01thm.jpg"))
        thumbnail6 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[2] + "02thm.jpg"))
        thumbnail7 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[3] + "01thm.jpg"))
        thumbnail8 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[3] + "02thm.jpg"))
        thumbnail9 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[4] + "01thm.jpg"))
        thumbnail10 = ImageTk.PhotoImage(Image.open(path_thumbnail_images + self.CURRENT_UNIT_IMAGES[4] + "02thm.jpg"))

        text1 = f" {self.CURRENT_UNIT[0]} 1"
        text2 = f" {self.CURRENT_UNIT[0]} 2"
        text3 = f" {self.CURRENT_UNIT[1]} 1"
        text4 = f" {self.CURRENT_UNIT[1]} 2"
        text5 = f" {self.CURRENT_UNIT[2]} 1"
        text6 = f" {self.CURRENT_UNIT[2]} 2"
        text7 = f" {self.CURRENT_UNIT[3]} 1"
        text8 = f" {self.CURRENT_UNIT[3]} 2"
        text9 = f" {self.CURRENT_UNIT[4]} 1"
        text10 = f" {self.CURRENT_UNIT[4]} 2"
        thumbnail_frame = tk.Frame(self)

        ab_bc_buttons_frame = tk.Frame(thumbnail_frame)
        def toggle_ab():
            toggle_bc_button['fg'] = 'black'
            toggle_ab_button['fg'] = 'green'
            voc1btn['command'] = lambda: text_to_speech(textab[0], 'en-US_AllisonVoice', 'audio1.wav', image1, "ab")
            voc2btn['command'] = lambda: text_to_speech(textab[1], 'en-US_AllisonVoice', 'audio1.wav', image2, "ab")
            voc3btn['command'] = lambda: text_to_speech(textab[2], 'en-US_AllisonVoice', 'audio1.wav', image3, "ab")
            voc4btn['command'] = lambda: text_to_speech(textab[3], 'en-US_AllisonVoice', 'audio1.wav', image4, "ab")
            voc5btn['command'] = lambda: text_to_speech(textab[4], 'en-US_AllisonVoice', 'audio1.wav', image5, "ab")
            voc6btn['command'] = lambda: text_to_speech(textab[5], 'en-US_AllisonVoice', 'audio1.wav', image6, "ab")
            voc7btn['command'] = lambda: text_to_speech(textab[6], 'en-US_AllisonVoice', 'audio1.wav', image7, "ab")
            voc8btn['command'] = lambda: text_to_speech(textab[7], 'en-US_AllisonVoice', 'audio1.wav', image8, "ab")
            voc9btn['command'] = lambda: text_to_speech(textab[8], 'en-US_AllisonVoice', 'audio1.wav', image9, "ab")
            voc10btn['command'] = lambda: text_to_speech(textab[9], 'en-US_AllisonVoice', 'audio1.wav', image10, "ab")

        def toggle_bc():
            toggle_bc_button['fg'] = 'green'
            toggle_ab_button['fg'] = 'black'
            voc1btn['command'] = lambda: text_to_speech(textbc[0], 'en-US_AllisonVoice', 'audio1.wav', image1, "bc")
            voc2btn['command'] = lambda: text_to_speech(textbc[1], 'en-US_AllisonVoice', 'audio1.wav', image2, "bc")
            voc3btn['command'] = lambda: text_to_speech(textbc[2], 'en-US_AllisonVoice', 'audio1.wav', image3, "bc")
            voc4btn['command'] = lambda: text_to_speech(textbc[3], 'en-US_AllisonVoice', 'audio1.wav', image4, "bc")
            voc5btn['command'] = lambda: text_to_speech(textbc[4], 'en-US_AllisonVoice', 'audio1.wav', image5, "bc")
            voc6btn['command'] = lambda: text_to_speech(textbc[5], 'en-US_AllisonVoice', 'audio1.wav', image6, "bc")
            voc7btn['command'] = lambda: text_to_speech(textbc[6], 'en-US_AllisonVoice', 'audio1.wav', image7, "bc")
            voc8btn['command'] = lambda: text_to_speech(textbc[7], 'en-US_AllisonVoice', 'audio1.wav', image8, "bc")
            voc9btn['command'] = lambda: text_to_speech(textbc[8], 'en-US_AllisonVoice', 'audio1.wav', image9, "bc")
            voc10btn['command'] = lambda: text_to_speech(textbc[9], 'en-US_AllisonVoice', 'audio1.wav', image10, "bc")

        toggle_ab_button = tk.Button(ab_bc_buttons_frame, text="AB", font=controller.small_button_font, command=lambda:toggle_ab(), fg='green')
        toggle_bc_button = tk.Button(ab_bc_buttons_frame, text='BC', font=controller.small_button_font, command=lambda:toggle_bc())
        toggle_ab_button.pack()
        toggle_bc_button.pack()
        ab_bc_buttons_frame.pack(side='left', padx=20)
        voc1btn = tk.Button(thumbnail_frame, text=text1, compound='top', image=thumbnail1, command = lambda: text_to_speech(textab[0], 'en-US_AllisonVoice', 'audio1.wav', image1, "ab"))
        voc1btn.image = thumbnail1
        voc1btn.flash()
        voc1btn.pack(side="left", padx=2)
        voc2btn = tk.Button(thumbnail_frame, text=text2, compound='top', image=thumbnail2,command = lambda: text_to_speech(textab[1], 'en-US_AllisonVoice', 'audio1.wav', image2, "ab"))
        voc2btn.image = thumbnail2
        voc2btn.pack(side="left", padx=2)
        voc3btn = tk.Button(thumbnail_frame, text=text3, compound='top', image=thumbnail3,command = lambda: text_to_speech(textab[2], 'en-US_AllisonVoice', 'audio1.wav', image3, "ab"))
        voc3btn.image = thumbnail3
        voc3btn.pack(side="left", padx=2)
        voc4btn = tk.Button(thumbnail_frame, text=text4, compound='top', image=thumbnail4,command = lambda: text_to_speech(textab[3], 'en-US_AllisonVoice', 'audio1.wav', image4, "ab"))
        voc4btn.image = thumbnail4
        voc4btn.pack(side="left", padx=2)
        voc5btn = tk.Button(thumbnail_frame, text=text5, compound='top', image=thumbnail5,command = lambda: text_to_speech(textab[4], 'en-US_AllisonVoice', 'audio1.wav', image5, "ab"))
        voc5btn.image = thumbnail5
        voc5btn.pack(side="left", padx=2)
        voc6btn = tk.Button(thumbnail_frame, text=text6, compound='top', image=thumbnail6,command = lambda: text_to_speech(textab[5], 'en-US_AllisonVoice', 'audio1.wav', image6, "ab"))
        voc6btn.image = thumbnail6
        voc6btn.pack(side="left", padx=2)
        voc7btn = tk.Button(thumbnail_frame, text=text7, compound='top', image=thumbnail7,command = lambda: text_to_speech(textab[6], 'en-US_AllisonVoice', 'audio1.wav', image7, "ab"))
        voc7btn.image = thumbnail7
        voc7btn.pack(side="left", padx=2)
        voc8btn = tk.Button(thumbnail_frame, text=text8, compound='top', image=thumbnail8,command = lambda: text_to_speech(textab[7], 'en-US_AllisonVoice', 'audio1.wav', image8, "ab"))
        voc8btn.image = thumbnail8
        voc8btn.pack(side="left", padx=2)
        voc9btn = tk.Button(thumbnail_frame, text=text9, compound='top', image=thumbnail9,command = lambda: text_to_speech(textab[8], 'en-US_AllisonVoice', 'audio1.wav', image9, "ab"))
        voc9btn.image = thumbnail9
        voc9btn.pack(side="left", padx=2)
        voc10btn = tk.Button(thumbnail_frame, text=text10, compound='top', image=thumbnail10,command = lambda: text_to_speech(textab[9], 'en-US_AllisonVoice', 'audio1.wav', image10, "ab"))
        voc10btn.image = thumbnail10
        voc10btn.pack(side="left", padx=2)

        return_frame = tk.Frame(thumbnail_frame)

        to_unit_button = tk.Button(return_frame,
                                   text='Unit Worksheets', width=15,
                                   command=lambda: go_to_unit_selection())
        to_unit_button.pack(padx=5)
        to_main_menu_button = tk.Button(return_frame, text="Main Menu", width=15,  command=lambda: go_to_main_menu())
        to_main_menu_button.pack(padx=5)
        def go_to_main_menu():
            import main as main_menu
            self.controller.destroy()
            app = main_menu.MainMenuGui()
            app.mainloop()

        def go_to_unit_selection():
            import offer_choices_per_unit as choices
            self.controller.destroy()
            app = choices.OfferUnitChoicesApp(self.theme, self.unit_number)
            app.mainloop()

        options_frame = tk.Frame(thumbnail_frame)
        instructions_button = tk.Button(options_frame, text='Instructions', font=controller.smaller_button_font,
                                        width=20,
                                        command=lambda: controller.show_frame("Instructions")).pack(pady=2)
        to_unit_button = tk.Button(options_frame, text=f'{self.theme.capitalize()} {self.unit_number}\nWorksheets',
                                   width=20, font=controller.smaller_button_font,
                                   command=lambda: go_to_unit_selection()).pack(pady=2)
        to_main_menu_button = tk.Button(options_frame, text="Main Menu", width=20, command=lambda: go_to_main_menu(),
                                        font=controller.smaller_button_font).pack(pady=2)
        options_frame.pack(side='left', padx=30)
        thumbnail_frame.pack(side="bottom")


class Instructions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open("circle_images/indiv_background_for_now.jpg"))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename

        def create_data():
            database = r"circle_db.db"
            conn = cd.create_connection(database)
            theme_names = ['body', 'color', 'fall', 'geography', 'house', 'plants', 'space', 'transportation', 'water',
                           'worldculture']
            themes = []
            for th in theme_names:
                local_theme = []
                with conn:
                    images = cd.create_theme_infos(conn, th)
                    local_theme.append(images)
                themes.append(local_theme)
            return themes

        self.theme = controller.theme
        self.unit_number = controller.unit_number
        self.data = create_data()
        self.CURRENT_THEME_NAME = self.theme
        self.CURRENT_UNIT_NUMBER = self.unit_number
        self.CURRENT_UNIT = []
        self.CURRENT_UNIT_IMAGES = []
        self.CURRENT_UNIT_PASCAL = []
        self.CURRENT_UNIT_NAME = ""
        for item in self.data:
            for vocab in item[0]:
                if vocab.theme == self.CURRENT_THEME_NAME and vocab.unit == self.CURRENT_UNIT_NUMBER:
                    if vocab.vocabulary not in self.CURRENT_UNIT:
                        self.CURRENT_UNIT.append(vocab.vocabulary)
                    image_word = ""
                    local_word = vocab.vocabulary.lower()
                    for char in local_word:
                        if char.isalnum():
                            image_word += char
                        else:
                            image_word += "_"
                    if image_word not in self.CURRENT_UNIT_IMAGES:
                        self.CURRENT_UNIT_IMAGES.append(image_word)
                    local_pascal_word = ""
                    local_pascal_words = vocab.vocabulary.split(" ")
                    for word in local_pascal_words:
                        word.capitalize()
                        local_pascal_word += word
                    if local_pascal_word not in self.CURRENT_UNIT_PASCAL:
                        self.CURRENT_UNIT_PASCAL.append(local_pascal_word)

        instructions_text = f"""1.  Click on a picture

2.  Listen to the questions-- 
    --Respond to them
    --Give your own ideas

3.  AB questions and BC questions are
    appropriate for everyone, but BC
    questions sometimes have more
    challenging vocabulary."""
        instructions_frame = tk.Frame(self, bg='SlateGray3')
        introduction_text_header = tk.Label(instructions_frame,
                                            text=f"Introduction for {self.theme.capitalize()} Unit {self.unit_number}\nWorksheet Three: 'Listening and Responding'",
                                            font=controller.instructions_title_font, bg='DarkSeaGreen3')
        proceed_to_worksheet_button = tk.Button(instructions_frame, bg='SlateGray1', text="To the Lesson",
                                                font=controller.huge_button_font,
                                                command=lambda: controller.show_frame("WorksheetThree"))
        instruction_text_label = tk.Label(instructions_frame, bg='SlateGray3', width=100, text=instructions_text,
                                          font=controller.instructions_font, justify='left')
        introduction_text_header.pack(pady=10)
        instruction_text_label.pack(pady=10)
        proceed_to_worksheet_button.pack(pady=10)
        instructions_frame.pack(expand=True, fill='both')

if __name__ == "__main__":
    app = WorksheetThreeApp('body', 1)
    app.mainloop()