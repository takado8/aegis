from googleapiclient.discovery import build
import json
import csv


# Load configuration and create a YouTube service object
with open('../config/config.json') as file:
    config = json.load(file)
    api_key = config.get('youtube_api_key')

youtube = build('youtube', 'v3', developerKey=api_key)


def get_comment_thread_replies(service, parent_id, page_token=None):
    replies = []
    kwargs = {
        'parentId': parent_id,
        'part': 'snippet',
        'maxResults': 100,
        'textFormat': 'plainText'
    }
    if page_token:
        kwargs['pageToken'] = page_token

    response = service.comments().list(**kwargs).execute()

    for item in response['items']:
        reply_id = item['id']
        reply_text = item['snippet']['textDisplay']
        replies.append({'id': reply_id, 'text': reply_text})

    return replies, response.get('nextPageToken')


def get_video_comments(service, **kwargs):
    comments = {}
    results = service.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment_id = item['id']
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments[comment_id] = {
                'text': comment_text,
                'replies': []
            }
            # Check for replies to the comment thread and fetch them
            if item['snippet']['totalReplyCount'] > 0:
                next_page_token = None
                while True:
                    replies, next_page_token = get_comment_thread_replies(service, comment_id, next_page_token)
                    comments[comment_id]['replies'].extend(replies)
                    if not next_page_token:
                        break
        # Check if there is a next page for top-level comments
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break
        if len(comments) >= kwargs['maxResults']:
            break

    return comments


def save_comments_to_csv(comments, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'comment'])
        writer.writeheader()

        for comment_id, comment_data in comments.items():
            # Write the top-level comment
            writer.writerow({
                'id': comment_id,
                'comment': comment_data['text']
            })
            # Write the replies to the top-level comment
            for reply in comment_data['replies']:
                writer.writerow({
                    'id':  reply['id'],
                    'comment': reply['text']
                })


def print_comments_with_indentation(comments):
    for comment_id, comment_info in comments.items():
        # Print the main comment
        print(f"ID: {comment_id}")
        print(comment_info['text'])
        print()  # Newline for better readability

        # Print the replies with indentation
        for reply in comment_info['replies']:
            print(f"\tID: {reply['id']}")  # Indentation for replies
            print(f"\t{reply['text']}")
            print()  # Newline for separation of replies


if __name__ == '__main__':
    # Example usage:
    video_id = 'xsB22KeX-D0'
    comments = get_video_comments(youtube, part='snippet', videoId=video_id,
        textFormat='plainText', maxResults=30)
    # print(comments)
    # print_comments_with_indentation(comments)
    save_comments_to_csv(comments, '../data/wiatraki_comments.csv')
