# Blueprint 
from flask import Blueprint

bp = Blueprint("foo", __name__, url_prefix="/foo")

@bp.route("/bar")
def bar ():
    return "foobar";
