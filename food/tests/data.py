from django.core.files.uploadedfile import SimpleUploadedFile


GIF = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"

PICTURE = SimpleUploadedFile("gif.gif", GIF, content_type="image/gif")


SIGN_UP_DATA = {
    "username": "username",
    "email": "username@email.com",
    "password1": "$Password10",
    "password2": "$Password10",
}

LOG_IN_DATA = {
    "username": "username",
    "password": "$Password10",
}

RESTAURANT_DATA = {
    "name": "Name",
    "address": "Address",
    "description": "Description",
    "photo": PICTURE,
}

ORDER_DATA = {
    "dishes": {"1": 2, "2": 3},
    "region_address": "Unknown",
    "city_address": "Radom",
    "street_address": "Żeromskiego 666",
    "zip_code": "12345",
}
