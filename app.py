from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file uploaded", 400

        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400

        try:
            input_image = Image.open(file.stream)
            output_image = remove(input_image)

            # Convert output image to bytes
            img_bytes = io.BytesIO()
            output_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)

            # Send file to client
            return send_file(
                img_bytes,
                mimetype='image/png',
                as_attachment=True,
                download_name='output.png'
            )
        except Exception as e:
            return f"Error removing background: {str(e)}", 500

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
