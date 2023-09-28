from flask import render_template, url_for, redirect, flash, session, request
from werkzeug.security import generate_password_hash as g_psw_hash, check_password_hash as c_psw_hash
from . import admin
from app import db
from ..dbModels import (
    Admins, LeftMenu, Categories, Jurnals, LeftBar,
    RightBar, MainData, MainCatalogs, RecentSupplement, IssuesProgress,
    EditorialBoardTitles, EditorialBoardItems)
from .forms import (
    LoginForm, AddAdminForm, LeftMenuForm, CategoryForm, MainDataForm, RecentSupplementForm,
    ArticlesForm, EditAdminForm, LeftBarForm, RightBarForm, MainCatalogsForm, IssuesProgressForm,
    EditorialBoardTitleForm, EditorialBoardItemsForm)




@admin.route("/editorial_board_title/<int:col>/<int:handler_type>/<int:id>/<add_type>", methods=['GET', 'POST'])
def editorial_board_title(col, handler_type, id, add_type):
    # -----   -----   -----
    if col != 1 and col != 2: col = 1
    if col == 1: col_result = True
    if col == 2: col_result = False
    # -----   -----   -----   -----
    if handler_type != 1 and handler_type != 0:
        handler_type = 1
    # -----   -----   -----   -----
    form = EditorialBoardTitleForm()
    func = 'admin.editorial_board_title'
    # -----   -----   -----   -----

    if form.validate_on_submit():
        if handler_type:
            db.session.add(EditorialBoardTitles(
                column = col_result,
                name = form.title_name.data,
            ))
            db.session.commit()
        else:
            title = EditorialBoardTitles.query.filter_by(id=id).first()
            if title:
                title.name = form.title_name.data
                db.session.add(title)
                db.session.commit()

        if add_type == 'addMoreBtn':
            return redirect(url_for(
                func, col = col,
                handler_type = handler_type,
                id = id,
                add_type = 'None',
            ))
        elif add_type == 'addBtn':
            return redirect(url_for('main.edition'))
    # -----   -----   -----   -----
    if handler_type == 0:
        title = EditorialBoardTitles.query.filter_by(id=id).first()
        if title: form.title_name.data = title.name
    # -----   -----   -----   -----
    return render_template(
        'editorial_board_title.html',
        form = form,
        form_name = f'Add Title {col}',
        func = func,
        col = col,
        id = id,
        handler_type = handler_type,
    )


@admin.route("/editorial_board_title_delete/<int:id>", methods=['GET', 'POST'])
def editorial_board_title_delete(id):
    # -----   -----   -----   -----
    title = EditorialBoardTitles.query.filter_by(id=id).first()
    if title:
        db.session.delete(title)
        db.session.commit()

    return redirect(url_for('main.edition'))




@admin.route("/editorial_board_item/<int:title_id>/<int:handler_type>/<int:id>/<add_type>", methods=['GET', 'POST'])
def editorial_board_item(title_id, handler_type, id, add_type):
    title_query = EditorialBoardTitles.query.filter_by(id=title_id).first()
    
    if title_query:
        title_id = title_query.id

        # -----   -----   -----
        if handler_type != 1 and handler_type != 0:
            handler_type = 1
        # -----   -----   -----   -----
        form = EditorialBoardItemsForm()
        # Получите данные для choices из вашей модели или другого источника
        titles = EditorialBoardTitles.query.all()
        choices_data = []
        first_tuple = []

        for title in titles:
            my_tuple = (title.id, title.name)

            if title.id == title_id: first_tuple.append(my_tuple)
            else: choices_data.append(my_tuple)
        
        if len(first_tuple) > 0:
            choices_data = first_tuple + choices_data
        # -----   -----   -----   -----

        # Установите default значение для поля SelectField
        # -----   -----   -----   -----
        form.title.choices = choices_data
        # -----   -----   -----   -----

        func = 'admin.editorial_board_item'
        # -----   -----   -----   -----

        if form.validate_on_submit():

            if handler_type:
                db.session.add(EditorialBoardItems(
                    title_id = form.title.data,
                    text = form.text.data
                ))
                db.session.commit()

            else:
                item = EditorialBoardItems.query.filter_by(id=id).first()
                if item:
                    item.title_id = form.title.data
                    item.text = form.text.data
                    db.session.add(item)
                    db.session.commit()

            # -----   -----   -----   -----

            if add_type == 'addMoreBtn':
                flash('Успешно выполнено!')
                return redirect(url_for(
                    func, title_id = title_id,
                    handler_type = handler_type,
                    id = id,
                    add_type = 'None',
                ))
            
            elif add_type == 'addBtn':
                flash('Успешно выполнено!')
                return redirect(url_for('main.edition'))
            
        # -----   -----   -----   -----
        if handler_type == 0:
            item = EditorialBoardItems.query.filter_by(id=id).first()
            if item: form.text.data = item.text

    # -----   -----   -----   -----
    else:
        flash('Title не найден!')
        return redirect(url_for('main.edition'))
    # -----   -----   -----   -----
    return render_template(
        'editorial_board_item.html',
        form = form,
        form_name = 'Add Item',
        func = func,
        title_id = title_id,
        id = id,
        handler_type = handler_type,
        titles = titles,
    )


