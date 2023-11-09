from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

def compute_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    C = X + 1j * Y
    not_diverged = np.ones_like(C, bool)
    for i in range(max_iter):
        Z[not_diverged] = Z[not_diverged] ** 2 + C[not_diverged]
        not_diverged &= np.abs(Z) < 2
    return not_diverged

def plot_mandelbrot(xmin, xmax, ymin, ymax, width=800, height=600, max_iter=256):
    escape = compute_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter)
    plt.imshow(escape.T, extent=[xmin, xmax, ymin, ymax], cmap='hot', origin='lower')
    plt.axis('off')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

@app.route('/')
def home():
    return render_template('mandelbrot.html')

@app.route('/plot', methods=['POST'])
def plot():
    data = request.json
    xmin, xmax, ymin, ymax = data['xmin'], data['xmax'], data['ymin'], data['ymax']
    image_data = plot_mandelbrot(xmin, xmax, ymin, ymax)
    return jsonify({'image_data': image_data})

if __name__ == '__main__':
    app.run(debug=False)
