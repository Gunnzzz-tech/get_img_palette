from flask import Flask, render_template, request
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for Matplotlib
import matplotlib.pyplot as plt
from PIL import Image

from werkzeug.utils import secure_filename
import os
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='static'
app.config['ALLOWED_EXTENSIONS']={'png','jpg','jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_palette(img_path,num_color=5):
    image = Image.open(img_path).convert('RGB')
    image = image.resize((100,100))
    pixels = list(image.getdata())
    from collections import Counter
    color_counts=Counter(pixels)
    most_common=color_counts.most_common(num_color)
    palette=[color for color,_ in most_common]
    return palette

@app.route('/',methods=["GET","POST"])
def index():
    if request.method=="POST":
        if 'file' not in request.files:
            return "no file part"
        file=request.files['file']
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(file_path)

            palette=generate_palette(file_path)
            palette_img_path=os.path.join(app.config['UPLOAD_FOLDER'],'palette.png')
            fig, ax = plt.subplots(figsize=(5, 2))
            for i,color in enumerate(palette):
                ax.add_patch(plt.Rectangle((i,0),1,1,color=[c/255 for c in color]))
            ax.set_xlim(0,len(palette))
            ax.set_ylim(0, 1)
            ax.axis('off')
            plt.savefig(palette_img_path, bbox_inches='tight')
            plt.close(fig)
        return render_template('index.html', uploaded_image=filename, palette_image='palette.png')
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)