# makeshift test code for obj2

from obj2_weather import Weather

EXPECTED_DEFAULT_QUERIES = [
    '',
    'hey',
    'weather',
    'weather rain',
    'weather singapore',
    'singapore weather',
    'weather in singapore',
    'the weather in singapore',
    "singapore's weather",
    'singapore weather?',
    'weather in singapore?',
    'what is the temperature like in singapore!',
    'i hear the weather in cairo is hot',
    'i am studying at nus in singapore'
]

EXPECTED_SINGAPORE_QUERIES = [
    'is it going to be a rainy day in singapore',
    "how's the weather in singapore",
    'please tell me about the singapore weather',
    'what is the temperature like in singapore?',
    'is the singapore weather as hot as cairo or as rainy as london?'
]

w = Weather('')
fail = False

for x in EXPECTED_DEFAULT_QUERIES:
    if w.weather(x) != Weather.DEFAULT:
        print(x)
        print(w.weather(x))
        fail = True

for x in EXPECTED_SINGAPORE_QUERIES:
    if w.weather(x) != Weather.SINGAPORE_WEATHER:
        print(x)
        print(w.weather(x))
        fail = True

if not fail:
    print('nice')