import os


ssh_user = os.environ["SSH_USER"]
ssh_server = os.environ["SSH_SERVER"]
ssh_password = os.environ["SSH_PASSWORD"]

DATABASE = {
	"db_host": os.environ["DB_HOST"],
	"db_name": os.environ["DB_NAME"],
	"db_user": os.environ["DB_USER"]
}

AZURE_ACCOUNT_NAME = os.environ["AZURE_ACCOUNT_NAME"]
AZURE_ACCOUNT_KEY = os.environ["AZURE_ACCOUNT_KEY"]
AZURE_CONTAINER_NAME = "dbbackups"
