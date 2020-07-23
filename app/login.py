# Config the login manager
login_manager = LoginManager()
login_manager.init_app(app)


# ==============================================================================
# Build login callback
# ==============================================================================

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# ------------------------------------------------------------------------------
login_manager.login_view = 'login'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():

        username = form.data.get('username', 'guest')
        password = form.data.get('password', '')
        user = User.objects(name=username,
                            password=password).first()

        print(user)
        if user:
            # login_user(user)
            # return jsonify(user.to_json())
            return flask.redirect(next or flask.url_for('index'))
    else:
        return flask.render_template('login.html', form=form)


    #
    #     # Login and validate the user.
    #     # user should be an instance of your `User` class
    #     # login_user(user)
    #
    #     flash('Logged in successfully.')
    #
    #     next = flask.request.args.get('next')
    #     # is_safe_url should check if the url is safe for redirects.
    #     # See http://flask.pocoo.org/snippets/62/ for an example.
    #     # if not is_safe_url(next):
    #     #     return abort(400)
    #
    #


#
# @app.route("/settings")
# @login_required
# def settings():
#     pass
#
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(somewhere)
