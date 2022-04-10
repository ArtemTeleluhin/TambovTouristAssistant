class ArticlesQueue:
    def __init__(self, data, user_latitude, user_longitude):
        self.data = data
        self.current_position = 0
        self.user_latitude = user_latitude
        self.user_longitude = user_longitude
        self.flag_is_top_selected = False

    def get_current_element(self):
        return self.data[self.current_position]

    def next_element(self):
        if self.is_last():
            return None
        self.flag_is_top_selected = False
        self.current_position += 1
        return self.data[self.current_position]

    def prev_element(self):
        if self.is_first():
            return None
        self.flag_is_top_selected = False
        self.current_position -= 1
        return self.data[self.current_position]

    def is_last(self):
        if self.current_position == len(self.data) - 1:
            return True
        return False

    def is_first(self):
        if self.current_position == 0:
            return True
        return False

    def get_user_cords(self):
        return self.user_latitude, self.user_longitude

    def get_top_articles(self, count):
        self.flag_is_top_selected = True
        return self.data[:min(count, len(self.data))]

    def is_top_last(self):
        return self.flag_is_top_selected
