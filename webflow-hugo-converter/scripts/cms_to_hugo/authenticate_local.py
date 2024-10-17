from .authenticate_workflow import TokenAuthenticator


def main():
    token = TokenAuthenticator.generate_token()
    token_authenticator = TokenAuthenticator(token)
    token_authenticator.validate_token()
    print(token)


if __name__ == "__main__":
    main()
