import requests
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://app:8000/api"  

def generate_user():
    return {
        "email": f"user{random.randint(1, 10000)}@example.com",
        "is_active": True
    }

def create_user():
    user_data = generate_user()
    try:
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        response.raise_for_status()
        logging.info(f"Created user: {response.json()['email']}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create user: {e}")
        logging.error(f"Response content: {response.text}")
        return None


def create_users(num_users=10):
    created_users = []
    for _ in range(num_users):
        user_data = {
            "email": f"user{random.randint(1000, 9999)}@example.com",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 200:
            created_user = response.json()
            created_users.append(created_user)
            logger.info(f"Created user: {created_user['email']}")
        else:
            logger.error(f"Failed to create user: {response.status_code} {response.text}")
    logger.info(f"Created {len(created_users)} users")
    return created_users


def main():
    logger.info("Starting test data generation")
    users = create_users()
    logger.info("Test data generation completed")

if __name__ == "__main__":
    main()
