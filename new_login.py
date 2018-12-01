from robobrowser import RoboBrowser

browser = RoboBrowser()
browser.open('https://login.utexas.edu/login/UI/Login')

# Get the signup form
signup_form = browser.get_form(name_='Login')
print(signup_form)         # <RoboForm user[name]=, user[email]=, ...

# Inspect its values
signup_form['authenticity_token'].value     # 6d03597 ...

# Fill it out
signup_form['user[name]'].value = 'python-robot'
signup_form['user[user_password]'].value = 'secret'

# Submit the form
browser.submit_form(signup_form)
