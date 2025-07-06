import flask

def request_header(name, header_type='Bearer'):
    header = flask.request.headers.get(name)
    if header is not None and header_type == 'Bearer': header = header.replace('Bearer ', '') 
    return header

def request_form(name):
    return flask.request.form.get(name)

def request_arg(name):
    return flask.request.args.get(name)