@admin.route("/editorial_board_item_delete/<int:id>", methods=['GET', 'POST'])
def editorial_board_item_delete(id):
    # -----   -----   -----   -----
    item = EditorialBoardItems.query.filter_by(id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for('main.edition'))








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
@admin.route("/add-admin", methods=['GET', 'POST'])
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
@admin.route("/admin-panel", methods=['GET', 'POST'])
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
@admin.route("/admin-edit", methods=['GET', 'POST'])
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
@admin.route("/admin-delete", methods=['GET', 'POST'])
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
@admin.route("/add-Volume", methods=['GET', 'POST'])
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
@admin.route("/edit-Volume/<int:id>", methods=['GET', 'POST'])
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
@admin.route("/delete-Volume/<int:id>")
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
@admin.route("/edd-category/<int:id>", methods=['GET', 'POST'])
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
@admin.route("/edit-category/<int:id>", methods=['GET', 'POST'])
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
@admin.route("/delete-category/<int:id>")
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
@admin.route("/add-article/<int:id>", methods=['GET', 'POST'])
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
@admin.route("/edit-article/<int:id>", methods=['GET', 'POST'])
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
@admin.route("/delete-article/<int:id>")
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








@admin.route("/left_bar/")
def left_bar():
    if 'login' in session:
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query

        numbers = LeftBar.query.order_by(LeftBar.id).all()
        if len(numbers) == 0:
            for i in range(1,7):
                numbers = LeftBar(image='0.gif')
                db.session.add(numbers)
            db.session.commit()
            numbers = LeftBar.query.order_by(LeftBar.id).all()
        return render_template(
            'left_bar.html', page_title = 'Edit left bar', numbers=numbers,
            volumes=volumes, categories_chek=categories_chek,)

    else: return redirect(url_for('main.home'))

@admin.route("/left_bar_add", methods=['GET', 'POST'])
def left_bar_add():
    if 'login' in session:
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query
        numbers = LeftBar.query.order_by(LeftBar.id).all()

        form = LeftBarForm()
        if form.validate_on_submit():
            image = form.image.data
            if image.filename != '':
                number = LeftBar.query.filter_by(image=image.filename).first()
                if number:
                    number = LeftBar(image=image.filename)
                else:
                    ext = image.filename.split('.')[-1]
                    folder_path = os.path.join('app', 'main', 'main-static', 'images', 'numbers')
                    if ext.lower() in ['gif', 'jpg', 'png', 'jpeg']:
                        number = LeftBar(image=image.filename)
                        image.save(os.path.join(folder_path, image.filename))
                    else:
                        flash('Разрешены только gif, jpg, png И jpeg форматы!')
                        return redirect(url_for('admin.left_bar_add'))
                try:
                    db.session.add(number)
                    db.session.commit()
                    flash('Изображение сохранёно!')
                    return redirect(url_for('admin.left_bar'))
                except:
                    flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                    return redirect(url_for('admin.left_bar_add'))
            else:
                flash('Вы отправили пустой файл! Пожалуйста, повторите попытку.')
                return redirect(url_for('admin.left_bar_add'))
        return render_template(
            'edit_left_bar.html', page_title = 'Add left bar', numbers=numbers,
            volumes=volumes, categories_chek=categories_chek,
            form_action=url_for('admin.left_bar_add'), form=form
            )

    else: return redirect(url_for('main.home'))



