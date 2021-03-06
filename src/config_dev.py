import os

# dialect+driver://username:password@host:port/database
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.abspath("breul.db")
SQLALCHEMY_ECHO = False
# Evil as errors during .commit() don't get caught.
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# Used for secure sessions. Must be kept secret in production.
SECRET_KEY = "OMGORLYDEADBEEF"
SIGNATURE_MAX_AGE = 60*60*24*7  # 7 days

# Flask Debug Mode
DEBUG = True

BASIC_AUTH_FORCE = False
BASIC_AUTH_REALM = "Formmanagement"
BASIC_AUTH_USERNAME = "breul"
BASIC_AUTH_PASSWORD = "1234"

## File Uploads
# File Upload Folder.
UPLOAD_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 "uploads/"))
# Maximum upload size: 50 megabytes
# needs to be adjusted at web/components/bankbook/common/common.js -> <file-input> as well.

## SSL Settings
#SSL_KEYFILE = ""
#SSL_CERTFILE = ""
#SSL_CIPHERS = ""

# Host and Port to bind on.
# "" binds on all hosts.
