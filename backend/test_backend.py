import requests
import json

# Test the Flask backend
def test_health():
    try:
        response = requests.get('http://localhost:5000/api/health')
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_analyze_job():
    try:
        job_description = """
        Job Title: Digital Marketing Specialist
        
        We are seeking a creative and analytical Digital Marketing Specialist to execute 
        and optimize our online marketing strategies. You will be responsible for managing 
        our social media presence, executing email campaigns, and driving traffic through 
        SEO and paid channels.
        
        Key Responsibilities:
        - Plan and implement digital marketing campaigns, including SEO, PPC, email, and social media
        - Analyze campaign performance using tools like Google Analytics
        - Manage content calendars and coordinate with designers and copywriters
        - Conduct keyword research and optimize website content for search engines
        - Set up and manage Google Ads and Facebook Ads campaigns
        
        Qualifications:
        - Bachelor's degree in Marketing, Business, or related field
        - 2-4 years of experience in digital marketing
        - Strong knowledge of SEO/SEM, Google Ads, and social media platforms
        - Hands-on experience with tools like Google Analytics, Mailchimp, and HubSpot
        - Excellent written and verbal communication skills
        """
        
        data = {
            "job_description": job_description,
            "resume_folder": "uploads",
            "top_n": 5
        }
        
        response = requests.post('http://localhost:5000/api/analyze-job', 
                               json=data, 
                               headers={'Content-Type': 'application/json'})
        
        print(f"Analyze job: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success', False)}")
            if result.get('success'):
                print(f"Total processed: {result.get('total_processed', 0)}")
                print(f"Top candidates count: {len(result.get('top_candidates', []))}")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    print("Testing Flask Backend...")
    print("=" * 50)
    
    if test_health():
        print("✅ Health check passed")
        test_analyze_job()
    else:
        print("❌ Health check failed - make sure the server is running") 