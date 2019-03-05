import os 
WELCOME = "jraulouvre/index.html" # used to be welcome.html
WELCOME_EN = "jraulouvre/index_en.html" # used to be welcome.html
KEY_REDIS_WELCOME = {'page' : 'welcome', 'language':'fr'}
KEY_REDIS_WELCOME_EN = {'page' : 'welcome', 'language':'en'}

REGISTER = "jraulouvre/register.html" #used to be register.html 
KEY_REDIS_SHIFTS = {'shifts' : 'currentStatus'}


UNREGISTER = "jraulouvre/unregister_fr.html"
UNREGISTER_EN = "jraulouvre/unregister_en.html"
UNREGISTER_SUCCESS="jraulouvre/unregister_thanks_fr.html"
UNREGISTER_SUCCESS_EN="jraulouvre/unregister_thanks_en.html"


ERROR_PAGE="jraulouvre/error.html"
NO_MORE_SHIFT="jraulouvre/noshift.html"
THANKS="jraulouvre/register_thanks.html"
ACCEPT_REGISTRATION=os.getenv("ACCEPT_REGISTRATION", "True")
ADMIN="jraulouvre/cestquilpatron.html"