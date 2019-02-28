import os 
WELCOME = "jraulouvre/index.html" # used to be welcome.html
KEY_REDIS_WELCOME = {'page' : 'welcome'}

REGISTER = "jraulouvre/subscribe.html" #used to be register.html 
KEY_REDIS_SHIFTS = {'shifts' : 'currentStatus'}


UNREGISTER = "jraulouvre/unregister.html"
UNREGISTER_SUCCESS="jraulouvre/unregister_thanks.html"
ERROR_PAGE="jraulouvre/error.html"
NO_MORE_SHIFT="jraulouvre/noshift.html"


THANKS="jraulouvre/register_thanks.html"
ACCEPT_REGISTRATION=os.getenv("ACCEPT_REGISTRATION", "True")

ADMIN="jraulouvre/cestquilpatron.html"