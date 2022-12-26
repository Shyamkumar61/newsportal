from urllib.parse import urlparse, parse_qs

class MediaEmbed:

    def __init__(self, url):
        self.url = url
        self.parts = urlparse(self.url)

    def replace_with_embed(self):
        if 'youtube.com' in self.parts.netloc or 'youtu.be' in self.parts.netloc:
            return self.youtube_embed()
        elif 'twitter.com' in self.parts.netloc:
            return self.twitter_embed()
        elif 'facebook.com' in self.parts.netloc:
            return self.facebook_embed()
        elif 'instagram.com' in self.parts.netloc:
            return self.facebook_embed()
        return self.url

    def youtube_embed(self):
        youbute_iframe = '<iframe width="420" height="315" src="https://www.youtube.com/embed/{}"></iframe>'
        if 'youtu.be' in self.parts.netloc:
            youtube_id = self.parts.path.strip('/')
        else:
            query = parse_qs(self.parts.query)
            youtube_id = query["v"][0]
        return youbute_iframe.format(youtube_id)

    def twitter_embed(self):
        twitter_tweet = '<blockquote class="twitter-tweet" tw-align-center data-lang="en"><p lang="en" dir="ltr">Twitter tweet: <a href="{}">{}</a></p></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
        return twitter_tweet.format(self.url, self.url)

    def facebook_embed(self):
        facebbok_post = """<div class="fb-post" data-href="{}" data-width="500">
                <blockquote class="fb-xfbml-parse-ignore">
                    <p>Facebook Post: <a href="{}">{}</a></p></blockquote></div>
                """
        return facebbok_post.format(self.url, self.url, self.url)

    def instagram_embed(self):
        insta_photo = """<blockquote class="instagram-media" data-instgrm-permalink="{}" data-instgrm-version="12" style="max-width:540px; min-width:326px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);">
                        <div style="padding:16px;">
                            <p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;"><a href="https://www.instagram.com/p/B5ihrA3gbFf/" style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none;" target="_blank">Instagram Post: {}</a></p>
                        </div>
                    </blockquote>"""
        return insta_photo.format(self.url, self.url)