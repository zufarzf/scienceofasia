from flask import render_template, url_for, redirect, flash, session, request
from werkzeug.security import generate_password_hash as g_psw_hash, check_password_hash as c_psw_hash
from . import admin
from app import db
from ..dbModels import Admins, LeftMenu, Categories, Jurnals
from .forms import LoginForm, AddAdminForm, LeftMenuForm, CategoryForm, ArticlesForm, EditAdminForm


@admin.route("/", methods=['GET', 'POST'])
def admin_login():
    categories_chek = Categories.query

    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    if 'login' in session:
        return redirect(url_for('main.home'))
    else:
        form = LoginForm()
        
        if form.validate_on_submit():
            admin = Admins.query.filter_by(name=form.login.data).first()
            if admin is None:
                flash('Не правильный login!')
                return redirect(url_for('admin.admin_login'))
            
            if c_psw_hash(admin.psw, form.psw.data):
                session['login'] = admin.id
                return redirect(url_for('main.home'))
            else:
                flash('Не правильный пароль!')
                return redirect(url_for('admin.admin_login'))
            

        return render_template(
            'admin-login.html',
            page_title = 'Login',
            form=form, volumes=volumes, categories_chek=categories_chek
            )


@admin.route("/Exit", methods=['GET', 'POST'])
def exit():
    del session['login']
    return redirect(url_for('main.home'))





@admin.route("/Add-Admin", methods=['GET', 'POST'])
def admin_add():
    if 'login' in session:
        categories_chek = Categories.query

        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()

        form = AddAdminForm()
        if form.validate_on_submit():
            admin = Admins.query.filter_by(name=form.login.data).first()
            if admin is None:
                hash_psw = g_psw_hash(form.psw.data)
                admin = Admins(name=form.login.data, psw=hash_psw)
                try:
                    db.session.add(admin)
                    db.session.commit()
                    flash('Admin успешно добавлен!')
                    return redirect(url_for('admin.admin_add'))
                except:
                    flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                    return redirect(url_for('admin.admin_add'))
            elif admin is not None:
                flash('Такой администратор уже существует!')
                return redirect(url_for('admin.admin_add'))


        return render_template(
            'add-admin.html',
            page_title = 'Add Admin',
            form=form, volumes=volumes,
            categories_chek=categories_chek,
            form_name = 'Add Admin',
            func = 'admin.admin_add'
            )
    else: return redirect(url_for('main.home'))



@admin.route("/Admin-panel", methods=['GET', 'POST'])
def admin_panel():
    if 'login' in session:
        admins = Admins.query.all()
        admins_li = []
        for i in admins:
            admins_li.append(i.id)
        if len(admins_li) == 1: delete = False
        else: delete = True
        categories_chek = Categories.query
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        admin = Admins.query.filter_by(id=session['login']).first()
        return render_template(
            'admin-panel.html',
            page_title = 'Add Admin',
            volumes=volumes,
            categories_chek=categories_chek,
            admin=admin, delete=delete, admins_li=len(admins_li)
            )
    else: return redirect(url_for('main.home'))



@admin.route("/Admin-edit", methods=['GET', 'POST'])
def admin_edit():
    if 'login' in session:
        categories_chek = Categories.query
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()

        form = EditAdminForm()
        admin = Admins.query.filter_by(id=session['login']).first()

        if form.validate_on_submit():
            if admin is not None:
                hash_psw = g_psw_hash(form.psw.data)
                if form.login.data != '': admin.name = form.login.data
                if form.psw.data != '': admin.psw=hash_psw

                try:
                    db.session.add(admin)
                    db.session.commit()
                    flash('Данные успешно изменены!')
                    return redirect(url_for('admin.admin_panel'))
                except:
                    flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                    return redirect(url_for('admin.admin_edit'))

        form.login.data = admin.name
        form.psw.data = admin.psw
        form.repeat_psw.data = admin.psw

        return render_template(
            'add-admin.html',
            page_title = 'Admin Edit',
            form=form, volumes=volumes,
            categories_chek=categories_chek,
            form_name = 'Admin Edit',
            func = 'admin.admin_edit'
            )
    else: return redirect(url_for('main.home'))



