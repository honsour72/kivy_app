"""
Name: Assanali Amangeldiyev
Date: 18.01.2022
Brief Project Description: Create Movie list with interactive UI
GitHub URL:
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button

from movie import Movie

KEYS = {"Watched": "is_watched", "Genre": "genre", "Title": "title", "Year": "year"}


class MoviesToWatchApp(App):
    """..."""
    current_key = StringProperty()
    keys = ListProperty()
    movies = []
    count_w = 0
    count_u = 0

    def build(self):
        """Build the GUI using Kivy"""
        self.title = "Kivy Application"
        self.root = Builder.load_file("app.kv")
        self.keys = KEYS
        self.current_key = self.keys[0]
        self.create_widgets()
        self.count_movies()
        return self.root

    def change_key(self, key):
        print("Changed to", key)
        self.root.ids.entries_box.clear_widgets()
        if self.movies:
            if key == 'Genre':
                new_order = sorted(self.movies, key=lambda x: x.category)
            if key == 'Watched':
                new_order = [ww for ww in self.movies if ww.is_watched == "True"] + [uu for uu in self.movies if uu.is_watched != "True"]
            if key == 'Title':
                new_order = sorted(self.movies, key=lambda x: x.title)
            if key == 'Year':
                new_order = sorted(self.movies, key=lambda x: x.year)

            for movie in new_order:
                if movie.is_watched == 'True':
                    temp_button = Button(text = "{} ({} from {})".format(movie.title, movie.category, movie.year),
                                         on_press=self.callback,
                                         background_color = (0.86, 0.86, 0, 1),
                                         )
                else:
                    temp_button = Button(text = "{} ({} from {})".format(movie.title, movie.category, movie.year),
                                         background_color = (0, 0.75, 0.85, 1),
                                         on_press=self.callback)
                self.root.ids.entries_box.add_widget(temp_button)

        # self.count_movies()

    def handle_clear(self):
        """Handle clear button to remove all characters from input fields"""
        self.root.ids.title.text = ""
        self.root.ids.year.text = ""
        self.root.ids.category.text = ""

    def create_widgets(self):
        """Run through csv file and create widgets accordingly"""
        out_file = open("movies.csv", "r")
        for line in out_file:
            line = line.strip()
            line = line.split(",")
            new_movie = Movie(line[0], line[1], line[2], line[3])
            self.movies.append(new_movie)
            # Set background color only for unwatched movies
            # If watched
            if line[3] == "True":
                temp_button = Button(text = "{} ({} from {})".format(line[0], line[2], line[1]),
                                     on_press=self.callback,
                                     background_color = (0.86, 0.86, 0, 1),
                                     )
                self.count_w += 1
            else:
                temp_button = Button(text = "{} ({} from {})".format(line[0], line[2], line[1]),
                                     background_color = (0, 0.75, 0.85, 1),
                                     on_press=self.callback)
                self.count_u += 1

            self.root.ids.entries_box.add_widget(temp_button)
        out_file.close()

    def add_movie(self):
        """Add widget of a movie using inputs from the user and set background color"""
        if self.root.ids.title.text == "" or self.root.ids.category.text == "" or self.root.ids.year.text == "":
            self.root.ids.status_text.text = "All fields must be completed"
        elif int(self.root.ids.year.text) <= 0:
            self.root.ids.status_text.text = "Year must be > 0"
        else:
            self.movies.append(Movie(self.root.ids.title.text,
                                     self.root.ids.category.text,
                                     self.root.ids.year.text,
                                     False))
            # Add widget of a new movie
            temp_button = Button(text = "{} ({} from {})".format(self.root.ids.title.text,
                                                                 self.root.ids.category.text,
                                                                 self.root.ids.year.text),
                                 on_press=self.callback,
                                 background_color = (0, 0.75, 0.85, 1))
            self.root.ids.entries_box.add_widget(temp_button)
            # Update status text
            self.root.ids.status_text.text = "{} ({} from {}) added".format(self.root.ids.title.text,
                                                                            self.root.ids.category.text,
                                                                            self.root.ids.year.text)
            self.count_u += 1
            self.handle_clear()
            self.count_movies()
            self.save_movies("movies.csv")

    def count_movies(self):
        """Count the number of unwatched movies"""
        self.root.ids.movies.text = f"To watch: {self.count_u}. Watched: {self.count_w}"

    def save_movies(self, file_name):
        """Save movies back to csv file"""
        out_file = open(file_name, "w")
        for movie in self.movies:
            movie = str(movie)
            if movie or not movie:
                movie += "\n"
            out_file.write(movie)
        out_file.close()

    def callback(self, instance_toggle_button):
        # If watched
        if instance_toggle_button.background_color == [0.86, 0.86, 0, 1]:
            # Change button backgroun color
            instance_toggle_button.background_color = (0, 0.75, 0.85, 1)
            # Change movie watch-parameter
            self.set_movie_watched(instance_toggle_button.text)
            # Change counters
            self.count_u += 1
            self.count_w -= 1
            # Change status_text text
            self.root.ids.status_text.text = "You need to watch {}".format(instance_toggle_button.text)
        else:
            # Change button backgroun color
            instance_toggle_button.background_color = (0.86, 0.86, 0, 1)
            self.set_movie_watched(instance_toggle_button.text)
            # Change counters
            self.count_u -= 1
            self.count_w += 1
            # Change status_text text
            self.root.ids.status_text.text = "You have watched {}".format(instance_toggle_button.text)
        self.count_movies()

    def set_movie_watched(self, _movie: str) -> None:
        # get current movie from the list
        movie_name = _movie.split(" (")[0]
        m = [x for x in self.movies if x.title == movie_name][0]
        # update movies list without current movie
        self.movies = [y for y in self.movies if y.title != movie_name]
        # set the watch-parameter
        if m.is_watched == 'False':
            m.is_watched = 'True'
        else:
            m.is_watched = 'False'
        # update current movie and append it to the list
        self.movies.append(m)


if __name__ == '__main__':
    MoviesToWatchApp().run()
