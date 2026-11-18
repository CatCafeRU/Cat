from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Contact(db.Model):
    __tablename__ = 'cafe_contact'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250))
    address_en = db.Column(db.String(250))
    hours = db.Column(db.String(150))
    hours_en = db.Column(db.String(150))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(254))
    map_url = db.Column(db.String(200))
    social_url = db.Column(db.String(200))


class SocialLink(db.Model):
    __tablename__ = 'cafe_sociallink'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(200))
    sort_order = db.Column(db.Integer)
    active = db.Column(db.Boolean)


class Page(db.Model):
    __tablename__ = 'cafe_page'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    title_en = db.Column(db.String(200))
    body_en = db.Column(db.Text)
    image = db.Column(db.String(100))
    team_image = db.Column(db.String(100))


class MenuItem(db.Model):
    __tablename__ = 'cafe_menuitem'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    category_en = db.Column(db.String(100))
    name = db.Column(db.String(150))
    name_en = db.Column(db.String(150))
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    price = db.Column(db.Numeric(9, 2))
    icon = db.Column(db.String(10))
    sort_order = db.Column(db.Integer)
    active = db.Column(db.Boolean)


class Cat(db.Model):
    __tablename__ = 'cafe_cat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    bio = db.Column(db.Text)
    bio_en = db.Column(db.Text)
    photo = db.Column(db.String(100))
    sort_order = db.Column(db.Integer)
    active = db.Column(db.Boolean)


class Promotion(db.Model):
    __tablename__ = 'cafe_promotion'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    starts_at = db.Column(db.Date)
    ends_at = db.Column(db.Date)
    active = db.Column(db.Boolean)
    show_banner = db.Column(db.Boolean)


class Coupon(db.Model):
    __tablename__ = 'cafe_coupon'
    id = db.Column(db.Integer, primary_key=True)
    promotion_id = db.Column(db.Integer, db.ForeignKey('cafe_promotion.id'))
    code = db.Column(db.String(80), unique=True)
    discount = db.Column(db.String(80))
    discount_type = db.Column(db.String(10))
    discount_value = db.Column(db.Numeric(9, 2))
    min_order = db.Column(db.Numeric(9, 2))
    discount_en = db.Column(db.String(80))
    conditions = db.Column(db.Text)
    conditions_en = db.Column(db.Text)
    active = db.Column(db.Boolean)

    promotion = db.relationship('Promotion', backref='coupons')


class Slide(db.Model):
    __tablename__ = 'cafe_slide'
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(200))
    caption_en = db.Column(db.String(200))
    image = db.Column(db.String(100))
    sort_order = db.Column(db.Integer)
    active = db.Column(db.Boolean)