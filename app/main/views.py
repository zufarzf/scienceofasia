from flask import render_template, url_for, redirect, flash
from . import main
from app import db
from ..dbModels import LeftMenu, Categories, Jurnals, LeftBar, RightBar, MainData
from ..dbModels import MainCatalogs, RecentSupplement, IssuesProgress
from ..dbModels import EditorialBoardTitles, EditorialBoardItems



@main.route("/")
def home():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    numbers = LeftBar.query.order_by(LeftBar.id).all()
    right_bar = RightBar.query.first()

    if len(numbers) == 0:
        for i in range(1,7):
            numbers = LeftBar(image='0.gif')
            db.session.add(numbers)
        db.session.commit()
    if right_bar == None:
        right_bar = RightBar(
            image_1 = 'right1.png', image_2 = 'right2.jpg',
            text_1 = 'The Impact Factor for 2020 = 0.615', text_2 = 'Web Usage Statistics',
            text_3 = 'ACCEPTED ARTICLES', text_4 = 'Table of Contents',
            text_5 = 'Accepted articles are corrected proof articles in which final details need to be futher assigned.',
        )
        db.session.add(right_bar)
        db.session.commit()

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
        
    numbers = LeftBar.query.order_by(LeftBar.id).all()
    right_bar = RightBar.query.first()
    data = MainData.query.first()
    value_list_1 = MainCatalogs.query.order_by(MainCatalogs.id).all()
    recent_supplement = RecentSupplement.query.order_by(RecentSupplement.id).all()
    issues_progress = IssuesProgress.query.order_by(IssuesProgress.id).all()


    return render_template(
        'home.html', volumes=volumes, numbers=numbers, data=data, recent_supplement=recent_supplement,
        right_bar=right_bar, categories_chek=categories_chek, value_list_1=value_list_1, issues_progress=issues_progress)



@main.route("/publication")
def public():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    return render_template('publication.html', volumes=volumes, categories_chek=categories_chek)





@main.route("/editorial_board/")
def edition():
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query

    titles = EditorialBoardTitles.query.order_by(EditorialBoardTitles.id).all()
    items =  EditorialBoardItems.query.order_by(EditorialBoardItems.id).all()

    return render_template(
        'edition.html',
        volumes=volumes,
        categories_chek=categories_chek,
        titles=titles,
        items=items,
        )





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










# ==================================
def get_page_first_number(text:str):
    if '): ' in text:
        a = text.replace(' ', '').split('):')[-1]
        page_first_number = str(a).split('-')[0]
        return page_first_number


def min_dict(values_list:list):
    counter = values_list[0]
    for i in values_list:
        counter_number = get_page_first_number(counter['doi_text'])
        page_first_number = get_page_first_number(i['doi_text'])
        
        print()
        print()
        print(f'counter[doi_text]= {counter["doi_text"]}')
        print(f'i[doi_text]= {i["doi_text"]}')
        print()
        print()
        try:
            if int(page_first_number) < int(counter_number):
                counter = i
        except:
            counter = i
    return counter
# ==================================


@main.route("/content/content=<int:id>")
def volume_1(id):
    volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
    categories_chek = Categories.query
    volume = LeftMenu.query.filter_by(id=id).first()
    
    categories = Categories.query.filter_by(left_menu=id).all()
    jurnals_cheked = Jurnals.query
    jurnals = Jurnals.query.filter_by(menu_id=id).all()
    pages = next_page(id)
    # ---------------------------
    result = []
    for c in categories:
        jurnals = Jurnals.query.filter_by(menu_id=c.id).all()
    
        jurnals_list = []
        sort_list = []

        for i in jurnals:
            article_dict = {
                'id':i.id, 'title':i.title,
                'authors':i.authors, 'authors_sup':i.authors_sup,
                'abstract':i.abstract, 'pdf_url':i.pdf_url,
                'doi_text':i.doi_text, 'downloads':i.downloads,
                'Views':i.Views, 'sub_text':i.sub_text,
                'author_email':i.author_email, 'received_date':i.received_date,
                'accepted_date':i.accepted_date, 'valid_articles':i.valid_articles,
                'menu_id':i.menu_id,
            }
            jurnals_list.append(article_dict)
        
        while len(jurnals_list) != 0:
            small_dict = min_dict(jurnals_list)
            sort_list.append(jurnals_list.pop(jurnals_list.index(small_dict)))

        
        result.append([c.id, sort_list])
    
    return render_template(
        'valume48_2.html',
        volumes=volumes, categories_chek=categories_chek,
        volume=volume,
        categories=categories,
        pages=pages,
        id=id,
        jurnals_cheked=jurnals_cheked,
        jurnals=result)



# @main.route("/content/content=<int:id>")
# def volume_1(id):
#     volumes = LeftMenu.query.order_by(LeftMenu.id.desc()).all()
#     categories_chek = Categories.query
#     volume = LeftMenu.query.filter_by(id=id).first()
    
#     categories = Categories.query.filter_by(left_menu=id).all()
#     jurnals = Jurnals.query
#     pages = next_page(id)

#     return render_template(
#         'valume48_2.html',
#         volumes=volumes, categories_chek=categories_chek,
#         volume=volume,
#         categories=categories,
#         pages=pages,
#         id=id,
#         jurnals=jurnals)










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
