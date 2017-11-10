#!/usr/bin/python

from app import app
import sys

if __name__ == '__main__':

    deploy_mode = str(sys.argv[1])
    port = int(sys.argv[2])

    if deploy_mode == 'debug':
        app.debug = True
        app.run(host='localhost', port=port)

    elif deploy_mode == 'production':
        app.run(host='0.0.0.0', port=port)

    else:
        print("Usage: python run.py <debug/production>")