from flask import Flask, render_template, url_for, flash, redirect, request
from flask_mail import Mail, Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from forms import RequestResetForm, ResetPasswordForm
from models import User, db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
mail = Mail(app)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Redefinir Senha',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''Para redefinir sua senha, clique no seguinte link:
{url_for('reset_token', token=token, _external=True)}

Se você não solicitou esta alteração, por favor, ignore este email.
'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('Um email foi enviado com instruções para redefinir sua senha.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token inválido ou expirado', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data  # Aqui você deve hashear a senha antes de salvar
        db.session.commit()
        flash('Sua senha foi atualizada! Você já pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)
