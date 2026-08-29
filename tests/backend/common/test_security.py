import bcrypt

from common import security

def test_secure_creds():
    credentials = "testname", "testpwd"

    sec_credentials = security.secure_creds(credentials)

    username_match = credentials[0] == sec_credentials[0]
    pwd_hashed = bcrypt.checkpw(credentials[1].encode("utf-8"), sec_credentials[1].encode("utf-8"))

    assert username_match and pwd_hashed


def test_secure_creds_returns_str():
    credentials = "testname", "testpwd"

    sec_credentials = security.secure_creds(credentials)

    assert isinstance(sec_credentials[1], str)


def test_password_match():
    password = "testpwd"
    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    assert security.password_match(password, hashed_pwd)


def test_password_nomatch():
    password = "testpwd"
    wrongpwd = "notcorrect"
    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    assert not security.password_match(wrongpwd, hashed_pwd)