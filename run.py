import sys
from application import app

if __name__ == '__main__':
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug = True
    app.run('0.0.0.0', 3000, debug=debug)
