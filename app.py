from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from matplotlib.colors import PowerNorm

app = Flask(__name__)

def compute_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    C = Z.copy()
    escaped = np.zeros(Z.shape, bool)
    iteration = np.zeros(Z.shape, int)

    for i in range(max_iter):
        # Suppress the ComplexWarning here
        with np.errstate(all='ignore'):
            Z[~escaped] = Z[~escaped] ** 2 + C[~escaped]
        escaped |= np.abs(Z) > 2
        iteration[escaped & (iteration == 0)] = i
    return iteration.swapaxes(1,0)

def plot_mandelbrot(xmin, xmax, ymin, ymax, width=800, height=600, max_iter=256):
    mandelbrot_set = compute_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter)
    
    fig, ax = plt.subplots()
    
    # Normalization and colormap
    norm = PowerNorm(0.3)  # Adjust the exponent to control color scaling
    cmap = plt.cm.viridis  # You can experiment with different colormaps

    ax.imshow(mandelbrot_set, extent=[xmin, xmax, ymin, ymax], cmap=cmap, norm=norm)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('ascii')
    buf.close()

    return image_base64

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
