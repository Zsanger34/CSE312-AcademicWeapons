from app import create_app
from time import time
from flask import Flask, request, jsonify
app = create_app()
LIMIT = 50 
PERIOD = 10      
BLOCKTIME = 30

#will store as BLOCKEDIPS[ip] = block Time
BLOCKEDIPS = {}
REQUESTCOUNTS = {}


@app.before_request
def ddosProtection():
    ipAddress = request.remote_addr
    currentTime = time()

    if ipAddress in BLOCKEDIPS:
        blockTime = BLOCKEDIPS[ipAddress]
        if currentTime < blockTime:
            #send a 429 request saying they are blocked
            return jsonify({"error": "too many requests you are now banned"}), 429
        else:
            del BLOCKEDIPS[ipAddress]

    
    #delete any old request counts
    if ipAddress in REQUESTCOUNTS:
        currentTime = time()
        requestsKeep = []
        for requestTime in REQUESTCOUNTS[ipAddress]:
            if currentTime - requestTime < PERIOD:
                requestsKeep.append(requestTime)
        
        REQUESTCOUNTS[ipAddress] = requestsKeep




    if ipAddress not in REQUESTCOUNTS:
        REQUESTCOUNTS[ipAddress] = []

    REQUESTCOUNTS[ipAddress].append(currentTime)

    if len(REQUESTCOUNTS[ipAddress]) > LIMIT:
        #too many requests, ban the ip for 30 seconds
        banTime = currentTime + BLOCKTIME
        BLOCKEDIPS[ipAddress] = banTime
        return jsonify({"error": "too many requests you are now banned"}), 429



    

@app.after_request
def nosniffSecurity(response):
    """
    This will add the noSniff header to all response right before it gets sent
    """
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
