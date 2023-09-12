import random


def random_html_color():
    r = random.randint(0,256)
    g = random.randint(0,256)
    b = random.randint(0,256)
    return "#%02x%02x%02x" % (r, g, b)

def style_fcn(_):
    return { 
        "fillColor": random_html_color(),
        "weight" : 1,
        "fillOpacity" : 0.25,
        "color": "#32a852",
        "radius": "20px",
    }

def highlight_fcn(_):
    return {"fillColor": "#000000"}