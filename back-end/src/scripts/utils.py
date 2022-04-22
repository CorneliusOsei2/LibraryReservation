import json

# Response Handler
def response(res={}, success = True, code = 200):
    if success: return json.dumps(res), code
    return json.dumps({"error": res}), code
