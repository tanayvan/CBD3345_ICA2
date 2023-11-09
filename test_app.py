import unittest
from app import app, compute_mandelbrot, plot_mandelbrot
import numpy as np

class TestMandelbrotApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    # Your existing test methods go here...
    # test_compute_mandelbrot(...)
    # test_plot_mandelbrot(...)
    # test_home_route(...)
    # test_plot_route(...)

    # ... Your test code continues ...

if __name__ == '__main__':
    unittest.main()
