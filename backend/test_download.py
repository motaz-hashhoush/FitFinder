import requests
import os

def test_download_endpoints():
    """Test the download endpoints"""
    
    # First, make sure we have results files by running an analysis
    print("Testing download functionality...")
    print("=" * 50)
    
    # Test JSON download
    try:
        print("Testing JSON download...")
        response = requests.get('http://localhost:5000/api/download/json')
        
        if response.status_code == 200:
            # Save the file to verify it works
            with open('test_download.json', 'wb') as f:
                f.write(response.content)
            print("✅ JSON download successful")
            print(f"   File size: {len(response.content)} bytes")
            
            # Clean up test file
            if os.path.exists('test_download.json'):
                os.remove('test_download.json')
        else:
            print(f"❌ JSON download failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ JSON download error: {e}")
    
    # Test CSV download
    try:
        print("\nTesting CSV download...")
        response = requests.get('http://localhost:5000/api/download/csv')
        
        if response.status_code == 200:
            # Save the file to verify it works
            with open('test_download.csv', 'wb') as f:
                f.write(response.content)
            print("✅ CSV download successful")
            print(f"   File size: {len(response.content)} bytes")
            
            # Clean up test file
            if os.path.exists('test_download.csv'):
                os.remove('test_download.csv')
        else:
            print(f"❌ CSV download failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ CSV download error: {e}")
    
    # Test invalid file type
    try:
        print("\nTesting invalid file type...")
        response = requests.get('http://localhost:5000/api/download/invalid')
        
        if response.status_code == 400:
            print("✅ Invalid file type properly rejected")
        else:
            print(f"❌ Expected 400 error but got: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Invalid file type test error: {e}")

if __name__ == "__main__":
    test_download_endpoints() 