@admin.route("/Admin-delete", methods=['GET', 'POST'])
def admin_delete():
    if 'login' in session:
        categories_chek = Categories.query
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()

        return render_template(
            'admin-delete.html',
            page_title = 'Add Admin',
            volumes=volumes,
            categories_chek=categories_chek
            )
    else: return redirect(url_for('main.home'))


@admin.route("/delete_profile")
def delete_profile():
    if 'login' in session:
        admins = Admins.query.all()
        admins_li = []
        for i in admins:
            admins_li.append(i.id)
        if len(admins_li) == 0:
            flash('Нельзя удалять единственный профиль админа!')
            return redirect(url_for('admin.admin_panel'))
        else:
            categories_chek = Categories.query
            volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
            admin = Admins.query.filter_by(id=session['login']).first()
            if admin is not None:
                try:
                    db.session.delete(admin)
                    db.session.commit()
                    del session['login']
                    flash('admin успешно удалён!')
                    return redirect(url_for('main.home'))
                except:
                    flash('Ошибка при удалении! Пожалуйста, повторите попытку.')
                    return redirect(url_for('admin.delete_profile'))
            elif admin is None:
                flash('Такой volume не существует!')
                return redirect(url_for('admin.admin_panel'))

    else: return redirect(url_for('main.home'))



# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


@admin.route("/Add-Volume", methods=['GET', 'POST'])
def add_volume():
    if 'login' in session:

        categories_chek = Categories.query

        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()

        form = LeftMenuForm()
        if form.validate_on_submit():
            volume = LeftMenu.query.filter_by(name=form.name.data).first()
            if volume is None:
                volume = LeftMenu(
                    name=form.name.data,
                    date=form.date.data,
                    cover_image=form.cover_image.data,
                    photographed=form.photographed.data
                    )
                try:
                    db.session.add(volume)
                    db.session.commit()
                    flash('Volume сохранён')
                    return redirect(url_for('admin.add_volume'))
                except:
                    flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                    return redirect(url_for('admin.add_volume'))
            elif volume is not None:
                flash('Такой volume уже существует!')
                return redirect(url_for('admin.add_volume'))


        return render_template(
            'add-volume.html',
            page_title = 'Add volume',
            form=form, volumes=volumes, categories_chek=categories_chek
            )
    else: return redirect(url_for('main.home'))


@admin.route("/Edit-Volume/<int:id>", methods=['GET', 'POST'])
def edit_volume(id):
    if 'login' in session:

        categories_chek = Categories.query

        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()

        form = LeftMenuForm()
        volume = LeftMenu.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if volume is not None:
                volume.name=form.name.data
                volume.date=form.date.data
                volume.cover_image=form.cover_image.data,
                volume.photographed=form.photographed.data
                try:
                    db.session.add(volume)
                    db.session.commit()
                    flash('Volume изменён')
                    return redirect(url_for('main.volume_1', id=id))
                except:
                    flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                    return redirect(url_for('admin.edit_volume', id=id))
            elif volume is None:
                flash('Такой volume не существует!')
                return redirect(url_for('admin.edit_volume', id=id))


        return render_template(
            'edit-volume.html',
            page_title = 'Edit volume',
            volume=volume,
            form=form, volumes=volumes, categories_chek=categories_chek,
            cover_image = volume.cover_image
            )
    else: return redirect(url_for('main.home'))


@admin.route("/Delete-Volume/<int:id>")
def delete_volume(id):
    if 'login' in session:

        volume = LeftMenu.query.filter_by(id=id).first()

        if volume is not None:
            try:
                db.session.delete(volume)
                db.session.commit()
                flash('Volume успешно удалён!')
                return redirect(url_for('admin.add_volume'))
            except:
                flash('Ошибка при удалении! Пожалуйста, повторите попытку.')
                return redirect(url_for('main.home'))
        elif volume is None:
            flash('Такой volume не существует!')
            return redirect(url_for('main.home'))

    else: return redirect(url_for('main.home'))



# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


