REGEX_CONTINUE = "//a[contains(text(),'Continuar')]"

# Time between steps (interactions with forms): 0.5 seconds
STEP_TIME = 0.5

# Wait time between retries/checks for available dates: 10 minutes
RETRY_TIME = 10 * 60

# Wait time when an exception occurs: 30 minutes
EXCEPTION_TIME = 30 * 60

# Wait time when temporary banned (empty list): 60 minutes
COOLDOWN_TIME = 60 * 60
