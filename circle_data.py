import sqlite3
from sqlite3 import Error

from PIL import Image

class PerImage:
    def __repr__(self):
        return f"{self.image_name}"

    def __str__(self):
        return f"{self.image_name}"

    def __init__(self, prog_name, theme, image_name, unit, vocabulary, num_syll, syll_structure, ab_sent, bc_sent,
                 ab_question, ab_question_domain, bc_question, bc_question_domain, alliteration, rhyme):

        self.prog_name = prog_name
        self.theme = theme
        self.image_name = image_name
        self.unit = unit
        self.vocabulary = vocabulary
        self.num_syll = num_syll
        self.syll_structure = syll_structure
        self.ab_sent = ab_sent
        self.bc_sent = bc_sent
        self.ab_question = ab_question
        self.ab_question_domain = ab_question_domain
        self.bc_question = bc_question
        self.bc_question_domain = bc_question_domain
        self.alliteration = alliteration
        self.rhyme = rhyme

    def get_program_name(self):
        return self.prog_name

    def get_theme(self):
        return self.theme

    def get_image_name(self):
        return self.image_name

    def get_unit(self):
        return self.unit

    def get_num_syll(self):
        return self.num_syll

    def get_syll_structure(self):
        return self.syll_structure

    def get_ab_sent(self):
        return self.ab_sent

    def get_bc_sent(self):
        return self.bc_sent

    def get_ab_question(self):
        return self.ab_question

    def get_ab_question_domain(self):
        return self.ab_question_domain

    def get_bc_question(self):
        return self.bc_question

    def get_bc_question_domain(self):
        return self.bc_question_domain

    def get_alliteration(self):
        return self.alliteration

    def get_rhyme(self):
        return self.rhyme


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_theme_infos(conn, th):
    theme = th
    cur = conn.cursor()
    cur.execute(rf"SELECT prog_name, theme, image_name, unit, vocabulary, num_syll, syll_structure, ab_sent, bc_sent, ab_question, ab_question_domain, bc_question, bc_question_domain, alliteration, rhyme FROM circle_db WHERE theme == '{theme}'")
    rows = cur.fetchall()
    images = []
    for row in rows:
        prog_name, theme, image_name, unit, vocabulary, num_syll, syll_structure, ab_sent, bc_sent, ab_question, ab_question_domain, bc_question, bc_question_domain, alliteration, rhyme = row
        image = PerImage(prog_name, theme, image_name, unit, vocabulary, num_syll, syll_structure, ab_sent, bc_sent, ab_question, ab_question_domain, bc_question, bc_question_domain, alliteration, rhyme)
        images.append(image)
    return images


def circle_app_main():
    database = r"circle_db.db"
    conn = create_connection(database)
    theme_names = ['body', 'color', 'house', 'plants', 'geography', 'space', 'fall', 'transportation', 'world culture', 'water']
    themes = []
    for th in theme_names:
        local_theme = []
        with conn:
            images = create_theme_infos(conn, th)
            local_theme.append(images)
        themes.append(local_theme)
    # img = Image.open(rf'circle_images/{vocab_choice}.jpg')
    # img.show()
    print("---Circle-ELD---")
    print("---------Images for Conversation---------")
    print()
    print(theme_names)

    choice = input("Enter a theme name from the list above: ")
    print("-----------------")
    both = list(zip(theme_names, themes))
    for theme_name, theme in both:
        if choice == theme_name:
            print(f"You have chosen to look at {choice} materials. Here is the vocabulary: \n")
            for image in theme:
                for part in image:
                    print(part.image_name, end=" * ")
            vocab_choice = input("\nYour image choice: ")
            print("-----------------")
            print("From the following list choose a type of data to look at:\nprog_name, theme, image_name, image, unit, vocabulary, num_syll, \nsyll_structure, ab_sent, bc_sent, ab_question, ab_question_domain, \nbc_question, bc_question_domain, alliteration, rhyme")
            data_type = input("Your type of data:")
            for image in theme:
                for part in image:
                    if vocab_choice == part.image_name:
                        if data_type == "prog_name":
                            print(f"{part.prog_name}")
                        elif data_type == "image":
                            directory = str(part.theme).capitalize()
                            img = Image.open(rf'circle_images/{directory}Images/{vocab_choice}.jpg')
                            img.show(title=f"{vocab_choice}")
                        elif data_type == "theme":
                            print(f"{part.theme}")
                        elif data_type == "image_name":
                            print(f"{part.image_name}")
                        elif data_type == "unit":
                            print(f"{part.unit}")
                        elif data_type == "vocabulary":
                            print(f"{part.vocabulary}")
                        elif data_type == "num_syll":
                            print(f"{part.num_syll}")
                        elif data_type == "syll_structure":
                            print(f"{part.syll_structure}")
                        elif data_type == "ab_sent":
                            print(f"{part.ab_sent}")
                        elif data_type == "bc_sent":
                            print(f"{part.bc_sent}")
                        elif data_type == "ab_question_domain":
                            print(f"{part.ab_question_domain}")
                        elif data_type == "ab_question":
                            print(f"{part.ab_question}")
                        elif data_type == "bc_question_domain":
                            print(f"{part.bc_question_domain}")
                        elif data_type == "bc_question":
                            print(f"{part.bc_question}")

if __name__ == '__main__':
    circle_app_main()
