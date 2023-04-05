from flask import Flask, render_template

application = Flask(__name__)


@application.route('/.well-known/pki-validation/8E9E843D385B681CBB094B7A12A88187.txt')
def file_downloads():
    try:
        return render_template('\n'.join(open('ssl_verify.txt', 'r').readlines()))
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    application.run('localhost', port=5050, debug=True)
