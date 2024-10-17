from dataclasses import dataclass, field
import jwt
import os
import datetime

CMS_TOKEN = os.getenv("CMS_TOKEN", "")
TENANT_ID = os.getenv("TENANT_ID", "")
PROJECT_ID = os.getenv("PROJECT_ID", "")
CMS_API_KEY = os.getenv("CMS_API_KEY", "")
CMS_BASE_URL_TEMP = "https://{sub}.kantan-cms.com"


class ENVKey:
    TENANT_ID = "TENANT_ID"
    PROJECT_ID = "PROJECT_ID"
    CMS_BASE_URL = "CMS_BASE_URL"


def write_to_github_env(key: str, value: str):
    env_file = os.getenv('GITHUB_ENV', "")

    with open(env_file, "a") as myfile:
        myfile.write(f"{key}={value}\n")


def fmt_cms_base_url(sub: str) -> str:
    return CMS_BASE_URL_TEMP.format(sub=sub)


@dataclass
class TokenAuthenticator:

    target_token: str

    _payload: dict[str, any] = field(default_factory=dict)

    def is_not_blank(self) -> bool:
        if not self.token:
            raise Exception(
                "Token is blank. Please set TOKEN environment variable."
            )

    @classmethod
    def generate_token(cls):
        return jwt.encode({
            "target_sub": "api-dev",
            "tenant_id": TENANT_ID,
            "project_id": PROJECT_ID,
            "time": str(datetime.datetime.utcnow()),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        }, CMS_API_KEY.split(",")[0], algorithm="HS256")

    def validate_token(self):
        target_token = self.target_token

        def validate_per_token(
                token: str, api_key: str,
                ) -> dict[str, any] | None:
            try:
                payload = jwt.decode(token, api_key, algorithms=["HS256"])
                return payload
            except jwt.InvalidSignatureError:
                print("Invalid signature")
                return None
            except jwt.ExpiredSignatureError:
                print("Expired signature")
                return None

        def validate_candidate(token: str) -> dict[str, any]:
            for api_key in CMS_API_KEY.split(","):
                payload = validate_per_token(token, api_key)
                if payload:
                    return payload
            raise Exception("Invalid token")

        payload = validate_candidate(target_token)
        self._payload = payload

    def set_tenant_id_to_gitenv(self):
        write_to_github_env(ENVKey.TENANT_ID, self._payload["tenant_id"])

    def set_project_id_to_gitenv(self):
        write_to_github_env(ENVKey.PROJECT_ID, self._payload["project_id"])

    def set_target_sub_to_gitenv(self):
        write_to_github_env(
            ENVKey.CMS_BASE_URL,
            fmt_cms_base_url(self._payload["target_sub"]),
        )


def main():
    token_authenticator = TokenAuthenticator(CMS_TOKEN)
    token_authenticator.validate_token()
    token_authenticator.set_tenant_id_to_gitenv()
    token_authenticator.set_project_id_to_gitenv()
    token_authenticator.set_target_sub_to_gitenv()


if __name__ == "__main__":
    main()