@admin.route("/left_bar_edit/<int:id>", methods=['GET', 'POST'])
def left_bar_edit(id):
    if 'login' in session:
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query
        numbers = LeftBar.query.order_by(LeftBar.id).all()

        form = LeftBarForm()
        folder_path = os.path.join('app', 'main', 'main-static', 'images', 'numbers')
        if form.validate_on_submit():
            image = form.image.data
            if image.filename != '':
                number = LeftBar.query.filter_by(id=id).first()
                if number:
                    if number.image == image.filename:
                        flash(
                            'У изображения одинаковое название со старым, поэтому не был изменён. Если хотите изменить попытайтесь ещё раз изменив название')
                        return redirect(url_for('admin.left_bar_edit', id=id))
                    else:
                        if os.path.exists(os.path.join(folder_path, image.filename)):
                            number.image = image.filename
                        else:
                            ext = image.filename.split('.')[-1]
                            if ext.lower() in ['gif', 'jpg', 'png', 'jpeg']:
                                number.image = image.filename
                                image.save(os.path.join(folder_path, image.filename))
                            else:
                                flash('Разрешены только gif, jpg, png И jpeg форматы!')
                                return redirect(url_for('admin.left_bar_edit', id=id))
                        try:
                            db.session.add(number)
                            db.session.commit()
                            flash('Изображение сохранёно!')
                            return redirect(url_for('admin.left_bar'))
                        except:
                            flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                            return redirect(url_for('admin.left_bar_add'))
            else:
                flash('Вы отправили пустой файл! Пожалуйста, повторите попытку.')
                return redirect(url_for('admin.left_bar_edit', id=id))
        return render_template(
            'edit_left_bar.html', page_title = 'Edit left bar', numbers=numbers,
            volumes=volumes, categories_chek=categories_chek,
            form_action=url_for('admin.left_bar_edit', id=id), form=form
            )

    else: return redirect(url_for('main.home'))


@admin.route("/left_bar_delete/<int:id>")
def left_bar_delete(id):
    if 'login' in session:
        numbers = LeftBar.query.all()
        number = LeftBar.query.filter_by(id=id).first()
        folder_path = os.path.join('app', 'main', 'main-static', 'images', 'numbers')
        if len(numbers) <= 6:
            exists_images =  LeftBar.query.filter_by(image=number.image).all()
            if len(exists_images) == 1 and number.image != '0.gif':
                if os.path.exists(os.path.join(folder_path, number.image)):
                    os.remove(os.path.join(folder_path, number.image))
            number.image = '0.gif'
            db.session.add(number)
        elif len(numbers) > 6:
            exists_images =  LeftBar.query.filter_by(image=number.image).all()
            if len(exists_images) == 1 and number.image != '0.gif':
                if os.path.exists(os.path.join(folder_path, number.image)):
                    os.remove(os.path.join(folder_path, number.image))
            db.session.delete(number)
            
        db.session.commit()
        return redirect(url_for('admin.left_bar'))

    else: return redirect(url_for('main.home'))







