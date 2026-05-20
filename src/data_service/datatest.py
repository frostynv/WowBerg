class DataEndPoint:
    "Hide these when we done with implementation" 
    client_id = "09c055d763e848a4a251dbd61ab0eefd"
    client_secret = "Dj9NAoMQaC8xm1yZJaRqiF4RYqUZ2OAT"
    url = ""
    
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = "https://api.marketdataapi.com/v1/quotes?symbols=AAPL,GOOGL,MSFT&access_key=" + self.client_id + "&secret_key=" + self.client_secret
        
    
    