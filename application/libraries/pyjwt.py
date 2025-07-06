from flask import current_app

import jwt
import datetime

from application.services import db
from application.models.token import Token
from application.models.configuration import Configuration

def returns(message=None, code=401):
    return {
        'payload': "",
        'code': code if message is not None else 200,
        'message': message+"." if message is not None else '' 
    }

def token_generate(id, token_type):
    
    token_types = ['Refresh', 'Access']
    
    res = returns()
    if token_type in token_types:
        
        configuration = Configuration.query.with_entities(
            Configuration.value
        ).filter(Configuration.name==(token_type+" Token Duration")).first()
        
        if configuration is not None: 
            time = configuration.value
            payload = {
                'sub': id,
                'time': int(time),
                'iat': datetime.datetime.utcnow(),  # Issued at time
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(time)) # Token expiration time
            }
            token = jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
            res['payload'] = token
            
            # save token
            if token_type == 'Refresh': db_token_insert(token, payload)
        else:
            res = returns("Config not found", 404)
    else:
        res = returns("Invalid Type")
    
    return res

def token_check(token, isRefreshToken=0):
    if token:
        try:
            decoded_payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            
            if isRefreshToken:
                # check if token is active in database
                model_token = Token.query.filter(
                    Token.token==token,                                    
                    Token.status==1                                   
                ).first()
                
                # if still active
                if model_token is not None:
                    decoded_payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'], options={"verify_exp": False})
                    return token_generate(decoded_payload['sub'], 'Access')
                else:
                    return returns("Token does not exist", 404)
                
            # check if token is in database
            model_token = Token.query.filter_by(token=token).first()
            if model_token is not None: return returns("Invalid token", 401)
             
            ret = returns()
            ret['payload'] = decoded_payload['sub']
            return ret
        except jwt.ExpiredSignatureError:
            return returns("Token has expired", 401)
        except jwt.InvalidTokenError:
            return returns("Invalid token", 401)
    else:
        return returns("Token is missing", 401)

def db_token_insert(token, payload):
    model_token = Token(
        token           = token, 
        dateInserted    = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
        dateStarted     = payload['iat'].strftime('%Y-%m-%d %H:%M:%S'), 
        dateExpired     = payload['exp'].strftime('%Y-%m-%d %H:%M:%S'), 
        timeDuration    = payload['time'], 
        timeUsed        = 0, 
        status          = 1
    )
    db.session.add(model_token)
    db.session.commit()