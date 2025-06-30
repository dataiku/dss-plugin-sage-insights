def get(t):
    if t == "metric":
        data = {
            "pass": True, "title": None, "type": "metric",
            "label": None, "data": None,"delta": None,
        }
    elif t == "bar_chart":
        data = {
            "pass": True, "title": None, "type": "bar_chart",
            "data": None, "x": None, "x_label": None, "y": None, "y_label": None,
            "horizontal": False, "stack": False
        }
    else:
        data = {}
    return data