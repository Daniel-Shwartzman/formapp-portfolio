from wtforms import ValidationError

class Unique:

    def __init__(self, instance=None, field=None, message=None):
        self.instance = instance
        self.field = field
        self.message = message

    def __call__(self, form, field):
        if self.instance.query.filter(self.field == field.data).first():
            if not self.message:
                self.message = f'{field.name} already exists.'
            raise ValidationError(self.message)
