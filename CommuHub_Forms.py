from wtforms import *
class RequiredIf(object):
    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)

class NewProjectForm(Form):
    # Part 1
    title = StringField('Title', [validators.Length(min=10, max=175), validators.DataRequired("Please enter a title")])
    creator = StringField('Creator name', [validators.Length(min=1, max=100), validators.DataRequired("...")])
    categories = [('CMoney', 'Money'), ('CBooks', 'Books'), ('CClothes', 'Clothes'), ('CFood', 'Food'), ('CAmenities', 'Household amenities'), ('COthers', 'Others')]
    itemCategories = SelectMultipleField('Categories of items to be collected', [validators.DataRequired("Select at least one category")], choices=categories, default="")

    # Part 2
    description = TextAreaField("Project description", [validators.DataRequired("...")])
    items = StringField('Items') #Hmmmm

    # Part 3
    #status = StringField('Status') #Should not be user input
    start_date = StringField('Start date')
    end_date = StringField('End date')



