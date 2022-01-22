
class Movie:
    """Movie class"""
    def __init__(self, title="", year=0, category="", is_watched=False):
        self.title = title
        self.year = year
        self.category = category
        self.is_watched = is_watched

    def __str__(self):
        return "{},{},{},{}".format(self.title, self.year, self.category, self.is_watched)

    def watch(self):
        if not self.is_watched:
            self.is_watched = True