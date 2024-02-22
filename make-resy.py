import os
import hvac
import argparse
import logging
from hvac.exceptions import VaultError

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up argument parsing
parser = argparse.ArgumentParser(description='Reserve a user from Vault.')
parser.add_argument('--id', type=str, help='Unique ID for the host running the script')
parser.add_argument('--user-count', type=int, default=1, help='Total number of user secrets to iterate through')
parser.add_argument('--base-path', type=str, default='saasuser', help='Base path where user secrets are stored in Vault')
args = parser.parse_args()

# Initialize the Vault clients
try:
    client = hvac.Client(
        url=os.getenv('VAULT_URL'),  # export VAULT_URL=http://host.containers.internal:8200
        token=os.getenv('VAULT_TOKEN')  # export VAULT_TOKEN=secret
    )
    # Verify if the client is authenticated
    if not client.is_authenticated():
        logging.error('Vault Authentication Failed. Check your VAULT_TOKEN.')
        exit(1)
except Exception as e:
    logging.error(f'Error initializing Vault Client: {e}')
    exit(1)

def find_and_reserve_user(base_path, host_id, user_count):
    for i in range(1, user_count + 1):
        user_path = f"{base_path}{i}"
        try:
            read_response = client.secrets.kv.v2.read_secret_version(path=user_path, raise_on_deleted_version=True)
            user_data = read_response['data']['data']

            if user_data.get('reserved') == "false":
                user_data['reserved'] = "true"
                user_data['id'] = host_id

                client.secrets.kv.v2.create_or_update_secret(path=user_path, secret=user_data)
                logging.info(f"User {user_path} reserved successfully.")
                return user_data

        except VaultError as e:
            logging.error(f"Vault Error: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    logging.info("No unreserved user found.")
    return None

reserved_user = find_and_reserve_user(args.base_path, args.id, args.user_count)
if reserved_user:
    logging.info(f"Reserved user: {reserved_user}")
else:
    logging.info("No unreserved user found.")
