import datetime

class DProject:

    def __init__(self, title, creator, items, status, category, end_date):
        # Maybe set default value for end date, default duration of project
        self.__p_id = ''  # May use to link for user designed HTML template
        self.__title = title
        self.__creator = creator
        self.__items = items
        self.__status = status
        self.__start_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)  # DD-MM-YYYY format
        self.__category = category
        self.__end_date = str(end_date)  # Convert in case

    def get_p_id(self):
        return self.__p_id

    def get_title(self):
        return self.__title

    def get_creator(self):
        return self.__creator

    def get_items(self):
        return self.__items

    def get_status(self):
        return self.__status

    def get_category(self):
        return self.__category

    def get_end_date(self):
        return self.__end_date

    # Testing
    def print_date(self):
        print(datetime.datetime.now())

    def set_title(self, title):
        self.__title = title

    def set_creator(self, creator):
        self.__creator = creator

    def set_status(self, status):
        self.__status = status

    def set_category(self, category):
        self.__category = category

    def set_end_date(self, end_date):
        self.__end_date = end_date
