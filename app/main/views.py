from flask import render_template, url_for, redirect, flash
from . import main
from ..dbModels import LeftMenu, Categories, Jurnals



@main.route("/")
def home():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('home.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/publication")
def public():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('publication.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/editorial_board/")
def edition():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('edition.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/subscription")
def sub():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('subscription.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/journal")
def journal():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('Journal.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/instruction")
def instruction():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('instruction.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/online_submission")
def submission():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('submission.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/time_frame")
def status():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('status.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/author_login")
def author():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('author_login.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/review_login")
def review():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('reviewer_login.html', volumes=volumes, categories_chek=categories_chek)



def next_page(value):
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    volume = LeftMenu.query
    v_id = []
    for i in volumes:
        v_id.append(i.id)

    
    a = v_id.index(value)

    if a-1<0:first=False
    elif a-1>=0:
        i_1 = v_id[a-1]
        name_1 = volume.filter_by(id=i_1).first().name
        first = [i_1, name_1]
    
    if a+1>len(v_id)-1:next_p=False
    elif a+1<=len(v_id)-1:
        i_3 = v_id[a+1]
        name_3 = volume.filter_by(id=i_3).first().name
        next_p = [i_3, name_3]

    return [first, next_p]




@main.route("/content/content=<int:id>")
def volume_1(id):
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    volume = LeftMenu.query.filter_by(id=id).first()
    
    categories = Categories.query.filter_by(left_menu=id).all()
    jurnals = Jurnals.query
    pages = next_page(id)

    return render_template(
        'valume48_2.html',
        volumes=volumes, categories_chek=categories_chek,
        volume=volume,
        categories=categories,
        pages=pages,
        id=id,
        jurnals=jurnals)









@main.route("/abstract/abstract=<int:id>")
def abstract(id):
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    article = Jurnals.query.filter_by(id=id).first()
    return render_template(
        'abstract.html',
        volumes=volumes, categories_chek=categories_chek,
        article=article
        )






@main.route("/earlier_issues")
def earlier():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('earlier.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/2022")
def last_year():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('2022.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/supplementary")
def supple():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('supplementary.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/about")
def about():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('about.html', volumes=volumes, categories_chek=categories_chek)


@main.route("/contact")
def contact():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('contact.html', volumes=volumes, categories_chek=categories_chek)
