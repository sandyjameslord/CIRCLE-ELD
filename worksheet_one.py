"""
CIRCLE-ELD App
By Sandy Lord
github: sandyjameslord
"""
import tkinter as tk
from tkinter import font as tkfont
from PIL import ImageTk, Image
from watson_developer_cloud import TextToSpeechV1
import keys
import pydub
import pydub.playback
import circle_data as cd

class WorksheetOneApp(tk.Tk):

    def __init__(self, theme, unit_number, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.theme = theme
        self.unit_number = unit_number
        self.title_font = tkfont.Font(family='Helvetica', size=80, weight="bold")
        self.info_display_font = tkfont.Font(family='Helvetica', size=20, weight='bold')
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
        container.master.title("Worksheet One: Introduction")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages_to_view = (WorksheetOne,Instructions)
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

class WorksheetOne(tk.Frame):
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
        toptext = ""
        textab = []
        textbc = []
        for theme in self.data:
            for vocab in theme[0]:
                if self.CURRENT_UNIT_NUMBER == vocab.unit and vocab.theme == self.CURRENT_THEME_NAME:
                    toptext = vocab.theme.capitalize() + " Unit " + str(vocab.unit)
                    textab.append(vocab.ab_sent)
                    textbc.append(vocab.bc_sent)
        toptext = "CIRCLE-ELD " + toptext + " : Listen, Read, and Question"
        toplabel = tk.Label(self, text=toptext, font=controller.instructions_font)
        toplabel.pack(side="top", pady=2)

        image_at_hand_label = tk.Label(self)
        information_label = tk.Label(self)
        buttons_frame = tk.Frame(self, bg='black')

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
        images = [image1, image2, image3, image4, image5, image6, image7, image8, image9, image10]
        vocab1, vocab2, vocab3, vocab4, vocab5, vocab6, vocab7, vocab8, vocab9, vocab10 = "","","","","","","","","",""
        vocabs = [vocab1, vocab2, vocab3, vocab4, vocab5, vocab6, vocab7, vocab8, vocab9, vocab10]
        syll1, syll2, syll3, syll4, syll5, syll6, syll7, syll8, syll9, syll10 = "","","","","","","","","",""
        sylls = [syll1, syll2, syll3, syll4, syll5, syll6, syll7, syll8, syll9, syll10]
        sentab1, sentab2, sentab3, sentab4, sentab5, sentab6, sentab7, sentab8, sentab9, sentab10 = "", "","","","","","","","",""
        sent_abs = [sentab1, sentab2, sentab3, sentab4, sentab5, sentab6, sentab7, sentab8, sentab9, sentab10]
        sentbc1, sentbc2, sentbc3, sentbc4, sentbc5, sentbc6, sentbc7, sentbc8, sentbc9, sentbc10 = "", "","","","","","","","",""
        sent_bcs = [sentbc1, sentbc2, sentbc3, sentbc4, sentbc5, sentbc6, sentbc7, sentbc8, sentbc9, sentbc10]
        question_type_ab1, question_type_ab2, question_type_ab3, question_type_ab4, question_type_ab5, question_type_ab6, question_type_ab7, question_type_ab8, question_type_ab9, question_type_ab10 = "", "","","","","","","","",""
        question_type_abs = [question_type_ab1, question_type_ab2, question_type_ab3, question_type_ab4, question_type_ab5, question_type_ab6, question_type_ab7, question_type_ab8, question_type_ab9, question_type_ab10]
        questionab1, questionab2, questionab3, questionab4, questionab5, questionab6, questionab7, questionab8, questionab9, questionab10 = "", "","","","","","","","",""
        question_abs = [questionab1, questionab2, questionab3, questionab4, questionab5, questionab6, questionab7, questionab8, questionab9, questionab10]
        question_type_bc1, question_type_bc2, question_type_bc3, question_type_bc4, question_type_bc5, question_type_bc6, question_type_bc7, question_type_bc8, question_type_bc9, question_type_bc10 = "", "","","","","","","","",""
        question_type_bcs = [question_type_bc1, question_type_bc2, question_type_bc3, question_type_bc4, question_type_bc5, question_type_bc6, question_type_bc7, question_type_bc8, question_type_bc9, question_type_bc10]
        questionbc1, questionbc2, questionbc3, questionbc4, questionbc5, questionbc6, questionbc7, questionbc8, questionbc9, questionbc10 = "", "","","","","","","","",""
        question_bcs = [questionbc1, questionbc2, questionbc3, questionbc4, questionbc5, questionbc6, questionbc7, questionbc8, questionbc9, questionbc10]

        info_at_hand_display_label = tk.Label(self, padx=10, pady=10, font=controller.info_display_font, wraplength=1200, width=100, justify='left')

        vocab_button = tk.Button(buttons_frame, text="Vocabulary", font=controller.small_button_font, bg='black')
        ab_sent_button = tk.Button(buttons_frame, text='Sent 1', font=controller.small_button_font, bg='gray')
        bc_sent_button = tk.Button(buttons_frame, text='Sent 2', font=controller.small_button_font, bg='gray')
        ab_question_button = tk.Button(buttons_frame, text='Question 1', font=controller.small_button_font, bg='gray')
        bc_question_button = tk.Button(buttons_frame, text='Question 2', font=controller.small_button_font, bg='gray')

        for theme in self.data:
            for vocab in theme[0]:
                if self.CURRENT_UNIT_NUMBER == vocab.unit and vocab.theme == self.CURRENT_THEME_NAME:
                    for i in range(10):
                        if not vocabs[i]:
                            vocabs[i] = vocab.vocabulary
                            sylls[i] = vocab.syll_structure
                            sent_abs[i] = vocab.ab_sent
                            sent_bcs[i] = vocab.bc_sent
                            question_type_abs[i] = vocab.ab_question_domain
                            question_abs[i] = vocab.ab_question
                            question_type_bcs[i] = vocab.bc_question_domain
                            question_bcs[i] = vocab.bc_question
                            break

        def to_speak(text_to_speak, voice_to_use, file_name):
            tts = TextToSpeechV1(iam_apikey=keys.text_to_speech_key)
            with open(file_name, 'wb') as audio_file:
                audio_file.write(tts.synthesize(text_to_speak,
                                                accept='audio/wav', voice=voice_to_use).get_result().content)
            sound = pydub.AudioSegment.from_wav(file_name)
            pydub.playback.play(sound)


        def set_image_and_text_and_buttons(image_number):
            info_at_hand_display_label['text'] = "Click a button to display text"
            image_number = image_number - 1
            image_at_hand_label['image'] = images[image_number]
            image_at_hand_label.pack(pady=2)
            def set_vocab_and_syll_info_before_display(image_number):
                text = vocabs[image_number]
                to_speak(text, 'en-US_AllisonVoice', 'audio1.wav')
                info_at_hand_display_label['text'] = text
                info_at_hand_display_label.pack()
            def set_absentence_info_before_display(image_number):
                text = sent_abs[image_number]
                to_speak(text, 'en-US_AllisonVoice', 'audio1.wav')
                info_at_hand_display_label['text'] = text
                info_at_hand_display_label.pack()
            def set_bcsentence_info_before_display(image_number):
                text = sent_bcs[image_number]
                to_speak(text, 'en-US_AllisonVoice', 'audio1.wav')
                info_at_hand_display_label['text'] = text
                info_at_hand_display_label.pack()
            def set_abquestion_info_before_display(image_number):
                text = question_abs[image_number]
                to_speak(text, 'en-US_AllisonVoice', 'audio1.wav')
                info_at_hand_display_label['text'] = text
                info_at_hand_display_label.pack()
            def set_bcquestion_info_before_display(image_number):
                text = question_bcs[image_number]
                to_speak(text, 'en-US_AllisonVoice', 'audio1.wav')
                info_at_hand_display_label['text'] = text
                info_at_hand_display_label.pack()
            vocab_button['command'] = lambda: set_vocab_and_syll_info_before_display(image_number)
            vocab_button.pack(side='left', padx=10, pady=1)
            ab_sent_button['command'] = lambda: set_absentence_info_before_display(image_number)
            ab_sent_button.pack(side='left', padx=10, pady=1)
            bc_sent_button['command'] = lambda: set_bcsentence_info_before_display(image_number)
            bc_sent_button.pack(side='left', padx=10, pady=1)
            ab_question_button['command'] = lambda: set_abquestion_info_before_display(image_number)
            ab_question_button.pack(side='left', padx=10, pady=1)
            bc_question_button['command'] = lambda: set_bcquestion_info_before_display(image_number)
            bc_question_button.pack(side='left', padx=10, pady=1)
            buttons_frame.pack(side='bottom', pady=2)

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
        thumbnail_text1 = f" {self.CURRENT_UNIT[0]} 1"
        thumbnail_text2 = f" {self.CURRENT_UNIT[0]} 2"
        thumbnail_text3 = f" {self.CURRENT_UNIT[1]} 1"
        thumbnail_text4 = f" {self.CURRENT_UNIT[1]} 2"
        thumbnail_text5 = f" {self.CURRENT_UNIT[2]} 1"
        thumbnail_text6 = f" {self.CURRENT_UNIT[2]} 2"
        thumbnail_text7 = f" {self.CURRENT_UNIT[3]} 1"
        thumbnail_text8 = f" {self.CURRENT_UNIT[3]} 2"
        thumbnail_text9 = f" {self.CURRENT_UNIT[4]} 1"
        thumbnail_text10 = f" {self.CURRENT_UNIT[4]} 2"
        thumbnail_frame = tk.Frame(self)
        voc1btn = tk.Button(thumbnail_frame, text=thumbnail_text1, compound='top', image=thumbnail1, command = lambda: set_image_and_text_and_buttons(1))
        voc1btn.image = thumbnail1
        voc1btn.pack(side="left", padx=2)
        voc2btn = tk.Button(thumbnail_frame, text=thumbnail_text2, compound='top', image=thumbnail2,command = lambda: set_image_and_text_and_buttons(2))
        voc2btn.image = thumbnail2
        voc2btn.pack(side="left", padx=2)
        voc3btn = tk.Button(thumbnail_frame, text=thumbnail_text3, compound='top', image=thumbnail3,command = lambda: set_image_and_text_and_buttons(3))
        voc3btn.image = thumbnail3
        voc3btn.pack(side="left", padx=2)
        voc4btn = tk.Button(thumbnail_frame, text=thumbnail_text4, compound='top', image=thumbnail4,command = lambda: set_image_and_text_and_buttons(4))
        voc4btn.image = thumbnail4
        voc4btn.pack(side="left", padx=2)
        voc5btn = tk.Button(thumbnail_frame, text=thumbnail_text5, compound='top', image=thumbnail5,command = lambda: set_image_and_text_and_buttons(5))
        voc5btn.image = thumbnail5
        voc5btn.pack(side="left", padx=2)
        voc6btn = tk.Button(thumbnail_frame, text=thumbnail_text6, compound='top', image=thumbnail6,command = lambda: set_image_and_text_and_buttons(6))
        voc6btn.image = thumbnail6
        voc6btn.pack(side="left", padx=2)
        voc7btn = tk.Button(thumbnail_frame, text=thumbnail_text7, compound='top', image=thumbnail7,command = lambda: set_image_and_text_and_buttons(7))
        voc7btn.image = thumbnail7
        voc7btn.pack(side="left", padx=2)
        voc8btn = tk.Button(thumbnail_frame, text=thumbnail_text8, compound='top', image=thumbnail8,command = lambda: set_image_and_text_and_buttons(8))
        voc8btn.image = thumbnail8
        voc8btn.pack(side="left", padx=2)
        voc9btn = tk.Button(thumbnail_frame, text=thumbnail_text9, compound='top', image=thumbnail9,command = lambda: set_image_and_text_and_buttons(9))
        voc9btn.image = thumbnail9
        voc9btn.pack(side="left", padx=2)
        voc10btn = tk.Button(thumbnail_frame, text=thumbnail_text10, compound='top', image=thumbnail10,command = lambda: set_image_and_text_and_buttons(10))
        voc10btn.image = thumbnail10
        voc10btn.pack(side="left", padx=2)

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
        instructions_button = tk.Button(options_frame, text='Instructions', font=controller.smaller_button_font, width=20,
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

        instructions_text = f"""1. Click on a picture

2. Listen to the words and the sentences -- 
    -- Try and say each of them. 

3. Listen to the questions and discuss --
    -- No worries, just say what you think!"""
        instructions_frame = tk.Frame(self, bg='SlateGray3')
        introduction_text_header = tk.Label(instructions_frame,
                                            text=f"Introduction for {self.theme.capitalize()} Unit {self.unit_number}\nWorksheet One: 'Introduction'",
                                            font=controller.instructions_title_font, bg='DarkSeaGreen3')
        proceed_to_worksheet_button = tk.Button(instructions_frame, bg='SlateGray1', text="To the Lesson",
                                                font=controller.huge_button_font,
                                                command=lambda: controller.show_frame("WorksheetOne"))
        instruction_text_label = tk.Label(instructions_frame, bg='SlateGray3', width=100, text=instructions_text,
                                          font=controller.instructions_font, justify='left')
        introduction_text_header.pack(pady=10)
        instruction_text_label.pack(pady=10)
        proceed_to_worksheet_button.pack(pady=10)
        instructions_frame.pack(expand=True, fill='both')


if __name__ == "__main__":
    app = WorksheetOneApp('space', 1)
    app.mainloop()