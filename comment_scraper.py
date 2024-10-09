import googleapiclient.discovery
import json
import re

class Comment_Scraper:
    def __init__(self, api_service_name, api_version, DEVELOPER_KEY, video_id, num_comments):
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.DEVELOPER_KEY = DEVELOPER_KEY
        self.video_id = video_id
        self.num_comments = num_comments


    def build_youtube(self):
        youtube = googleapiclient.discovery.build(
            self.api_service_name,
            self.api_version,
            developerKey=self.DEVELOPER_KEY
        )

        print("Built youtube api successfully")

        return youtube

    def build_request(self, youtube):
        request = youtube.commentThreads().list(
            part="snippet",
            videoId = self.video_id,
            maxResults = self.num_comments
        )
        response = request.execute()

        print("Built request successfully")

        return response

    def clean_text(self, text):
        return re.sub(r'[^\x00-\x7F]+', '', text)


    def pull_comments(self, youtube, response):
        data = []

        try:
            nextPageToken = response['nextPageToken']
        except KeyError:
            return 0

        nextPageToken = response['nextPageToken']
        nextRequest = youtube.commentThreads().list(
            part="snippet",
            videoId = self.video_id,
            maxResults = self.num_comments,
            pageToken = nextPageToken

        )

        response = nextRequest.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            author = comment['authorDisplayName']
            text = comment['textOriginal']

            # Clean the comment to avoid illegal multibyte sequences
            cleaned_text = self.clean_text(text)

            data.append([author, cleaned_text])

        return data

    def get_comments(self, pull_all=False, pages=1):
        youtube = self.build_youtube()
        response = self.build_request(youtube)

        comments = {}

        if pull_all:
            while True:
                data = self.pull_comments(youtube, response)

                for element in data:
                    comments[element[0]] = element[1]
        else:
            for _ in range(pages):
                data = self.pull_comments(youtube, response)

                for element in data:
                    comments[element[0]] = element[1]

        return comments

    # Dump to json file
    def export_comments(self, comments):
        json_object = json.dumps(comments, indent=4)

        with open("sample.json", "w") as out:
            out.write(json_object)

        print("Dumped all comments in sample.json")
















