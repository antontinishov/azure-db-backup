import logging
import subprocess
from datetime import datetime

from azure.storage.blob import BlockBlobService

from config import *

logger = logging.getLogger(__name__)

try:
	blob_service = BlockBlobService(account_name=AZURE_ACCOUNT_NAME, account_key=AZURE_ACCOUNT_KEY)
except Exception as exc:
	logger.exception(exc)
	raise Exception


def make_dump() -> str:
	now_date = datetime.now().strftime("%d-%m-%Y.%H.%M")
	backup_dir_path = "{}/backup".format(os.getcwd())
	if not os.path.exists(backup_dir_path):
		os.mkdir(backup_dir_path)

	try:
		backup_file = "{backup_dir_path}/{db_name}_{now_date}.dump.gz".format(backup_dir_path=backup_dir_path,
		                                                                      db_name=DATABASE["db_name"],
		                                                                      now_date=now_date)

		pg_dump_command = "PGPASSWORD=$DB_PASSWORD pg_dump -U {db_user} -d {db_name} -h {db_host} | gzip > {backup_file}".format(
			db_user=DATABASE["db_user"],
			db_name=DATABASE["db_name"],
			db_host=DATABASE["db_host"],
			backup_file=backup_file
		)
		process = subprocess.Popen(pg_dump_command, stdout=subprocess.PIPE, shell=True)
		process.communicate()
		return backup_file
	except Exception as exc:
		logger.exception(exc)
		raise Exception


def upload_to_blob(filename: str) -> bool:
	if filename and os.path.exists(filename) and os.path.getsize(filename) > 0:
		blob_service.create_blob_from_path(
			container_name=AZURE_CONTAINER_NAME,
			blob_name=filename.split("/")[-1],
			file_path=filename
		)
		return True
	else:
		return False


def delete_local_file(filename) -> bool:
	try:
		os.remove(filename)
	except Exception as exc:
		logger.exception(exc)
	return True


def delete_old_blobs() -> bool:
	try:
		blobs = blob_service.list_blob_names(container_name=AZURE_CONTAINER_NAME)
		blobs = tuple(blobs)
		while len(blobs) > 10:
			blob_service.delete_blob(container_name=AZURE_CONTAINER_NAME, blob_name=blobs[0])
	except Exception as exc:
		logger.exception(exc)
	return True


if __name__ == "__main__":
	backup_file = make_dump()
	success_upload = upload_to_blob(filename=backup_file)
	if success_upload:
		delete_local_file(filename=backup_file)
	else:
		raise Exception
	delete_old_blobs()
