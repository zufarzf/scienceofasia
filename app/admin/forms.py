from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, FileField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_ckeditor import CKEditorField

default_message='Нельзя пропускать это поле'

class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired(message=default_message)])
    psw = PasswordField(validators=[DataRequired(message=default_message)])
    submit = SubmitField('Enter')


class AddAdminForm(FlaskForm):
    login = StringField(validators=[
        DataRequired(message=default_message),
        Length(min=4, message='Login должен быть не меньше 4 символов!')
        ])
    psw = PasswordField(validators=[
        DataRequired(message=default_message),
        Length(min=8, message='Пароль должен быть не меньше 8 символов!')
        ])
    repeat_psw = PasswordField(
        validators=[
            DataRequired(message=default_message),
            EqualTo('psw', message='Пароли не совпадают!')
            ])
    submit = SubmitField('Add')



class EditAdminForm(FlaskForm):
    login = StringField(validators=[])
    psw = PasswordField(validators=[])
    repeat_psw = PasswordField(validators=[EqualTo('psw', message='Пароли не совпадают!')])
    submit = SubmitField('Add')




class LeftMenuForm(FlaskForm):
    name = StringField(validators=[DataRequired(message=default_message)])
    date = StringField(validators=[DataRequired(message=default_message)])
    cover_image = TextAreaField()
    photographed = StringField()
    submit = SubmitField('Save')



class CategoryForm(FlaskForm):
    name = StringField(validators=[DataRequired(message=default_message)])
    submit = SubmitField('Save')





class ArticlesForm(FlaskForm):
    name = CKEditorField('name')  #ckeditor
    
    authors = StringField()
    authors_p = CKEditorField('authors_p') #ckeditor

    abstract = TextAreaField()
    pdf_file = FileField()

    doi_text = CKEditorField('doi_text') #ckeditor
    downloads = StringField()
    views = StringField()

    sub_text = CKEditorField('sub_list') #ckeditor
    author_email = StringField()

    received_date = StringField()
    accepted_date = StringField()

    valid_articles = BooleanField()
    
    enter = SubmitField('Save')


class LeftBarForm(FlaskForm):
    image = FileField()
    enter = SubmitField('Save')



class RightBarForm(FlaskForm):
    image_1 = FileField()
    image_2 = FileField()
    text_1 = StringField()
    text_2 = StringField()
    text_3 = StringField()
    text_4 = StringField()
    text_5 = TextAreaField()
    enter = SubmitField('Save')



class MainDataForm(FlaskForm):
    line_text_first = TextAreaField()
    line_text_last = TextAreaField()
    volume_image = FileField()
    volume_name = StringField()
    issues_in_prog = TextAreaField()
    enter = SubmitField('Save')



class MainCatalogsForm(FlaskForm):
    name = StringField()
    enter = SubmitField('Save')




class RecentSupplementForm(FlaskForm):
    image = FileField()
    text = StringField()
    link = StringField()
    enter = SubmitField('Save')


class IssuesProgressForm(FlaskForm):
    text = StringField()
    link = StringField()
    enter = SubmitField('Save')




class EditorialBoardTitleForm(FlaskForm):
    title_name = StringField(validators=[DataRequired(message=default_message)])

class EditorialBoardItemsForm(FlaskForm):
    title = SelectField('Title')
    text = CKEditorField('editorial_item') #ckeditor