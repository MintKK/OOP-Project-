import datetime

class DProject:

    def __init__(self, title, creator, itemCategories, description, items, start_date, end_date, duration=None, status=None):
        # Maybe set default value for end date, default duration of project
        self.__p_id = ''  # May use to link for user designed HTML template
        self.__title = title
        self.__creator = creator
        self.__categories = itemCategories
        self.__description = description
        self.__items = items
        self.__start_date = str(start_date) # Convert just in case
        # self.__start_date = str(datetime.datetime.now().day) + "/" + str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)  # DD-MM-YYYY format
        self.__end_date = str(end_date)  # Convert just in case
        if duration != None:
            pass
            # Enter code to calculate end date with duration
        self.__status = status


    def get_p_id(self):
        return self.__p_id

    def get_title(self):
        return self.__title

    def get_creator(self):
        return self.__creator

    def get_categories(self):
        return self.__categories

    def get_description(self):
        return self.__description

    def get_items(self):
        return self.__items

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date

    def get_duration(self):
        return self.__duration

    def get_status(self):
        return self.__status

    # Testing
    def print_date(self):
        print(datetime.datetime.now())

    def set_p_id(self, p_id):
        self.__p_id = p_id

    def set_title(self, title):
        self.__title = title

    def set_creator(self, creator):
        self.__creator = creator

    def set_categories(self, itemCategories):
        self.__categories = itemCategories

    def set_description(self, description):
        self.__description = description

    def set_items(self, items):
        self.__items = items

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def set_duration(self, duration):
        self.__duration = duration

    def set_status(self, status):
        self.__status = status

# test = DProject("1","2","3","4","5","6","7","8")
# test.print_date()