@admin.route("/Add-category/<int:id>", methods=['GET', 'POST'])
def add_category(id):
    if 'login' in session:

        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query


        form = CategoryForm()
        if form.validate_on_submit():
            category = Categories.query.filter_by(name=form.name.data).first()
            category = Categories(name=form.name.data, left_menu=id)
            try:
                db.session.add(category)
                db.session.commit()
                flash('Volume сохранён')
                return redirect(url_for('main.volume_1', id=id))
            except:
                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                return redirect(url_for('admin.add_category'))

        return render_template(
            'add-category.html',
            page_title = 'Add category',
            form=form, volumes=volumes, categories_chek=categories_chek, id=id
            )

    else: return redirect(url_for('main.home'))



@admin.route("/Edit-category/<int:id>", methods=['GET', 'POST'])
def edit_category(id):
    if 'login' in session:

        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query


        form = CategoryForm()
        category = Categories.query.filter_by(id=id).first()
        if form.validate_on_submit():
            if category is not None:
                category.name=form.name.data
                try:
                    db.session.add(category)
                    db.session.commit()
                    flash('Category изменён')
                    return redirect(url_for('main.volume_1', id=category.left_menu))
                except:
                    flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                    return redirect(url_for('admin.edit_category', id=id))
            elif category is None:
                flash('Такой category не существует!')
                return redirect(url_for('admin.edit_category', id=id))


        return render_template(
            'edit-category.html',
            page_title = 'Edit volume',
            category=category,
            form=form, volumes=volumes, categories_chek=categories_chek,
            id=id
            )

    else: return redirect(url_for('main.home'))


@admin.route("/Delete-category/<int:id>")
def delete_category(id):
    if 'login' in session:

        category = Categories.query.filter_by(id=id).first()
        volume_id = category.left_menu
        if category is not None:
            try:
                db.session.delete(category)
                db.session.commit()
                flash('Category успешно удалён!')
                return redirect(url_for('main.volume_1', id=volume_id))
            except:
                flash('Ошибка при удалении! Пожалуйста, повторите попытку.')
                return redirect(url_for('main.volume_1', id=volume_id))
        elif category is None:
            flash('Такой volume не существует!')
            return redirect(url_for('main.volume_1', id=volume_id))
    
    else: return redirect(url_for('main.home'))










# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

def allowed(ext: str):
    li = ['pdf', 'PDF']
    if ext in li: return True
    else: return False

import os

@admin.route("/Add-article/<int:id>", methods=['GET', 'POST'])
def add_article(id):
    if 'login' in session:

        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query

        category = Categories.query.filter_by(id=id).first()
        volume_id = category.left_menu

        form = ArticlesForm()
        if form.validate_on_submit():
            pdf_file = request.files.get('pdf_file', None)
            if pdf_file.filename != '':
                ext = pdf_file.filename.split('.')[-1]
                # -----------------------
                if allowed(ext):
                    folder_path = os.path.join('app', 'main', 'main-static', 'upload_files')
                    # -----------------------
                    pdf_file.save(os.path.join(folder_path, pdf_file.filename))
                    pdf_name = pdf_file.filename
                    pdf_true = Jurnals.query.filter_by(pdf_url=pdf_name).first()
                else:
                    flash('Можно отправлять только в PDF фомате!')
                    return redirect(url_for('admin.add_article', id=id))
            else:
                pdf_true = None
                pdf_name = 'FalseNone'


            article = Jurnals.query.filter_by(title=form.name.data).first()
            if article is None and pdf_true is None:
                article = Jurnals(
                    title = form.name.data,
                    authors = form.authors.data,
                    authors_sup = form.authors_p.data,
                    abstract = form.abstract.data,
                    pdf_url = pdf_name,
                    # ----------------------------
                    doi_text = form.doi_text.data,
                    downloads = form.downloads.data,
                    Views = form.views.data,
                    # ----------------------------
                    sub_text = form.sub_text.data,
                    author_email = form.author_email.data,
                    # ----------------------------
                    received_date = form.received_date.data,
                    accepted_date = form.accepted_date.data,
                    # ----------------------------
                    valid_articles = form.valid_articles.data,
                    menu_id=id
                    )
                try:
                    db.session.add(article)
                    db.session.commit()
                    flash('Article сохранён')
                    return redirect(url_for('main.volume_1', id=volume_id))
                except:
                    flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                    return redirect(url_for('admin.add_article', id=id))
            elif article is not None:
                flash('Такой article уже существует!')
                return redirect(url_for('admin.add_article', id=id))


        return render_template(
            'add-article.html',
            page_title = 'Add Article',
            form=form, volumes=volumes, categories_chek=categories_chek, id=id
            )
    else: return redirect(url_for('main.home'))


