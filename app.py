from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Ограничение размера файла 16 MB

# Допустимые расширения файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Словарь для хранения комментариев
comments = {}

# Функция для проверки допустимых расширений
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Главная страница
@app.route('/')
def index():
    photos = os.listdir(app.config['UPLOAD_FOLDER'])  # Получаем список файлов в папке uploads
    return render_template('index.html', photos=photos, comments=comments)

# Обработка загрузки файла
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        comments[filename] = []  # Добавляем пустой список для комментариев к новой фотографии
        return redirect(url_for('index'))
    return redirect(request.url)

# Маршрут для показа загруженных файлов
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Обработка добавления комментариев
@app.route('/comment/<filename>', methods=['POST'])
def add_comment(filename):
    comment = request.form['comment']
    if filename in comments:
        comments[filename].append(comment)  # Добавляем комментарий к соответствующему изображению
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
