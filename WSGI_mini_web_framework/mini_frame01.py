import time

def login():
    return "---login--- welcome hahah to our website .....tiem:%s" %time.ctime()
def register():
    return "---register--- welcome hahah to our website .....tiem:%s" %time.ctime()
def profile():
    return "---profile--- welcome hahah to our website .....tiem:%s" %time.ctime()

def application(file_name):
    if file_name=="/login.py":
        return login()
    elif file_name=="/register.py":
        return register()
    elif file_name=="/profile.py":
        return profile()
    else:
        return "not found your page..."