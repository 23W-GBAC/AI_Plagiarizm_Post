from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from models import db, Artwork, Comment
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artwork.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB upload limit
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        title = request.form['title']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            artwork = Artwork(title=title, image_filename=filename)
            db.session.add(artwork)
            db.session.commit()
            return redirect(url_for('home'))
    artworks = Artwork.query.all()
    return render_template('home.html', artworks=artworks)

@app.route('/artwork/<int:artwork_id>', methods=['GET', 'POST'])
def artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    if request.method == 'POST':
        content = request.form['content']
        comment = Comment(content=content, artwork_id=artwork_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('artwork', artwork_id=artwork_id))
    return render_template('artwork.html', artwork=artwork)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
