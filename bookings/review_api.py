import requests
import time
from django.conf import settings

class ReviewAPI:
    """Helper class for interacting with the Reviews API"""
    
    BASE_URL = "https://wxqzannoi7.execute-api.us-east-1.amazonaws.com/dev"
    
    @staticmethod
    def generate_review_token(review_data, max_retries=2):
        """
        Generate a review token with sentiment analysis
        
        Args:
            review_data (dict): The review data to analyze
            max_retries (int): Maximum number of retries on failure
            
        Returns:
            tuple: (success, result_or_error_message)
        """
        endpoint = f"{ReviewAPI.BASE_URL}/generate-review-token"
        headers = {'Content-Type': 'application/json'}
        
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(endpoint, json=review_data, headers=headers)
                
                if response.ok:
                    result = response.json()
                    # Handle the new response structure
                    if result.get('message') == 'Token generated successfully' and result.get('data'):
                        return True, result.get('data')
                    return True, result
                elif response.status_code >= 500:  # Server error
                    if attempt < max_retries:
                        # Exponential backoff
                        time.sleep(1 * (2 ** attempt))
                        continue
                    else:
                        return False, f"API Service unavailable after {max_retries} retries."
                else:
                    return False, f"API Error: {response.status_code} - {response.text}"
                    
            except requests.RequestException as e:
                if attempt < max_retries:
                    time.sleep(1 * (2 ** attempt))
                    continue
                return False, f"Connection error: {str(e)}"
        
        return False, "Failed to reach the sentiment analysis service."
    
    @staticmethod
    def verify_review_token(token):
        """
        Verify a review token
        
        Args:
            token (str): The review token to verify
            
        Returns:
            tuple: (success, result_or_error_message)
        """
        endpoint = f"{ReviewAPI.BASE_URL}/generate-review-token/verify"
        headers = {'Content-Type': 'application/json'}
        data = {"token": token}
        
        try:
            response = requests.post(endpoint, json=data, headers=headers)
            
            if response.ok:
                return True, response.json()
            else:
                return False, f"Verification failed: {response.status_code} - {response.text}"
                
        except requests.RequestException as e:
            return False, f"Connection error: {str(e)}"