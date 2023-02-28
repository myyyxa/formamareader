from app import app
import telegram
from flask import render_template, request,flash,redirect,url_for
from app.forms import LoginForm
from config import Config

bot = telegram.Bot(token=Config.BOT_TOKEN)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'anton))'}
    return render_template('index.html', title='Home', user=user)

@app.route('/message', methods=['POST'])
def message():
    message = request.form['message']
    return render_template('index.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/{}'.format(bot.token), methods=['POST'])
def telegram_webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    message_text = update.message.text
    request.post('http://localhost:5000/message', data={'message': message_text})
    return 'ok'