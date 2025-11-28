# 🚀 Render Cloudinary Setup Guide

## 🔧 Step-by-Step Instructions

### 1. Set Up Cloudinary Account (5 minutes)

1. **Go to**: https://cloudinary.com/
2. **Sign up** for free account
3. **Get your credentials** from Dashboard:
   - Cloud name
   - API Key  
   - API Secret

### 2. Add Environment Variables in Render

In your Render dashboard → Environment Variables, add these:

```
Key: CLOUDINARY_CLOUD_NAME
Value: your-cloud-name-here

Key: CLOUDINARY_API_KEY  
Value: 123456789012345

Key: CLOUDINARY_API_SECRET
Value: your-api-secret-here

Key: CLOUDINARY_URL
Value: cloudinary://123456789012345:your-api-secret@your-cloud-name

Key: DJANGO_SETTINGS_MODULE
Value: kaumahan.settings_cloudinary
```

### 3. Deploy Your Changes

Push your changes to GitHub, Render will auto-deploy:

```bash
git add .
git commit -m "feat: add Cloudinary storage for persistent media"
git push origin main
```

### 4. Verify It Works

After deployment (2-3 minutes):

1. **Upload a product image** in your admin panel
2. **Check the image URL** - it should be from Cloudinary
3. **Test persistence** - restart your service, image should remain

## 🎯 Expected Results

✅ **Images persist forever** in Cloudinary cloud storage  
✅ **Auto-optimization** - faster loading, smaller files  
✅ **CDN included** - global delivery  
✅ **Free tier** - 25GB storage (plenty for your needs)  
✅ **No more disappearing images**  

## 🔍 How to Check It's Working

### In Django Admin:
1. Upload a product image
2. Check the image URL - should be like:
   `https://res.cloudinary.com/your-cloud-name/image/upload/v1234567/products/image.jpg`

### In Browser Console:
```javascript
// Check image URLs are from Cloudinary
document.querySelectorAll('img[src*="/media/"]').forEach(img => {
    console.log('Image URL:', img.src);
});
```

### In Render Logs:
Look for Cloudinary URLs in your deployment logs.

## 🚨 Troubleshooting

### Images still local?
- Check `DJANGO_SETTINGS_MODULE=kaumahan.settings_cloudinary`
- Verify Cloudinary environment variables are set
- Restart your Render service

### Upload errors?
- Verify Cloudinary credentials are correct
- Check Cloudinary dashboard for API calls
- Ensure Cloudinary account is active

### Images not displaying?
- Check Cloudinary URL format
- Verify image permissions in Cloudinary
- Check browser console for 404 errors

## 📞 Support

If you need help:
1. Check Render deployment logs
2. Verify Cloudinary dashboard
3. Test with a new image upload
4. Check Django admin for image URLs

---

**This setup will completely solve your disappearing images problem!**
