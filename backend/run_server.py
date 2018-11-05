"""Used to run the Flask app"""
import logging

from app.api.app import app

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
