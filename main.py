from flask import Flask, request, redirect, render_template
import cgi
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader
(template_dir),autoescape=True)

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

# 1.Add a header "Signup"
# 2.Add the following blocks: 'Username', 'Password', 'Verify Password'
#   Email (optional)
# 3.Add a 'Submit Query' button at the bottom

userlist= []

@app.route("/add", methods=['POST'])
def add_user():
    # look inside the request to figure out what the user typed
    new_user = request.form['usernm']
    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    new_user_escaped = cgi.escape(new_user, quote=True)

    password = request.form['password']
    verify =request.form['verify']
    email= request.form['email']

    user_error= ''
    password_error = ''
    verify_error= ''
    email_error= ''

    userlist.append(new_user)

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_user_escaped) or (new_user_escaped.strip() == "") or (len(new_user_escaped.strip()) < 4) or (len(new_user_escaped.strip()) > 20):
        user_error = "That's not a valid username" 
        #return redirect("/?error=" + user_error)

    if (not password) or (password.strip() == ""):
        password_error = "That's not a valid password"

    if verify != password:
        # if the verify password doesn't match original throw error
        # so we redirect back to the front page and tell them what went wrong
        verify_error = "Passwords don't match!"

        # redirect to homepage, and include error as a query parameter in the URL
        #return redirect("/?error=" + verify_error)

    if len(email) != -1 and (email.find(' ')> 1) or (email.find('@') == -1) or (email.find('@@')== 0) or (email.find('..') == 0):
            email_error= "That's not a valid email"
        #return redirect("/?error=" + email_error)


    if not user_error and not password_error and not verify_error and not email_error:
        return render_template('welcome_page.html', new_user=new_user_escaped, userlist=userlist)
    else:
        template = jinja_env.get_template('edit.html')
        return template.render(user_error=user_error, 
        password_error= password_error,
        verify_error=verify_error,
        email_error= email_error)
    
    
@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('edit.html',  
           error=encoded_error and cgi.escape(encoded_error, quote=True))
app.run()