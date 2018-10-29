from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_input = StringField('search', render_kw={"class":"form-control mr-sm-2", "type":"text", "placeholder":"Search...", "aria-label":"Search"})
