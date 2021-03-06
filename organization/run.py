import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from organization.app import app

if __name__ == '__main__':

    deploy_mode = str(sys.argv[1])

    if deploy_mode == 'debug' or deploy_mode == 'd':
        app.debug = True
        app.run(host='localhost', port=9899)

    elif deploy_mode == 'production' or deploy_mode == 'p':
        app.run(host='0.0.0.0', port=9899)

    else:
        print("Usage: python run.py <[d/debug]/[p/production]>")
