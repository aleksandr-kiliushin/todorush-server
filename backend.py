import configparser
import json
import jwt
from typing import Union
from fastapi import FastAPI, Request
from schema import User, VerificationCode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

env_config = configparser.ConfigParser()
env_config.read("./.env")

DB_URL = env_config.get("DEFAULT", "DB_URL", fallback=None)
AUTHORIZATION_TOKEN_SECRET = env_config.get("DEFAULT", "AUTHORIZATION_TOKEN_SECRET", fallback=None)

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


@app.get("/")
def read_root():
	return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
	return {"item_id": item_id, "q": q}


@app.post("/api/authorize")
async def authorize(request: Request):
	request_body = await request.body()
	body = json.loads(request_body.decode("utf-8"))

	session = Session()
	verification_code = session.query(VerificationCode).filter_by(value=body["verification_code"]).first()

	# TODO: if verification_code.expires_at < now(): throw error

	if verification_code:
		session.query(VerificationCode).filter(VerificationCode.user_id == verification_code.user_id).delete()

	session.commit()
	session.close()

	if verification_code:
		session.query(VerificationCode).filter(VerificationCode.user_id == verification_code.user_id).delete()
		authorization_token = jwt.encode({"user_id": 1}, AUTHORIZATION_TOKEN_SECRET, algorithm="HS256")
		return {"authorization_token": authorization_token}
	else:
		return {"error": "Invalid verification code"}


@app.get("/api/me")
def me(request: Request):
	authorization_token = request.headers.get('Authorization')

	try:
		decoded_data = jwt.decode(authorization_token, AUTHORIZATION_TOKEN_SECRET, algorithms=["HS256"])
	except:
		return {"error": "Invalid authorization token"}

	session = Session()
	user = session.query(User).filter_by(id=decoded_data["user_id"]).first()

	response_body = {"user_id": user.id}

	session.commit()
	session.close()

	if not user:
		return {"error": f"User with id {decoded_data['user_id']} not found"}

	return response_body