import unittest
from app import app, compute_mandelbrot, plot_mandelbrot
import numpy as np

class TestMandelbrotApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_compute_mandelbrot(self):
            # Test the computation of the Mandelbrot set
            width, height = 800, 600
            result = compute_mandelbrot(-2.0, 1.0, -1.5, 1.5, width, height, 20)
            # expecting result.shape to be (width, height)
            self.assertEqual(result.shape, (width, height))
            self.assertIn(False, result)  # There should be some points that do not belong to the set
            self.assertIn(True, result)  # There should be some points that do belong to the set
        
    def test_plot_mandelbrot(self):
        # Test the plotting of the Mandelbrot set
        image_data = plot_mandelbrot(-2.0, 1.0, -1.5, 1.5)
        self.assertTrue(isinstance(image_data, str))
        self.assertTrue(image_data.startswith('iVBOR'))  # PNG image data starts with 'iVBOR'

    def test_home_route(self):
        # Test the home route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    def test_plot_route(self):
        # Test the plot route
        response = self.app.post('/plot', json={
            'xmin': -2.0, 'xmax': 1.0, 'ymin': -1.5, 'ymax': 1.5
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        data = response.get_json()
        self.assertIn('image_data', data)

if __name__ == '__main__':
    unittest.main()
