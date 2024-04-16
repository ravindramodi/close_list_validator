from flask import Flask, render_template, request
import difflib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        html_text = request.form['html_text']
        close_list = request.form['close_list']

        # Convert HTML text to normal text
        normal_text = html_to_text(html_text)

        # Process the "Close List" input
        close_list_values = process_close_list(close_list)

        # Search for exact matches and similar values in the HTML text
        exact_matches, similar_values = search_close_list(close_list_values, html_text)

        return render_template('index.html',
                               normal_text=normal_text,
                               close_list_values=close_list_values,
                               exact_matches=exact_matches,
                               similar_values=similar_values)

    return render_template('index.html')

def html_to_text(html_text):
    return html_text.replace('<', '&lt;').replace('>', '&gt;')

def process_close_list(close_list):
    return [item.strip() for item in close_list.split(',')]

def search_close_list(close_list_values, html_text):
    exact_matches = []
    similar_values = []

    for value in close_list_values:
        if value in html_text:
            exact_matches.append(value)
        else:
            similar_values_found = difflib.get_close_matches(value, html_text.split(), n=1)
            if similar_values_found:
                similar_values.append(value)

    return '|'.join(exact_matches), '|'.join(similar_values)

if __name__ == '__main__':
    app.run(debug=True)