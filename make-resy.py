import os
import hvac
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Reserve a user from Vault.')
parser.add_argument('--id', type=str, help='Unique ID for the host running the script')
args = parser.parse_args()

# Initialize the Vault client
client = hvac.Client(
    url=os.getenv('VAULT_URL'),  # export VAULT_URL=https://vault.example.com
    token=os.getenv('VAULT_TOKEN')  # export VAULT_TOKEN=secret
)

def find_and_reserve_user(base_path='saasuser', host_id=None, user_count=1):
    """
    Find an unreserved user and mark it as reserved.

    :param base_path: The base path where user secrets are stored in Vault.
    :param host_id: Unique ID for the host, used to find a user reserved by this host.
    :param user_count: The total number of user secrets to iterate through.
    :return: The credentials of the reserved user or None if no unreserved user is found.
    """
    for i in range(1, user_count + 1):
        user_path = f"{base_path}{i}"  # Construct the path for each user secret
        
        # Attempt to read the user's secret
        read_response = client.secrets.kv.v2.read_secret_version(path=user_path, raise_on_deleted_version=True)
        user_data = read_response['data']['data']

        # Check if the user is reserved by this host or not reserved at all
        if user_data.get('reserved') == "false" or (host_id and user_data.get('id') == host_id):
            # Mark the user as reserved and update the host ID
            user_data['reserved'] = "true"
            if host_id:
                user_data['id'] = host_id

            # Update the secret with the new reserved status
            client.secrets.kv.v2.create_or_update_secret(path=user_path, secret=user_data)

            # Return the reserved user's details
            return {
                "username": user_data['username'],
                "password": user_data['password'],
                "id": user_data.get('id')
            }

    # Return None if no unreserved user is found
    return None

# Example usage
host_id = args.id  # Unique ID passed as an argument
reserved_user = find_and_reserve_user(host_id=host_id)
if reserved_user:
    print("Reserved user:", reserved_user)
else:
    print("No unreserved user found.")
