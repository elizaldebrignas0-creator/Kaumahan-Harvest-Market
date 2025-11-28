# Render Environment Variables Setup

## AWS S3 Configuration (Option 1 - Recommended)

Add these environment variables in your Render dashboard:

### Required AWS S3 Variables:
```
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_STORAGE_BUCKET_NAME=your_unique_bucket_name
AWS_S3_REGION_NAME=us-east-1
```

### Other Required Variables:
```
SECRET_KEY=your_django_secret_key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
ALLOWED_HOSTS=*.onrender.com,your-domain.com
```

## AWS S3 Setup Instructions:

### 1. Create AWS S3 Bucket:
1. Go to AWS Console → S3
2. Click "Create bucket"
3. Bucket name: `your-unique-bucket-name` (must be globally unique)
4. Region: `us-east-1` (or your preferred region)
5. Block public access: **UNCHECK** all boxes (we need public access)
6. Enable "ACLs enabled"
7. Create bucket

### 2. Create IAM User:
1. Go to AWS Console → IAM → Users
2. Click "Create user"
3. User name: `django-media-uploader`
4. Select "Attach policies directly"
5. Add policy: `AmazonS3FullAccess`
6. Create user
7. Save **Access key ID** and **Secret access key**

### 3. Configure Bucket CORS:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>https://*.onrender.com</AllowedOrigin>
    <AllowedOrigin>http://localhost:8000</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>DELETE</AllowedMethod>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

### 4. Set Bucket ACL:
1. Go to your S3 bucket → Permissions tab
2. Edit "Object ownership" → "ACLs enabled"
3. Edit "Block public access" → **UNCHECK** "Block all public access"
4. Save changes

## Cloudinary Configuration (Option 2 - Easiest)

If you prefer Cloudinary instead:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Cloudinary Setup:
1. Sign up at https://cloudinary.com
2. Get your cloud name, API key, and secret from Dashboard
3. Add the environment variables above

## Testing:

After deployment, test with:
```python
python manage.py shell
>>> from django.core.files.storage import default_storage
>>> default_storage.url('test.jpg')
'https://your-bucket.s3.amazonaws.com/media/test.jpg'
```
