import requests

class APIClient:
    BASE_URL = "http://127.0.0.1:8000/api"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIClient, cls).__new__(cls)
            cls._instance.token = None
        return cls._instance

    def login(self, email, password):
        """Authenticate and store the token."""
        try:
            # Adjust endpoint if your Django auth setup is different (e.g., /api-token-auth/)
            # Based on previous analysis, it likely uses standard DRF Token auth or a custom view.
            # Assuming a standard 'login' or token endpoint exists.
            # We'll try a common pattern, and the user can debug if it fails.
            # Looking at previous file list, there was 'api' app. 
            response = requests.post(f"{self.BASE_URL}/login", json={
                "email": email,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                return True, "Login successful"
            else:
                return False, response.json().get("error", "Login failed")
        except Exception as e:
            return False, str(e)

    def get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers

    def get(self, endpoint, params=None):
        return requests.get(
            f"{self.BASE_URL}/{endpoint}", 
            headers=self.get_headers(), 
            params=params
        )

    def post(self, endpoint, data=None, files=None):
        # Files don't need Content-Type header (requests handles it)
        headers = self.get_headers()
        title_headers = headers.copy()
        if files:
            title_headers.pop("Content-Type", None)
            return requests.post(f"{self.BASE_URL}/{endpoint}", headers=title_headers, data=data, files=files)
        
        return requests.post(f"{self.BASE_URL}/{endpoint}", json=data, headers=headers)

    def delete(self, endpoint):
        return requests.delete(f"{self.BASE_URL}/{endpoint}", headers=self.get_headers())
