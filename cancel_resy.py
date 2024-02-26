import os
import hvac
import argparse
import logging
from hvac.exceptions import VaultError

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Release a reserved user in Vault.')
parser.add_argument('--id', type=str, help='Unique ID for the host releasing the user', required=True)
parser.add_argument('--user-count', type=int, default=100, help='Total number of user secrets to iterate through')
parser.add_argument('--base-path', type=str, default='saasuser', help='Base path where user secrets are stored in Vault')
args = parser.parse_args()

# Initialize the Vault client
try:
    client = hvac.Client(
        url=os.getenv('VAULT_URL'),  # export VAULT_URL=http://host.containers.local:8200
        token=os.getenv('VAULT_TOKEN')  # export VAULT_TOKEN=secret
    )
    if not client.is_authenticated():
        logging.error('Vault Authentication Failed. Check your VAULT_TOKEN.')
        exit(1)
except Exception as e:
    logging.error(f'Error initializing Vault Client: {e}')
    exit(1)

def release_reserved_user(base_path, host_id, user_count):
    for i in range(1, user_count + 1):
        user_path = f"{base_path}{i}"
        try:
            read_response = client.secrets.kv.v2.read_secret_version(path=user_path, raise_on_deleted_version=True)
            user_data = read_response['data']['data']

            if host_id and user_data.get('id') == host_id:
                user_data['reserved'] = "false"
                user_data.pop('id', None)  # Remove the id key if it exists

                client.secrets.kv.v2.create_or_update_secret(path=user_path, secret=user_data)
                logging.info(f"User {user_path} reservation released successfully.")
                return {"username": user_data['username'], "path": user_path}

        except VaultError as e:
            logging.error(f"Vault Error: {e}")
        except Exception as e:
            logging.error(f"An error occurred while processing {user_path}: {e}")

    logging.info("No reserved user found with the specified ID.")
    return None

released_user = release_reserved_user(args.base_path, args.id, args.user_count)
if released_user:
    logging.info(f"Released user: {released_user}")
else:
    logging.info("No reserved user found with the specified ID.")