@admin.route("/right_bar/", methods=['GET', 'POST'])
def right_bar():
    if 'login' in session:
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query
        folder_path = os.path.join('app', 'main', 'main-static', 'images', 'right_bar')

        form = RightBarForm()
        right_bar = RightBar.query.first()
        if right_bar == None:
            right_bar = RightBar(
                image_1 = 'right1.png', image_2 = 'right2.jpg',
                text_1 = 'The Impact Factor for 2020 = 0.615', text_2 = 'Web Usage Statistics',
                text_3 = 'ACCEPTED ARTICLES', text_4 = 'Table of Contents',
                text_5 = 'Accepted articles are corrected proof articles in which final details need to be futher assigned.',
            )
            db.session.add(right_bar)
            db.session.commit()

        if form.validate_on_submit():
            images = [form.image_1.data, form.image_2.data]
            right_bar = RightBar.query.first()

            for image in images:
                if image.filename != '':
                    # -----------------------------------------------------------
                    if os.path.exists(os.path.join(folder_path, right_bar.image_1)) and \
                        os.path.exists(os.path.join(folder_path, right_bar.image_2)):
                        
                        ext = image.filename.split('.')[-1].lower()
                        if ext in ['gif', 'jpg', 'png', 'jpeg']:
                            # -----------------------------------------------------------------------
                            if image == form.image_1.data:
                                os.remove(os.path.join(folder_path, right_bar.image_1))
                                filename = f'right1.{ext}'
                                right_bar.image_1 = filename
                            else:
                                os.remove(os.path.join(folder_path, right_bar.image_2))
                                filename = f'right2.{ext}'
                                right_bar.image_2 = filename
                            # --------------------------------------------------
                            try:
                                db.session.add(right_bar)
                                db.session.commit()
                            except:
                                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                                return redirect(url_for('admin.right_bar'))
                            image.save(os.path.join(folder_path, filename))
                        else:
                            flash('Разрешены только gif, jpg, png И jpeg форматы!')
                            return redirect(url_for('admin.right_bar'))
                        # -----------------------------------------------------------
            try:
                right_bar.text_1 = form.text_1.data
                right_bar.text_2 = form.text_2.data
                right_bar.text_3 = form.text_3.data
                right_bar.text_4 = form.text_4.data
                right_bar.text_5 = form.text_5.data
                db.session.add(right_bar)
                db.session.commit()
                flash('Изменения сохранёны!')
                return redirect(url_for('main.home'))
            except:
                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                return redirect(url_for('admin.right_bar'))
        
        right_bar = RightBar.query.first()
        
        form.text_1.data = right_bar.text_1
        form.text_2.data = right_bar.text_2
        form.text_3.data = right_bar.text_3
        form.text_4.data = right_bar.text_4
        form.text_5.data = right_bar.text_5
        

        return render_template(
            'right_bar.html', page_title = 'Edit right bar', form=form,
            volumes=volumes, categories_chek=categories_chek, form_action=url_for('admin.right_bar'))

    else: return redirect(url_for('main.home'))









@admin.route("/main_data/", methods=['GET', 'POST'])
def main_data():
    if 'login' in session:
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query
        folder_path = os.path.join('app', 'main', 'main-static', 'images', 'main_data')

        form = MainDataForm()
        data = MainData.query.first()
        if data == None:
            data = MainData(
                line_text_first = '''
                ***ScienceAsia has started the online published ahead of print from the issue 48(3),
                  2022 onwards. *** ''',
                line_text_last = '''
                  ::Authors please consult the Instructions for Authors updated on May 1,
                    2021 before preparing your manuscript.
                      Use of manuscript template is recommended.''',
                volume_image = 'item1.jpg',
                volume_name = 'Volume 48 Number 6 (December 2022)',
                issues_in_prog = 'In progress issues contain online articles which are citable using their doi numbers.',
            )
            db.session.add(data)
            db.session.commit()

        if form.validate_on_submit():
            image = form.volume_image.data
            data = MainData.query.first()

            if image.filename != '':
                # -----------------------------------------------------------
                if os.path.exists(os.path.join(folder_path, data.volume_image)):
                    
                    ext = image.filename.split('.')[-1].lower()
                    if ext in ['gif', 'jpg', 'png', 'jpeg']:
                        # -----------------------------------------------------------------------
                        os.remove(os.path.join(folder_path, data.volume_image))
                        filename = f'item1.{ext}'
                        data.volume_image = filename
                        # --------------------------------------------------
                        try:
                            db.session.add(data)
                            db.session.commit()
                        except:
                            flash('Ошибка при сохранении изображения! Пожалуйста, повторите попытку.')
                            return redirect(url_for('admin.main_data'))
                        image.save(os.path.join(folder_path, filename))
                    else:
                        flash('Разрешены только gif, jpg, png И jpeg форматы!')
                        return redirect(url_for('admin.main_data'))
                    # -----------------------------------------------------------
            try:
                data.line_text_first = form.line_text_first.data
                data.line_text_last = form.line_text_last.data
                data.volume_name = form.volume_name.data
                data.issues_in_prog = form.issues_in_prog.data
                db.session.add(data)
                db.session.commit()
                flash('Изменения сохранёны!')
                return redirect(url_for('main.home'))
            except:
                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                return redirect(url_for('admin.main_data'))
        
        data = MainData.query.first()
        
        form.line_text_first.data = data.line_text_first
        form.line_text_last.data = data.line_text_last
        form.volume_name.data = data.volume_name
        form.issues_in_prog.data = data.issues_in_prog
        

        return render_template(
            'main_data.html', page_title = 'Edit main', form=form,
            volumes=volumes, categories_chek=categories_chek, form_action=url_for('admin.main_data'))

    else: return redirect(url_for('main.home'))













