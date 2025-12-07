"""
Test script for FastAPI API functionality
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    print(f"Health check response: {response.json()}")
    assert response.status_code == 200

def test_predict():
    # Generate 30 days of sample historical sales data
    historical_sales = [100 + i + (i % 7) * 10 for i in range(30)]
    test_data = {
        "category": "Furniture",
        "subcategory": "Chairs",
        "region": "East",
        "date": "2023-10-11",
        "discount": 0.1,
        "historical_sales": historical_sales
    }
    response = client.post("/predict", json=test_data)
    print(f"Prediction response: {response.json()}")
    assert response.status_code == 200

if __name__ == "__main__":
    print("Testing API endpoints...")
    try:
        test_health()
        test_predict()
        print("All tests passed!")
    except Exception as e:
        print(f"Error during testing: {str(e)}")