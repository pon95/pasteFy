from flask import Flask, render_template, request
import json
import os

app = Flask(__name__, static_folder='G:/pasteFy/js-css')

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
        author = request.form['nickname']
        pastas = load_data()
        
        if text.strip() != '':
            pasta_id = len(pastas) + 1
            pastas[pasta_id] = {
                'author': author.strip() if author.strip() != '' else '--- не указано ---',
                'text': text,
                'file_path': None  # По умолчанию нет файла
            }
            
            # Сохранение файла, если он был загружен
            if 'file' in request.files:
                uploaded_file = request.form['file']
                if uploaded_file:
                    file_path = 'G:/pasteFy/uploads/' + uploaded_file.filename
                    uploaded_file.save(file_path)
                    pastas[pasta_id]['file_path'] = file_path  # Устанавливаем путь к файлу

                save_data(pastas)
            else: return "ошибка с файлом!!"
        else:
            return 'Похоже, вы создали пустой паст. Пустые пасты не сохраняются. <a href="/">Назад</a>'

        return f"Ваша паста создана! <a href='/paste/{pasta_id}'>Посмотреть паст</a>"

    return render_template('index.html')

@app.route('/paste/<pasta_id>')
def view_paste(pasta_id):
    try:
        pastas = load_data()
        author = pastas.get(pasta_id).get('author')
        pasta = pastas.get(pasta_id).get('text')
        if pasta is not None:
            return render_template('view_paste.html', pasta=pasta, author=author.capitalize())
    except:
        return render_template('404.html')

@app.errorhandler(404)
def err(e):
    return render_template('ab.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