@admin.route("/add_main_catalog", methods=['GET', 'POST'])
def add_main_catalog():
    if 'login' in session:
        url = url_for('admin.add_main_catalog')
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query

        form = MainCatalogsForm()
        if form.validate_on_submit():
            data = MainCatalogs(name=form.name.data)
            try:
                db.session.add(data)
                db.session.commit()
                flash('Успешно сохранено!')
                return redirect(url)
            except:
                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                return redirect(url)
        
        return render_template(
            'main_catalog.html', page_title = 'Add catalog', form=form,
            volumes=volumes, categories_chek=categories_chek, form_action=url)

    else: return redirect(url_for('main.home'))


@admin.route("/edit_main_catalog/<int:id>", methods=['GET', 'POST'])
def edit_main_catalog(id):
    if 'login' in session:
        url = url_for('admin.edit_main_catalog', id=id)
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query

        form = MainCatalogsForm()
        data = MainCatalogs.query.filter_by(id=id).first()
        if form.validate_on_submit():
            try:
                data.name = form.name.data
                db.session.add(data)
                db.session.commit()
                flash('Изменения сохранёны!')
                return redirect(url_for('main.home'))
            except:
                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                return redirect(url)
        
        form.name.data = data.name
        return render_template(
            'main_catalog.html', page_title = 'Edit catalog', form=form,
            volumes=volumes, categories_chek=categories_chek, form_action=url)

    else: return redirect(url_for('main.home'))


@admin.route("/delete_main_catalog/<int:id>", methods=['GET', 'POST'])
def delete_main_catalog(id):
    if 'login' in session:
        data = MainCatalogs.query.filter_by(id=id).first()
        try:
            db.session.delete(data)
            db.session.commit()
            flash('Успешно удалено!')
            return redirect(url_for('main.home'))
        except:
            flash('Ошибка при удалении! Пожалуйста, повторите попытку.')
            return redirect(url_for('main.home'))
        
    else: return redirect(url_for('main.home'))











@admin.route("/add_recent_supplement", methods=['GET', 'POST'])
def add_recent_supplement():
    if 'login' in session:
        url = url_for('admin.add_recent_supplement')
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query

        form = RecentSupplementForm()
        folder_path = os.path.join('app', 'main', 'main-static', 'images', 'recent_supplement')
        # -------------------------------------------------------------------------------------
        if form.validate_on_submit():
            image = form.image.data
            filename = image.filename
            # -----------------------

            if filename != '':
                ext = filename.split('.')[-1].lower()
                if ext in ['gif', 'jpg', 'png', 'jpeg']:
                    # -----------------------------------------------------------------------
                    check_data = RecentSupplement.query.filter_by(image=filename).first()
                    if check_data: filename = f'{filename}_duble.{ext}'
                    # ---------------------------------------------
                    image.save(os.path.join(folder_path, filename))
                    # ---------------------------------------------
                    try:
                        data = RecentSupplement(
                            image=filename, text=form.text.data,
                            link=form.link.data,
                        )
                        db.session.add(data)
                        db.session.commit()
                        flash('Успешно сохранёно!')
                        return redirect(url_for('main.home'))
                    except:
                        flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                        return redirect(url)
                else:
                    flash('Разрешены только gif, jpg, png и jpeg форматы!')
                    return redirect(url)
                # ---------------------------------------------------------- 
        return render_template(
            'recent_supplement.html', page_title = 'Add recent supplement', form=form,
            volumes=volumes, categories_chek=categories_chek, form_action=url)

    else: return redirect(url_for('main.home'))


