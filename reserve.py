import hvac

# Initialize the Vault client
client = hvac.Client(
    url='http://localhost:8200',  # Replace with your actual Vault server address
    token=''  # Replace with your actual Vault token
)

def find_and_reserve_user(base_path='secret/data/dynatraceuser', user_count=2):
    """
    Find an unreserved user and mark it as reserved.

    :param base_path: The base path where user secrets are stored in Vault.
    :param user_count: The total number of user secrets to iterate through.
    :return: The credentials of the reserved user or None if no unreserved user is found.
    """
    for i in range(1, user_count + 1):
        user_path = f"{base_path}{i}"  # Construct the path for each user secret
        
        # Attempt to read the user's secret
        read_response = client.secrets.kv.v2.read_secret_version(path=user_path)
        user_data = read_response['data']['data']

        # Check if the user is not reserved
        if user_data.get('reserved') == "false":
            # Mark the user as reserved
            user_data['reserved'] = "true"
            user_data['instruqt_sandbox_id'] = "some_unique_identifier"  # Optionally, set a unique identifier for the reservation

            # Update the secret with the new reserved status
            client.secrets.kv.v2.create_or_update_secret(path=user_path, secret=user_data)

            # Return the reserved user's details
            return {
                "username": user_data['username'],
                "password": user_data['password'],
                "instruqt_sandbox_id": user_data['instruqt_sandbox_id']
            }

    # Return None if no unreserved user is found
    return None

# Example usage
reserved_user = find_and_reserve_user()
if reserved_user:
    print("Reserved user:", reserved_user)
else:
    print("No unreserved user found.")
