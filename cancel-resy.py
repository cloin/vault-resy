import os
import hvac
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Release a reserved user in Vault.')
parser.add_argument('--id', type=str, help='Unique ID for the host releasing the user', required=True)
args = parser.parse_args()

# Initialize the Vault client
client = hvac.Client(
    url=os.getenv('VAULT_URL'),  # export VAULT_URL=https://vault.example.com
    token=os.getenv('VAULT_TOKEN')  # export VAULT_TOKEN=secret
)

def release_reserved_user(base_path='saasuser', host_id=None, user_count=1): # Todo: handle user_count better
    """
    Release a user reserved by the specified host ID.

    :param base_path: The base path where user secrets are stored in Vault.
    :param host_id: Unique ID for the host, used to find the reserved user.
    :param user_count: The total number of user secrets to iterate through.
    :return: Details of the released user or None if no matching user is found.
    """
    for i in range(1, user_count + 1):
        user_path = f"{base_path}{i}"  # Construct the path for each user secret
        
        # Attempt to read the user's secret
        read_response = client.secrets.kv.v2.read_secret_version(path=user_path, raise_on_deleted_version=True)
        user_data = read_response['data']['data']

        # Check if the user is reserved by this host
        if host_id and user_data.get('id') == host_id:
            # Mark the user as unreserved and remove the host ID
            user_data['reserved'] = "false"
            user_data.pop('id', None)  # Remove the id key if it exists

            # Update the secret with the new status
            client.secrets.kv.v2.create_or_update_secret(path=user_path, secret=user_data)

            # Return the released user's details
            return {
                "username": user_data['username'],
                "path": user_path
            }

    # Return None if no matching reserved user is found
    return None

# Example usage
host_id = args.id  # Unique ID passed as an argument
released_user = release_reserved_user(host_id=host_id)
if released_user:
    print("Released user:", released_user)
else:
    print("No reserved user found with the specified ID.")