@admin.route("/edit_recent_supplement/<int:id>", methods=['GET', 'POST'])
def edit_recent_supplement(id):
    if 'login' in session:
        url = url_for('admin.edit_recent_supplement', id=id)
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query

        form = RecentSupplementForm()
        data = RecentSupplement.query.filter_by(id=id).first()
        folder_path = os.path.join('app', 'main', 'main-static', 'images', 'recent_supplement')
        if form.validate_on_submit():
            image = form.image.data

            if image.filename != '':
                # -----------------------------------------------------------
                if os.path.exists(os.path.join(folder_path, data.image)):
                    
                    ext = image.filename.split('.')[-1].lower()
                    if ext in ['gif', 'jpg', 'png', 'jpeg']:
                        # -----------------------------------------------------------------------
                        filename = image.filename
                        check_data = RecentSupplement.query.filter_by(image=filename).first()
                        if check_data: filename = f'{filename}_duble.{ext}'
                        os.remove(os.path.join(folder_path, data.image))
                        data.image = filename
                        # --------------------------------------------------
                        try:
                            db.session.add(data)
                            db.session.commit()
                        except:
                            flash('Ошибка при сохранении изображения! Пожалуйста, повторите попытку.')
                            return redirect(url)
                        image.save(os.path.join(folder_path, filename))
                    else:
                        flash('Разрешены только gif, jpg, png И jpeg форматы!')
                        return redirect(url)
                    # -----------------------------------------------------------
            try:
                data.text = form.text.data
                data.link = form.link.data
                db.session.add(data)
                db.session.commit()
                flash('Успешно сохранёно!')
                return redirect(url_for('main.home'))
            except:
                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                return redirect(url)
        
        form.text.data = data.text
        form.link.data = data.link
        

        return render_template(
            'recent_supplement.html', page_title='Edit recent supplement', form=form,
            volumes=volumes, categories_chek=categories_chek, form_action=url)

    else: return redirect(url_for('main.home'))


@admin.route("/delete_recent_supplement/<int:id>", methods=['GET', 'POST'])
def delete_recent_supplement(id):
    if 'login' in session:
        data = RecentSupplement.query.filter_by(id=id).first()
        folder_path = os.path.join('app', 'main', 'main-static', 'images', 'recent_supplement')
        if os.path.exists(os.path.join(folder_path, data.image)):
            try:
                os.remove(os.path.join(folder_path, data.image))
                db.session.delete(data)
                db.session.commit()
                flash('Успешно удалено!')
                return redirect(url_for('main.home'))
            except:
                flash('Ошибка при удалении! Пожалуйста, повторите попытку.')
                return redirect(url_for('main.home'))
        
    else: return redirect(url_for('main.home'))








@admin.route("/add_issues_progress", methods=['GET', 'POST'])
def add_issues_progress():
    if 'login' in session:
        url = url_for('admin.add_issues_progress')
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query

        form = IssuesProgressForm()
        if form.validate_on_submit():
            try:
                data = IssuesProgress(text=form.text.data, link=form.link.data)
                db.session.add(data)
                db.session.commit()
                flash('Успешно сохранёно!')
                return redirect(url_for('main.home'))
            except:
                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                return redirect(url)
                # ---------------------------------------------------------- 
        return render_template(
            'issues_progress.html', page_title = 'Add issues progress', form=form,
            volumes=volumes, categories_chek=categories_chek, form_action=url)

    else: return redirect(url_for('main.home'))


@admin.route("/edit_issues_progress/<int:id>", methods=['GET', 'POST'])
def edit_issues_progress(id):
    if 'login' in session:
        url = url_for('admin.edit_issues_progress', id=id)
        volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
        categories_chek = Categories.query

        data = IssuesProgress.query.filter_by(id=id).first()
        form = IssuesProgressForm()
        if form.validate_on_submit():
            try:
                data.text = form.text.data
                data.link = form.link.data
                db.session.add(data)
                db.session.commit()
                flash('Изменения сохранёны!')
                return redirect(url_for('main.home'))
            except:
                flash('Ошибка при сохранении! Пожалуйста, повторите попытку.')
                return redirect(url)
        if data:
            form.text.data = data.text
            form.link.data = data.link
        

        return render_template(
            'issues_progress.html', page_title='Edit issues progress', form=form,
            volumes=volumes, categories_chek=categories_chek, form_action=url)

    else: return redirect(url_for('main.home'))


@admin.route("/delete_issues_progress/<int:id>", methods=['GET', 'POST'])
def delete_issues_progress(id):
    if 'login' in session:
        data = IssuesProgress.query.filter_by(id=id).first()
        if data:
            try:
                db.session.delete(data)
                db.session.commit()
                flash('Успешно удалено!')
                return redirect(url_for('main.home'))
            except:
                flash('Ошибка при удалении! Пожалуйста, повторите попытку.')
                return redirect(url_for('main.home'))
        else: 
            flash('Ошибка при удалении! Неправильное имя.')
            return redirect(url_for('main.home'))
    else: return redirect(url_for('main.home'))