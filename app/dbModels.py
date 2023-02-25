from . import db


class Admins(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    psw = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Admins: <id: {self.id}>, <name: {self.name}>'





class LeftMenu(db.Model):
    __tablename__ = 'leftmenu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    date = db.Column(db.String(300))
    cover_image = db.Column(db.Text, default=' ')
    photographed = db.Column(db.String(300), default=' ')

    categories = db.relationship('Categories', backref='leftmenu', lazy='dynamic')

    def __repr__(self):
        return f'leftmenu: <id: {self.id}>, <name: {self.name}>, <type: {self.date}>'



class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)

    left_menu = db.Column(db.Integer, db.ForeignKey('leftmenu.id'))
    jurnals = db.relationship('Jurnals', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'Categories: <id: {self.id}>, <name: {self.name}>, <type: {self.left_menu}>'


class Jurnals(db.Model):
    __tablename__ = 'jurnals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), default=' ') #ckeditor
    authors = db.Column(db.String(500), default=' ')
    authors_sup = db.Column(db.String(1000), default=' ') #ckeditor
    abstract = db.Column(db.Text, default=' ')
    pdf_url = db.Column(db.String(500))
    # ----------------------------
    doi_text = db.Column(db.String(1000), default=' ') #ckeditor
    downloads = db.Column(db.Integer, default=' ')
    Views = db.Column(db.Integer, default=' ')
    # ----------------------------
    sub_text = db.Column(db.Text, default=' ')
    author_email = db.Column(db.String(200), default=' ')
    # ----------------------------
    received_date = db.Column(db.String(200), default=' ')
    accepted_date = db.Column(db.String(200), default=' ')
    # ----------------------------
    valid_articles = db.Column(db.Boolean, default=False)

    menu_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return f'Jurnls: <id: {self.id}>, <title: {self.title}>'


class LeftBar(db.Model):
    __tablename__ = 'left_bar'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150))

    def __repr__(self):
        return f'Jurnls: <id: {self.id}>, <title: {self.image}>'
    


class RightBar(db.Model):
    __tablename__ = 'right_bar'
    id = db.Column(db.Integer, primary_key=True)
    image_1 = db.Column(db.String(150))
    image_2 = db.Column(db.String(150))
    text_1 = db.Column(db.String(300))
    text_2 = db.Column(db.String(300))
    text_3 = db.Column(db.String(300))
    text_4 = db.Column(db.String(300))
    text_5 = db.Column(db.Text)



class MainData(db.Model):
    __tablename__ = 'main_data'
    id = db.Column(db.Integer, primary_key=True)
    line_text_first = db.Column(db.Text)
    line_text_last = db.Column(db.Text)
    volume_image = db.Column(db.String(150))
    volume_name = db.Column(db.String(300))
    issues_in_prog = db.Column(db.Text)



class MainCatalogs(db.Model):
    __tablename__ = 'main_catalogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))





class RecentSupplement(db.Model):
    __tablename__ = 'recent_supplement'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150))
    text = db.Column(db.String(300))
    link = db.Column(db.String(300), default='Table of Contents')


class IssuesProgress(db.Model):
    __tablename__ = 'issues_progress'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    link = db.Column(db.String(300))