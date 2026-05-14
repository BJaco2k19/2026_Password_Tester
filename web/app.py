from flask import Flask, render_template, request, jsonify
from password_strength import score_password, suggest_improvements

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    pw = ''
    if request.method == 'POST':
        pw = request.form.get('password', '')
        result = score_password(pw)
        result['suggestions'] = suggest_improvements(pw)
    return render_template('index.html', result=result, password=pw)


@app.route('/api/score', methods=['POST'])
def api_score():
    data = request.get_json() or {}
    pw = data.get('password', '')
    result = score_password(pw)
    result['suggestions'] = suggest_improvements(pw)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
