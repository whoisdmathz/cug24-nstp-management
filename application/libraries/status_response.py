import datetime

def status_response(code, message=None, name=None):
    names = {
        0: name, 
        200: "OK", 
        400: "BAD REQUEST", 
        401: "UNAUTHORIZED", 
        403: "FORBIDDEN", 
        404: "NOT FOUND", 
        409: "CONFLICT", 
        500: "INTERNAL SERVER ERROR" 
    }
    messages = {
        0: message, 
        200: "", 
        400: "Invalid request parameters.", 
        401: "Authentication credentials were missing or invalid.", 
        403: "You do not have permission to access this resource.", 
        404: "The requested resource could not be found.", 
        409: "Record already exist.", 
        500: "An unexpected error occurred." 
    }
    return {
        "status": code,
        "name": name if name is not None else names[code],
        "message": message if message else messages[code],
        "timestamp": datetime.datetime.now().isoformat() + 'Z'
    }