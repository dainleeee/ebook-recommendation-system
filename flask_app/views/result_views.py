from flask import Blueprint, render_template, request
from similarity  import get_recommendations

result_bp = Blueprint('result', __name__)

@result_bp.route('/result', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('result.html')
    else:

        title = request.form['link']
        ebooks = get_recommendations(title)

        return render_template('result.html', ebooks=ebooks, title=title)