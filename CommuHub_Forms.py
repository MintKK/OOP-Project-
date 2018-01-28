from wtforms import Form, StringField, PasswordField, RadioField, SelectField, ValidationError, FileField, SubmitField, TextAreaField, DateField, validators

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
    title = StringField('Title', [validators.Length(min=1, max=150), validators.DataRequired()])
    items = RadioField('Type Of Publication', choices=[('sbook', 'Book'), ('smag', 'Magazine')], default='sbook')
    category = SelectField('Caterory', [validators.DataRequired()],
                           choices=[('', 'Select'), ('FANTASY', 'Fantasy'), ('FASHION', 'Fashion'),
                                    ('THRILLER', 'Thriller'), ('CRIME', 'Crime'), ('BUSINESS', 'Business')],
                           default='')
    publisher = StringField('Publisher', [validators.Length(min=1, max=100), validators.DataRequired()])
    status = SelectField('status', [validators.DataRequired()], choices=[('', 'Select'), ('P', 'Pending'), ('A', 'Available For Borrowing'), ('R', 'Only For Reference')], default='')
    isbn = StringField('ISBN No', [
        validators.Length(min=1, max=100),
        RequiredIf(pubtype='sbook')])
    author = StringField('Author', [
        validators.Length(min=1, max=100),
        RequiredIf(pubtype='sbook')])
    synopsis = TextAreaField('Synopsis', [
        RequiredIf(pubtype='sbook')])
    frequency = RadioField('Frequency', [RequiredIf(pubtype='smag')],
                           choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')])



