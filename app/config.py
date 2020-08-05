class BaseConfig(object):
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = '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'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    SECRET_KEY = 'my_precious'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    MAIL_DEFAULT_SENDER = 'dr49@njit.edu'