def button_layout(url:str, classname='', label='', icon='', onclick=False):
    if onclick:
        button_layout = {
            'classname': classname,
            'label': label,
            'icon': icon,
            'onclick': url
        }
    else:
        button_layout = {
            'classname': classname,
            'label': label,
            'icon': icon,
            'url': url
        }

    return button_layout