import os 
WELCOME = {"fr" : "jraulouvre/index.html", # used to be welcome.html,
    "en": "jraulouvre/index_en.html"}


KEY_REDIS_WELCOME= {
        'fr':  {'page' : 'welcome', 'language':'fr'},
        'en':  {'page' : 'welcome', 'language':'en'}
}



REGISTER = {
    'fr': "jraulouvre/register.html",    #used to be register.html 
    'en': "jraulouvre/register_en.html" #used to be register.html 
}

KEY_REDIS_SHIFTS = {'shifts' : 'currentStatus'}


UNREGISTER = {
    'fr':  "jraulouvre/unregister_fr.html",
    'en' : "jraulouvre/unregister_en.html"
}


UNREGISTER_SUCCESS={
    "fr" : "jraulouvre/unregister_thanks_fr.html",
    "en": "jraulouvre/unregister_thanks_en.html"
}


ERROR_PAGE="jraulouvre/error.html"
THANKS="jraulouvre/register_thanks.html"
ACCEPT_REGISTRATION=os.getenv("ACCEPT_REGISTRATION", "True")
ADMIN="jraulouvre/cestquilpatron.html"


### ERROR MESSAGES
ERROR_UNREGISTER={ 
    'en' : 'Incorrect configuration received.',
    'fr' : 'Configuration incorrecte.'
}

ERROR_GENERIC={
    "en":"An error occured, please try again later.",
    "fr":"Une erreur est survenue, merci de renouveller votre requête plus tard."
}
CODE_MISMATCH = {
     "en" :"Incorrect configuration. Can not proceed with unregister action. Please check code given by email.",
    "fr" : "Configuration incorrrecte, veuillez vérifier le code reçu par email."
}
EMAILS_MISMATCH={
    "fr":'Les emails ne correspondent pas, veuillez ressaisir.', 
    'en':'Emails entered do not match.'}
AGE_LIMIT={
    'fr':'Désolé, vous devez avoir au moins 18 ans pour participer à cet évènement.', 
    'en':'Sorry, you must be over 18 years old to participate to the event.'}    

SHIFT_FULL={
    'fr': "Cette session est désormais pleine, merci d'en choisir une autre.",
    'en':'This shift is now full, please select another one.'
}
REGISTRATION_CLOSED={
    "en" : "Registrations are closed: there is no more shift available. ",
    "fr" : "Les inscriptions sont suspendues: il n'y a plus de place disponible."
}
ALREADY_REGISTERED={
    "en":"You are already registered to a shift. Please cancel your registration first by clicking the link sent by email.",
    "fr": "Vous êtes déjà enregistré à une session. Veuillez d'abord annuler celle ci en cliquant sur le lien reçu par email."
}