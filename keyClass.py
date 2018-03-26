#Class of key objects, holds key and iv for each password

class keyIV:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        
    #Don't need to mutate this data
    def get_key(self):
        return self.key
    def get_iv(self):
        return self.iv