import json

# Response Handler
def response(res={}, success = True, code = 200):
    if success: return json.dumps(res), code
    return json.dumps({"error": res}), code


class Debug:

    count = 1

    def debug():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ " + str(Debug.count) + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        Debug.count += 1