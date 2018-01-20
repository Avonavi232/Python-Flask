from flask import Flask, render_template, request, escape

from vsearch import search4letters

from DBcm import UseDatabase


app = Flask(__name__)

app.config['dbconf'] = {
        'host': '127.0.0.1',
        'user': 'vsearch',
        'password': 'vsearchpasswd',
        'database': 'vsearchlogDB'
    }


def log(req, res) -> None:
    with UseDatabase(app.config['dbconf']) as cursor:
        _SQL = """insert into log
              (phrase, letters, ip, browser_string, results)
              values
              (%s,%s,%s,%s,%s)"""
        cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, req.user_agent.browser, res))


@app.route('/search4', methods=['POST']) 
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    result = str(search4letters(phrase, letters))
    log(request, result)
    return render_template('results.html', the_title='Your result is:',  the_phrase=phrase, the_letters=letters, the_results=result)


@app.route('/')
@app.route('/entry')
def entry_page() -> str:
    return render_template('entry.html', the_title="Welcome to search4letters on the web")


@app.route('/showlog')
def show_log() -> 'html':

    with UseDatabase(app.config['dbconf']) as cursor:
        _SQL = """SELECT phrase, letters, ip, browser_string, results FROM log"""
        cursor.execute(_SQL)
        result = cursor.fetchall()

    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html', the_title='View Log', the_row_titles=titles, the_data=result)


app.run(debug=True)
