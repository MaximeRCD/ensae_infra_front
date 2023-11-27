from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__, static_url_path='/static', static_folder='static')

# @app.route("/")
# def hello_world():
#     return render_template('form.html')


cards = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        if text.strip():
            # Create a dictionary to represent a card
            card = {'text': text}
            cards.append(card)
    return render_template('form.html', cards=cards)


@app.route('/validate_and_print', methods=['POST'])
def validate_and_print():
    # Transform cards into a list and print
    cards_list = [card['text'] for card in cards]
    print(cards_list)  # This will print the list of card texts in CMD
    # Redirect back to the index page
    cards.clear()

    return redirect(url_for('index'))
