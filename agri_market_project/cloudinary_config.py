import cloudinary
from decouple import config

# move to bottom to avoid circular imports in the produce app - which has settings import and cloudinary
cloudinary.config(
    api_key = config('CLOUDINARY_API_KEY'),
    api_secret = config('CLOUDINARY_API_SECRET'),
    cloud_name = config('CLOUDINARY_CLOUD_NAME'),
    secure = True
)