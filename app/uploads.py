from flask_uploads import UploadSet, IMAGES

post_images = UploadSet('postImages', IMAGES)
profile_photos = UploadSet('profilePhotos', IMAGES)
business_photos = UploadSet('businessPhotos', IMAGES)
request_images = UploadSet('requestImages', IMAGES)
message_images = UploadSet('messageImages', IMAGES)
