import cloudinary
import cloudinary.uploader
import cloudinary.api

# 1. Configure Cloudinary
cloudinary.config( 
  cloud_name = "finttein", 
  api_key = "837699919773594", 
  api_secret = "vqU32ikakYbmhKTCTVSlrgENyTM" 
)

# 2. Upload an image
print("Uploading image...")
upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/sample.jpg")
print(f"Secure URL: {upload_result.get('secure_url')}")
print(f"Public ID: {upload_result.get('public_id')}")

# 3. Get image details
print("\nFetching image details...")
details = cloudinary.api.resource(upload_result.get('public_id'))
print(f"Width: {details.get('width')}px")
print(f"Height: {details.get('height')}px")
print(f"Format: {details.get('format')}")
print(f"File size: {details.get('bytes')} bytes")

# 4. Transform the image
print("\nGenerating transformed image URL...")
# f_auto: Automatically selects the most efficient image format based on the browser (e.g., WebP, AVIF)
# q_auto: Automatically adjusts the image quality to reduce file size without losing visual fidelity
transformed_url, _ = cloudinary.utils.cloudinary_url(
    upload_result.get('public_id'),
    fetch_format="auto",
    quality="auto"
)
print("Done! Click link below to see optimized version of the image. Check the size and the format.")
print(transformed_url)
