from flask import Flask, render_template, request

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

        return render_template('index.html', normal_text=normal_text, close_list_values=close_list_values)

    return render_template('index.html')

def html_to_text(html_text):
    # Your HTML to text conversion logic here
    return html_text.replace('<', '&lt;').replace('>', '&gt;')

def process_close_list(close_list):
    # Your logic to process the "Close List" input here
    return close_list.split(',')

if __name__ == '__main__':
    app.run(debug=True)