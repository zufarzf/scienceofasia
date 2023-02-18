from flask import Blueprint

admin = Blueprint(
    'admin',
    __name__,
    template_folder='admin-templates',
    static_folder='admin-static'
)

from . import views
