from camunda import settings

SIGNED_IN = 'Sign in'
PASSWORD_CHANGED = 'Password changed'
USER_DETAILS_CHANGED = 'User details changed'
ACCOUNT_EXIST = 'Account exists'
PASSWORDS_NOT_SAME = 'Passwords don\'t match'
WRONG_PASSWORD = 'Wrong password'
EMAIL_DOESNT_EXIST = 'Email does not exist'
INVALID_RESET_LINK = 'Invalid reset password link'
ALREADY_EXIST = 'Email already exist'
INVALID_ACTIVATION_LINK = 'Invalid activation link'
NO_CREDENTIALS = 'Enter credentials'
WRONG_EMAIL_OR_PASSWORD = 'Wrong email or password'
EARLY_ATTEMPT = 'Resent password link was sent recently. Wait {0} minutes'.format(settings.WAITING_TIME_ATTEMPTS_MIN)
