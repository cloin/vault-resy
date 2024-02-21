# Vault User Reservation System

This repository contains two Python scripts for managing user reservations in HashiCorp Vault: `make-resy.py` for reserving users and `cancel-resy.py` for releasing reservations.

## Introduction

The Vault User Reservation System is designed to automate the process of reserving and releasing user credentials stored in HashiCorp Vault. It's particularly useful in environments where temporary access to resources is managed through Vault, such as in sandbox or testing environments.

- `make-resy.py`: Reserves a user by marking it as reserved and assigning a unique host ID.
- `cancel-resy.py`: Releases a user reservation by clearing the host ID and marking the user as unreserved.

## Requirements

- Python 3.x
- `hvac` library (HashiCorp Vault API client for Python)
- Access to a HashiCorp Vault server
- Appropriate permissions to read and write secrets in Vault

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://your-repository-url.git
   ```

2. Navigate to the repository directory:

   ```bash
   cd path/to/repository
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### KV secrets engine

KV is used to define the secret and these scripts are expecting a secret to look like this:
```
{
  "password": "pass1",
  "reserved": "false",
  "username": "user1",
  "id": "host123"
}
```

### Setting Environment Variables

Before using the scripts, set the following environment variables:

- `VAULT_URL`: The URL of your Vault server (e.g., `http://vault.example.com:8200`).
- `VAULT_TOKEN`: Your Vault authentication token.

Example:

```bash
export VAULT_URL=http://vault.example.com:8200
export VAULT_TOKEN=s.yourVaultTokenHere
```

### Reserving a User

To reserve a user, run `make-resy.py` with the `--id` parameter specifying the unique host ID.

```bash
python make-resy.py --id your_unique_host_id
```

### Releasing a Reservation

To release a user reservation, run `cancel-resy.py` with the `--id` parameter specifying the unique host ID associated with the reservation.

```bash
python cancel-resy.py --id your_unique_host_id
```

## Contributing

Contributions to improve the scripts or documentation are welcome. Please follow the standard GitHub pull request process to submit your changes.

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/yourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push the branch (`git push origin feature/yourFeature`).
5. Create a new Pull Request.
