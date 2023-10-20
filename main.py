
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
import json
app = Flask(__name__)


# Загрузка данных из JSON-файла
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Сохранение данных в JSON-файл
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/', methods=['GET', 'POST'])
def create_paste():
    if request.method == 'POST':
        text = request.form['text']
        pastas = load_data()
        print(pastas)
        pasta_id = len(pastas) + 1
        pastas[pasta_id] = text

        # Сохраняем пасты в файл JSON
        save_data(pastas)

        return f"Ваша паста создана! <a href='/paste/{pasta_id}'>Посмотреть пасту</a>"

    return render_template('index.html')

@app.route('/paste/<int:pasta_id>')
def view_paste(pasta_id):
    pastas = load_data()
    pasta = pastas[pasta_id]
    if pasta is not None:
        return render_template('view_paste.html', pasta=pasta)
    return "Пасты не найдено."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
