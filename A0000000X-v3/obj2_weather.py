'''
    NUS CS4248 Assignment 1 - Objective 2 (Weather)

    Class Weather for handling Objective 2



    Assumption:

    The assignment task states, "it’s also good for a bot to have some social skills. Weather is a 
    common subject for passing time." 
    
    We thus assume that the bot's purpose is to provide weather when asked for it in a
    conversational context. As such, queries like "^Singapore weather$", while acceptable on a
    search engine, will not be recognized by this bot. After all, if you said "^Singapore weather$"
    to a human, he/she would probably reply with confusion rather than the current weather.
'''
import re
class Weather:

    # Class Constants for responses.
    SINGAPORE_WEATHER = "Singapore: hot and humid."
    LONDON_WEATHER = "London: rainy and miserable."
    CAIRO_WEATHER = "Cairo: bone dry."
    DEFAULT = "Hmm. That’s nice."

    CITIES = ['singapore', 'london', 'cairo']
    CITIES_WEATHER = {
        'singapore': SINGAPORE_WEATHER,
        'london': LONDON_WEATHER,
        'cairo': CAIRO_WEATHER
    }
    WEATHER_WORDS = [
        'weather', 'rain', 'raining', 'rainy', 'cloud', 'clouds', 'cloudy', 'sunny', 'wind',
        'windy', 'storm', 'stormy', 'storms', 'humid', 'humidity', 'temperature', 'snow', 'snowing',
        'snowy', 'hot', 'cold', 'cool', 'warm', 'bright', 'dry', 'arid'
    ]

    # prof said someth about substituting path with text, but unsure.
    def __init__(self, path):
        with open(path, encoding='utf-8', errors='ignore') as f:
            self.text = f.read()


    '''
    This method exists in case the user makes a request for a city's weather, while also
    mentioning another city, e.g. "Is the Singapore weather as hot as Cairo?"
    '''
    def get_requested_city(self, text):
        possible_request_formats = [
            "{} in (?P<city_name>\w+)",
            "(?P<city_name>\w+)('s)? {}"
        ]
        possible_requests = []
        for weather_word in WEATHER_WORDS:
            for possible_request_format in possible_request_formats:
                possible_requests.append(
                    re.compile(
                        possible_request_format.format(weather_word)
                    )
                )
        for possible_request in possible_requests:
            match = re.search(possible_request, text, flags=re.IGNORECASE)
            if match:
                return match.groupdict()['city_name']
        
        return None
        
        
    def has_weather_word(self, text):
        return bool(re.search(
            '(' + '|'.join(WEATHER_WORDS) + ')',
            text,
            flags=re.IGNORECASE
        ))
    

    def starts_with_how_or_what(self, text):
        return (
            bool(re.search(r"^how( is|'s)", text, flags=re.IGNORECASE)) or
            bool(re.search(r"^what( is|'s)", text, flags=re.IGNORECASE))
        )


    def starts_with_is(self, text):
        return bool(re.search(r'^is', text, flags=re.IGNORECASE))

    '''
    We identify questions by the lack of periods or exclamation points at the ending.
    Rationale: most humans would also interpret "what's the singapore weather like" as a
    question, even though there's no question mark.
    '''
    def is_question(self, text):
        return bool(re.search(r'[^.!]\s*$'))


    def cities_mentioned(self, text):
        mentioned = []
        for city in CITIES:
            if re.search(city, text, flags=re.IGNORECASE):
                mentioned.append(city)
        return mentioned
    

    def is_request(self, text):
        request_words = ['tell', 'enlighten', 'inform', 'update', 'brief']
        before_request = [
            'please', 'could you', 'would you', 'could you please', 'would you please', 'you better'
        ]
        possible_requests = []
        for prefix in before_request:
            for request_word in request_words:
                possible_requests.append('^' + prefix + ' ' + request_word + ' me')
        for possible_request in possible_requests:
            if re.search(possible_request, text, flags=re.IGNORECASE):
                return True
        return False


    def weather(self,text):
        '''
        Decide whether the input is about the weather and
        respond appropriately
        '''
        if not self.has_weather_word(text):
            return DEFAULT

        mentioned = self.cities_mentioned(text)
        is_question = self.is_question(text)
        how_or_what = self.starts_with_how_or_what(text)
        is_request = self.is_request(text)
        
        if len(mentioned) == 0:
            return DEFAULT
        
        if (is_question and how_or_what) or is_request:
            if len(mentioned) == 1:
                return CITIES_WEATHER[mentioned[0]]
            else:
                requested_city = self.get_requested_city(text)
                if requested_city:
                    return CITIES_WEATHER[requested_city]
        
        return DEFAULT
        