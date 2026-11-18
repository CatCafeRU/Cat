import os
from datetime import date
from pathlib import Path

from flask import Flask, render_template, send_from_directory, abort, url_for

from models import (
    db, Contact, SocialLink, Page, MenuItem, Cat, Promotion, Coupon, Slide,
)

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLITE_PATH', f'sqlite:///{BASE_DIR / "db.sqlite3"}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MEDIA_ROOT'] = BASE_DIR / 'media'

db.init_app(app)


@app.context_processor
def inject_globals():
    return {
        'contact': Contact.query.first(),
        'social_links': (
            SocialLink.query
            .filter_by(active=True)
            .order_by(SocialLink.sort_order, SocialLink.id)
            .all()
        ),
    }


def current_promotions():
    today = date.today()
    promos = Promotion.query.filter_by(active=True).all()
    return [
        p for p in promos
        if (p.starts_at is None or p.starts_at <= today)
        and (p.ends_at is None or p.ends_at >= today)
    ]


@app.route('/')
def home():
    slides = (
        Slide.query.filter_by(active=True)
        .order_by(Slide.sort_order, Slide.id).all()
    )
    cats = (
        Cat.query.filter_by(active=True)
        .order_by(Cat.sort_order, Cat.id).limit(3).all()
    )
    banners = [p for p in current_promotions() if p.show_banner]
    about = Page.query.filter_by(slug='about').first()
    return render_template('home.html',
                           slides=slides, cats=cats,
                           banners=banners, about=about)


@app.route('/menu/')
@app.route('/menu')
def menu():
    items = (
        MenuItem.query.filter_by(active=True)
        .order_by(MenuItem.sort_order, MenuItem.id).all()
    )
    grouped = {}
    for it in items:
        grouped.setdefault(it.category, []).append(it)
    return render_template('menu.html', grouped=grouped)


@app.route('/cats/')
@app.route('/cats')
def cats():
    cats = (
        Cat.query.filter_by(active=True)
        .order_by(Cat.sort_order, Cat.id).all()
    )
    return render_template('cats.html', cats=cats)


@app.route('/promotions/')
@app.route('/promotions')
def promotions():
    promos = current_promotions()
    active_coupons = {}
    for p in promos:
        active_coupons[p.id] = [c for c in p.coupons if c.active]
    return render_template('promotions.html',
                           promotions=promos,
                           active_coupons=active_coupons)


@app.route('/about/')
@app.route('/about')
def about():
    page = Page.query.filter_by(slug='about').first()
    if not page:
        abort(404)
    return render_template('about.html', page=page)


@app.route('/contacts/')
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(app.config['MEDIA_ROOT'], filename)


@app.errorhandler(404)
def not_found(_e):
    return render_template('404.html'), 404


# шаблонный фильтр для Decimal → «1 234 ₽»
@app.template_filter('price')
def price_filter(value):
    if value is None:
        return ''
    try:
        s = f'{value:.2f}'.rstrip('0').rstrip('.')
    except Exception:
        s = str(value)
    return s


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)