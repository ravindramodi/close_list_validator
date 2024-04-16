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
        exact_matches, similar_values, highlighted_html_text, highlighted_close_list = search_close_list(close_list_values, html_text, 0.7)

        return render_template('index.html',
                               normal_text=normal_text,
                               close_list_values=highlighted_close_list,
                               exact_matches=exact_matches,
                               similar_values=similar_values,
                               highlighted_html_text=highlighted_html_text)

    return render_template('index.html')

def html_to_text(html_text):
    return html_text.replace('<', '&lt;').replace('>', '&gt;')

def process_close_list(close_list):
    return [item.strip() for item in close_list.split(',')]

def search_close_list(close_list_values, html_text, similarity_cutoff):
    exact_matches = []
    similar_values = []
    highlighted_html_text = html_text
    highlighted_close_list = []

    for value in close_list_values:
        if value in html_text:
            exact_matches.append(f'<span style="color:green;">{value}</span>')
            highlighted_close_list.append(f'<span style="color:green;">{value}</span>')
            highlighted_html_text = highlighted_html_text.replace(value, f'<span style="color:green;">{value}</span>')
        else:
            similar_values_found = difflib.get_close_matches(value, html_text.split(), n=1, cutoff=similarity_cutoff)
            if similar_values_found:
                similar_value = similar_values_found[0]
                similar_values.append(f'<span style="color:red;">{value}</span>')
                highlighted_close_list.append(f'<span style="color:red;">{value}</span>')
                highlighted_html_text = highlighted_html_text.replace(similar_value, f'<span style="color:red;">{similar_value}</span>')
            else:
                # Check for hyphen-separated values
                value_parts = value.split('-')
                if len(value_parts) > 1:
                    for part in value_parts:
                        similar_values_found = difflib.get_close_matches(part, html_text.split(), n=1, cutoff=similarity_cutoff)
                        if similar_values_found:
                            similar_value = similar_values_found[0]
                            similar_values.append(f'<span style="color:red;">{value}</span>')
                            highlighted_close_list.append(f'<span style="color:red;">{value}</span>')
                            highlighted_html_text = highlighted_html_text.replace(similar_value, f'<span style="color:red;">{similar_value}</span>')
                            break

    return '|'.join(exact_matches), '|'.join(similar_values), highlighted_html_text, '|'.join(highlighted_close_list)

if __name__ == '__main__':
    app.run(debug=True)