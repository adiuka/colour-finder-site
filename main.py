from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import os
from werkzeug.utils import secure_filename
from color_extractor import get_top_colors
import glob

UPLOAD_FOLDER = "static/uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

Bootstrap5(app)


@app.route("/")
def render_home():
    """Renders the homepage of the website + deletes all images"""
    files = glob.glob(os.path.join(app.config["UPLOAD_FOLDER"], "*"))
    for file in files:
        os.remove(file)

    return render_template("index.html")


@app.route("/upload", methods=['POST'])
def upload_image():
    """Upload image path, will redirect to render_image_data"""
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == "":
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('render_image_data', filename=filename))
    

@app.route("/image/<filename>")
def render_image_data(filename):
    """Renders the image and RGB data from the uploaded image"""
    image_url = url_for('static', filename=f'uploads/{filename}')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    colors = get_top_colors(file_path)
    return render_template("image.html", image_url=image_url, colors=colors, filename=filename)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
