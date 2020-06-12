"""
CIRCLE-ELD App
By Sandy Lord
github: sandyjameslord
"""
import tkinter as tk
from tkinter import font as tkfont

from PIL import ImageTk, Image

import circle_data as cd
import worksheet_one as w1
import worksheet_two as w2
import worksheet_three as w3
import worksheet_four as w4

class OfferUnitChoicesApp(tk.Tk):

    def __init__(self, theme, unit_number, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.theme = theme
        self.unit_number = unit_number
        self.title_font = tkfont.Font(family='Helvetica', size=35, weight="bold")
        self.big_button_font = tkfont.Font(family='Helvetica', size=45, weight='bold')
        self.small_button_font = tkfont.Font(family='Helvetica', size=15, weight='bold')

        self.image_title_font = tkfont.Font(family='Helvetica', size=20, weight='bold')
        self.italicize_text_font = tkfont.Font(family='Helvetica', size=12, weight='bold', slant='italic')
        self.SIZE = "1500x1000"
        container = tk.Frame(self)
        container.master.geometry(self.SIZE)
        container.master.title("Worksheet Selection")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages_to_view = (OfferUnitChoices,)
        for F in pages_to_view:
            page_name = F.__name__
            frame = F( parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("OfferUnitChoices")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class OfferUnitChoices(tk.Frame):
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
        for theme in self.data:
            for vocab in theme[0]:
                if self.CURRENT_UNIT_NUMBER == vocab.unit and vocab.theme == self.CURRENT_THEME_NAME:
                    toptext = vocab.theme.capitalize() + " Unit " + str(vocab.unit)
        toptext = "CIRCLE-ELD " + toptext + " : Choose a Worksheet"
        toplabel = tk.Label(self, text=toptext, font=controller.title_font)
        toplabel.pack(side="top", pady=5)
        choice1_btn = tk.Button(self, bg='light gray', font=controller.title_font, text="Worksheet One\n--\nIntroduction", command=lambda: go_to_worksheet1(self.theme, self.CURRENT_UNIT_NUMBER)).pack(pady=30)
        choice2_btn = tk.Button(self, bg='light gray', font=controller.title_font, text="Worksheet Two\n--\nListening and Speaking", command=lambda: go_to_worksheet2(self.theme, self.CURRENT_UNIT_NUMBER)).pack(pady=30)
        choice3_btn = tk.Button(self, bg='light gray', font=controller.title_font, text="Worksheet Three\n--\nListening and Questioning", command=lambda: go_to_worksheet3(self.theme, self.CURRENT_UNIT_NUMBER)).pack(pady=30)
        choice4_btn = tk.Button(self, bg='light gray', font=controller.title_font,text="Worksheet Four\n--\nCheck Your Skills",command=lambda: go_to_worksheet4(self.theme, self.CURRENT_UNIT_NUMBER)).pack(pady=30)

        def go_to_worksheet1(theme, unit_number):
            self.controller.destroy()
            app = w1.WorksheetOneApp(theme, unit_number)
            app.mainloop()
        def go_to_worksheet2(theme, unit_number):
            self.controller.destroy()
            app = w2.WorksheetTwoApp(theme, unit_number)
            app.mainloop()
        def go_to_worksheet3(theme, unit_number):
            self.controller.destroy()
            app = w3.WorksheetThreeApp(theme, unit_number)
            app.mainloop()
        def go_to_worksheet4(theme, unit_number):
            self.controller.destroy()
            app = w4.WorksheetFourApp(theme, unit_number)
            app.mainloop()
class WaterStudents(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "Water"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + self.unit.lower() + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_waterunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_waterunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_waterunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_waterunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)


    def go_to_waterunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('water', 1)
        app.mainloop()


    def go_to_waterunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('water', 2)
        app.mainloop()

    def go_to_waterunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('water', 3)
        app.mainloop()

    def go_to_waterunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('water', 4)
        app.mainloop()
class BodyStudents(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "Body"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + self.unit.lower() + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_bodyunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_bodyunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_bodyunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_bodyunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)
    def go_to_bodyunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('body', 1)
        app.mainloop()


    def go_to_bodyunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('body', 2)
        app.mainloop()

    def go_to_bodyunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('body', 3)
        app.mainloop()

    def go_to_bodyunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('body', 4)
        app.mainloop()
class ColorStudents(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "Color"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + self.unit.lower() + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_colorunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_colorunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_colorunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_colorunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)

    def go_to_colorunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('color', 1)
        app.mainloop()


    def go_to_colorunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('color', 2)
        app.mainloop()

    def go_to_colorunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('color', 3)
        app.mainloop()

    def go_to_colorunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('color', 4)
        app.mainloop()
class FallStudents(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "Fall"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + self.unit.lower() + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_fallunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_fallunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_fallunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_fallunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)

    def go_to_fallunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('fall', 1)
        app.mainloop()


    def go_to_fallunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('fall', 2)
        app.mainloop()

    def go_to_fallunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('fall', 3)
        app.mainloop()

    def go_to_fallunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('fall', 4)
        app.mainloop()
class GeographyStudents(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "Geography"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + self.unit.lower() + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_geographyunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_geographyunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_geographyunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_geographyunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)

    def go_to_geographyunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('geography', 1)
        app.mainloop()


    def go_to_geographyunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('geography', 2)
        app.mainloop()

    def go_to_geographyunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('geography', 3)
        app.mainloop()

    def go_to_geographyunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('geography', 4)
        app.mainloop()
class HouseStudents(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "House"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + self.unit.lower() + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_houseunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_houseunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_houseunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_houseunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)

    def go_to_houseunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('house', 1)
        app.mainloop()


    def go_to_houseunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('house', 2)
        app.mainloop()

    def go_to_houseunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('house', 3)
        app.mainloop()

    def go_to_houseunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('house', 4)
        app.mainloop()
class PlantsStudents(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "Plants"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + self.unit.lower() + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_plantsunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_plantsunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_plantsunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_plantsunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)

    def go_to_plantsunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('plants', 1)
        app.mainloop()


    def go_to_plantsunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('plants', 2)
        app.mainloop()

    def go_to_plantsunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('plants', 3)
        app.mainloop()

    def go_to_plantsunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('plants', 4)
        app.mainloop()
class SpaceStudents(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "Space"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + self.unit.lower() + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_spaceunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_spaceunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_spaceunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_spaceunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)

    def go_to_spaceunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('space', 1)
        app.mainloop()


    def go_to_spaceunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('space', 2)
        app.mainloop()

    def go_to_spaceunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('space', 3)
        app.mainloop()

    def go_to_spaceunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('space', 4)
        app.mainloop()
class TransportationStudents(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "Transportation"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + self.unit.lower() + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_transportationunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_transportationunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_transportationunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_transportationunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)

    def go_to_transportationunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('transportation', 1)
        app.mainloop()


    def go_to_transportationunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('transportation', 2)
        app.mainloop()

    def go_to_transportationunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('transportation', 3)
        app.mainloop()

    def go_to_transportationunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('transportation', 4)
        app.mainloop()
class WorldCultureStudents(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unit = "WorldCulture"
        self.background_image_path = "circle_images/" + self.unit + "Images/" + "world_culture" + "_background.jpg"
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open(self.background_image_path))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename
        title_label = tk.Label(self, text=" " + self.unit + " ", font=controller.title_font)
        title_label.pack(side="top", padx=10, pady=20)
        self.unit_image_path = "circle_images/" + self.unit + "Images/" + self.unit + "UnitImages/" + self.unit + "Unit"
        imgUnit1 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "1.jpg"))
        imgUnit2 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "2.jpg"))
        imgUnit3 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "3.jpg"))
        imgUnit4 = ImageTk.PhotoImage(Image.open(self.unit_image_path + "4.jpg"))

        images_frame = tk.Frame(self, bg='black')

        button_unit_1 = tk.Button(images_frame, image=imgUnit1, command=self.go_to_world_cultureunit1)
        button_unit_1.image = imgUnit1
        button_unit_1.pack(side="left", padx=5)
        button_unit_2 = tk.Button(images_frame, image=imgUnit2, command=self.go_to_world_cultureunit2)
        button_unit_2.image = imgUnit2
        button_unit_2.pack(side="left", padx=5)
        button_unit_3 = tk.Button(images_frame, image=imgUnit3, command=self.go_to_world_cultureunit3)
        button_unit_3.image = imgUnit3
        button_unit_3.pack(side="left", padx=5)
        button_unit_4 = tk.Button(images_frame, image=imgUnit4, command=self.go_to_world_cultureunit4)
        button_unit_4.image = imgUnit4
        button_unit_4.pack(side="left", padx=5)
        images_frame.pack(padx=20, pady=125)
        button = tk.Button(self, font=controller.big_button_font, text="Main Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=40)

    def go_to_world_cultureunit1(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('worldculture', 1)
        app.mainloop()


    def go_to_world_cultureunit2(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('worldculture', 2)
        app.mainloop()

    def go_to_world_cultureunit3(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('worldculture', 3)
        app.mainloop()

    def go_to_world_cultureunit4(self):
        self.controller.destroy()
        app = OfferUnitChoicesApp('worldculture', 4)
        app.mainloop()

if __name__ == "__main__":
    app = OfferUnitChoicesApp('fall', 2)
    app.mainloop()