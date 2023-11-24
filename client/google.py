from googleapiclient.discovery import build
import os
import json


with open('../config.json') as file:
    config = json.load(file)
    api_key = config.get('youtube_api_key')

youtube = build('youtube', 'v3', developerKey=api_key)


def get_video_comments(service, **kwargs):
    comments = {}
    results = service.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment_id = item['id']
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments[comment_id] = comment_text

        # Check if there is a next page
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break
    return comments


def delete_comment(id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    request = youtube.comments().delete(
        id=id
    )
    request.execute()


if __name__ == "__main__":
    delete_comment('Ugy_XwUVdKnmG57-xeR4AaABAg')
    # video_id = 'ZTSq_W0FnW4'
    # comments_dict = get_video_comments(youtube, part='snippet', videoId=video_id, textFormat='plainText')
    #
    # # Print each comment and its ID
    # for comment_id, comment_text in comments_dict.items():
    #     print(f"Comment ID: {comment_id}")
    #     print(f"Comment Text: {comment_text}\n")
