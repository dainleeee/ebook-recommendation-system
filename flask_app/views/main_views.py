from flask import Blueprint, render_template
from similarity  import load_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/',methods=['GET'])
def index():
    ebook_df = load_data()
    title = ebook_df['title']
    return render_template('index.html',title=title), 200