@admin.route("/Edit-article/<int:id>", methods=['GET', 'POST'])
def edit_article(id):
    if 'login' in session:

        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query

        article = Jurnals.query.filter_by(id=id).first()
        
        categories = Categories.query.filter_by(id=article.menu_id).first()
        volume_id = categories.left_menu

        form = ArticlesForm()
        

        if form.validate_on_submit():
            pdf_file = request.files.get('pdf_file', None)
            
            # -----------------------
            if pdf_file.filename != '':
                ext = pdf_file.filename.split('.')[-1]
                # -----------------------
                folder_path = os.path.join('app', 'main', 'main-static', 'upload_files')
                if allowed(ext):
                    if os.path.exists(os.path.join(folder_path, article.pdf_url)):
                        if os.path.isfile(os.path.join(folder_path, article.pdf_url)):
                            os.remove(os.path.join(folder_path, article.pdf_url))
                    # -----------------------
                    pdf_file.save(os.path.join(folder_path, pdf_file.filename))
                    pdf_name = pdf_file.filename
                else:
                    flash('Можно отправлять только в PDF фомате!')
                    return redirect(url_for('admin.add_article', id=id))
            else:pdf_name = article.pdf_url

            article.valid_articles = form.valid_articles.data
            article.title = form.name.data
            article.authors = form.authors.data
            article.authors_sup = form.authors_p.data
            article.abstract = form.abstract.data
            article.pdf_url = pdf_name
            article.doi_text = form.doi_text.data
            article.downloads = form.downloads.data
            article.Views = form.views.data
            article.sub_text = form.sub_text.data
            article.author_email = form.author_email.data
            article.received_date = form.received_date.data
            article.accepted_date = form.accepted_date.data

            try:
                db.session.add(article)
                db.session.commit()
                flash('Article сохранён')
                return redirect(url_for('main.volume_1', id=volume_id))
            except:
                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                return redirect(url_for('admin.add_article', id=id))

        form.valid_articles.data = article.valid_articles
        form.name.data = article.title
        form.authors.data = article.authors
        form.authors_p.data = article.authors_sup
        form.abstract.data = article.abstract
        form.doi_text.data = article.doi_text
        form.downloads.data = article.downloads
        form.views.data = article.Views
        form.sub_text.data = article.sub_text
        form.author_email.data = article.author_email
        form.received_date.data = article.received_date
        form.accepted_date.data = article.accepted_date

        return render_template(
            'edit-article.html',
            page_title = 'Edit Article',
            form=form, volumes=volumes, categories_chek=categories_chek, id=id
            )
    else: return redirect(url_for('main.home'))



@admin.route("/Delete-article/<int:id>")
def delete_article(id):
    if 'login' in session:

        article = Jurnals.query.filter_by(id=id).first()
        category = Categories.query.filter_by(id=article.menu_id).first()
        volume_id = category.left_menu
        if article is not None:
            # -----------------------
            folder_path = os.path.join('app', 'main', 'main-static', 'upload_files')
            if os.path.exists(os.path.join(folder_path, article.pdf_url)):
                        if os.path.isfile(os.path.join(folder_path, article.pdf_url)):
                            os.remove(os.path.join(folder_path, article.pdf_url))
            
            try:
                db.session.delete(article)
                db.session.commit()
                flash('Article успешно удалён!')
                return redirect(url_for('main.volume_1', id=volume_id))
            except:
                flash('Ошибка при удалении! Пожалуйста, повторите попытку.')
                return redirect(url_for('main.volume_1', id=volume_id))
        elif article is None:
            flash('Такой volume не существует!')
            return redirect(url_for('main.volume_1', id=volume_id))
    else: return redirect(url_for('main.home'))
