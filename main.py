"""
CIRCLE-ELD App
By Sandy Lord
github: sandyjameslord
"""
import tkinter as tk
from tkinter import font as tkfont
from PIL import ImageTk, Image
import circle_data as cd
import offer_choices_per_unit as otc



SIZE = "1280x800"
database = r"circle_db.db"
conn = cd.create_connection(database)
theme_names = ['body', 'color', 'house', 'plants', 'geography', 'space', 'fall', 'transportation', 'world culture', 'water']
themes = []
for th in theme_names:
    local_theme = []
    with conn:
        images = cd.create_theme_infos(conn, th)
        local_theme.append(images)
    themes.append(local_theme)



class MainMenuGui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=80, weight="bold")
        self.big_button_font = tkfont.Font(family='Helvetica', size=50, weight='bold')
        self.biggest_button_font = tkfont.Font(family='Helvetica', size=100, weight='bold')
        self.small_button_font = tkfont.Font(family='Helvetica', size=25, weight='bold')
        self.image_title_font = tkfont.Font(family='Helvetica', size=35, weight='bold')
        container = tk.Frame(self)
        container.master.geometry(SIZE)
        container.master.title("CIRCLE-ELD")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (
        StartPage, Students, Teachers, Parents, Districts, WaterStudents, BodyStudents, ColorStudents, FallStudents, GeographyStudents, HouseStudents,
        PlantsStudents, SpaceStudents, TransportationStudents, WorldCultureStudents):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open("circle_images/background.jpg"))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image = filename

        label = tk.Label(self, text="""CIRCLE-ELD Main Page""", font=controller.title_font)
        label.pack(side="top", padx=10, pady=10)
        c.pack()
        parents_teachers_districts_frame = tk.Frame(self, bg='black')
        students_button = tk.Button(self, text="Students", font=controller.biggest_button_font,
                                    command=lambda: controller.show_frame("Students"))
        teachers_button = tk.Button(parents_teachers_districts_frame, text="Teachers", font=controller.big_button_font,
                                    command=lambda: controller.show_frame("Teachers"))
        parents_button = tk.Button(parents_teachers_districts_frame, text="Parents", font=controller.big_button_font,
                                   command=lambda: controller.show_frame("Parents"))
        districts_button = tk.Button(parents_teachers_districts_frame, text="Districts", font=controller.big_button_font,
                                     command=lambda: controller.show_frame("Districts"))
        students_button.pack(padx=20, pady=20)
        teachers_button.pack(side="left", padx=20)
        parents_button.pack(side="left", padx=20)
        districts_button.pack(side="left", padx=20)
        parents_teachers_districts_frame.pack(pady=20)

class Students(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        c = tk.Canvas(self, bg="blue", height=250, width=300)
        filename = ImageTk.PhotoImage(Image.open("circle_images/WaterImages/WaterPrimaryImages/lake01.jpg"))
        background_label = tk.Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        c.image=filename
        label = tk.Label(self, text="Welcome Students", font=controller.title_font)
        label.pack(side="top", pady=10)
        top_frame = tk.Frame(self, bg='black')
        middle_frame = tk.Frame(self, bg='black')
        bottom_frame = tk.Frame(self, bg='black')
        water_button = tk.Button(top_frame, text="Water", font=controller.big_button_font,
                           command=lambda: controller.show_frame("WaterStudents"))
        body_button = tk.Button(top_frame, text="Body", font=controller.big_button_font,
                           command=lambda: controller.show_frame("BodyStudents"))
        color_button = tk.Button(top_frame, text="Color", font=controller.big_button_font,
                           command=lambda: controller.show_frame("ColorStudents"))
        fall_button = tk.Button(top_frame, text="Fall", font=controller.big_button_font,
                           command=lambda: controller.show_frame("FallStudents"))
        geography_button = tk.Button(middle_frame, text="Geography", font=controller.big_button_font,
                           command=lambda: controller.show_frame("GeographyStudents"))
        house_button = tk.Button(middle_frame, text="House", font=controller.big_button_font,
                           command=lambda: controller.show_frame("HouseStudents"))
        plants_button = tk.Button(middle_frame, text="Plants", font=controller.big_button_font,
                           command=lambda: controller.show_frame("PlantsStudents"))
        space_button = tk.Button(bottom_frame, text="Space", font=controller.big_button_font,
                           command=lambda: controller.show_frame("SpaceStudents"))
        transportation_button = tk.Button(bottom_frame, text="Transportation", font=controller.big_button_font,
                           command=lambda: controller.show_frame("TransportationStudents"))
        world_culture_button = tk.Button(bottom_frame, text="World Culture", font=controller.big_button_font,
                           command=lambda: controller.show_frame("WorldCultureStudents"))

        return_to_main_page_button = tk.Button(self, text="Main Menu", command=lambda: controller.show_frame("StartPage"), font=controller.big_button_font)

        water_button.pack(side='left', padx=20, pady=20)
        body_button.pack(side='left', padx=20, pady=20)
        color_button.pack(side='left', padx=20, pady=20)
        fall_button.pack(side='left', padx=20, pady=20)
        geography_button.pack(side='left', padx=20, pady=20)
        house_button.pack(side='left', padx=20, pady=20)
        plants_button.pack(side='left', padx=20, pady=20)
        space_button.pack(side='left', padx=20, pady=20)
        transportation_button.pack(side='left', padx=20, pady=20)
        world_culture_button.pack(side='left', padx=20, pady=20)
        top_frame.pack(padx=20, pady=20)
        middle_frame.pack(padx=20, pady=20)
        bottom_frame.pack(padx=20, pady=20)
        return_to_main_page_button.pack(side='bottom')

class Teachers(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is teachers", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the main page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class Parents(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is parents", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the main page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class Districts(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is district", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the main page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class WaterStudents(otc.WaterStudents):
    pass

class BodyStudents(otc.BodyStudents):
    pass

class ColorStudents(otc.ColorStudents):
    pass

class FallStudents(otc.FallStudents):
    pass

class GeographyStudents(otc.GeographyStudents):
    pass

class HouseStudents(otc.HouseStudents):
    pass

class PlantsStudents(otc.PlantsStudents):
    pass

class SpaceStudents(otc.SpaceStudents):
    pass

class TransportationStudents(otc.TransportationStudents):
    pass

class WorldCultureStudents(otc.WorldCultureStudents):
    pass

if __name__ == "__main__":
    app = MainMenuGui()
    app.mainloop()