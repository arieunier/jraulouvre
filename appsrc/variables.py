import os 
WELCOME = "jraulouvre/welcome.html"
KEY_REDIS_WELCOME = {'page' : 'welcome'}

REGISTER = "jraulouvre/register.html"
KEY_REDIS_SHIFTS = {'shifts' : 'currentStatus'}

ERROR_PAGE="jraulouvre/error.html"
NO_MORE_SHIFT="jraulouvre/noshift.html"


THANKS="jraulouvre/thanks.html"
ACCEPT_REGISTRATION=os.getenv("ACCEPT_REGISTRATION", "True")