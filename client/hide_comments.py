import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "../config/client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    request = youtube.comments().setModerationStatus(
        id="UgzHEOPe3QlmzTO4pXR4AaABAg",
        moderationStatus="rejected"
    )
    request.execute()


if __name__ == "__main__":
    main()