"""
This is the main entry point for the application.
"""

from formapp import create_app

app = create_app(testing=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
