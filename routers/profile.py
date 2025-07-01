
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from supabase import Client
from database import supabase
from utils.jwt_token import get_current_user
from models.user import UserUpdate
import os
import uuid
from datetime import datetime

router = APIRouter(prefix="/profile", tags=["profile"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.get("/landing")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    
    try:
        user_id = current_user.get("sub")
        
   
        response = supabase.table("user_profiles").select("username, email, profile_pic_url").eq("id", user_id).single().execute()
        
        if response.data:
            profile_data = response.data            
            return profile_data
        else:
            raise HTTPException(status_code=404, detail="User profile not found")
        
    except Exception as e:
        print(f"Error in get_user_profile: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch user profile: {str(e)}"
        )

@router.get("/info")
async def get_user_info(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        response = supabase.table("user_profiles").select("username, email, phone, profile_pic_url").eq("id", user_id).single().execute()

        if response.data:
            profile_pic_url = response.data.get("profile_pic_url")
            response.data["profile_pic_url"] = profile_pic_url
            return response.data
        else:
            raise HTTPException(status_code=404, detail="User profile not found")
            
    except Exception as e:
        print(f"Error in get_user_info: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to fetch user info: {str(e)}")



@router.put("/update")
async def update_user_profile(
    username: str = Form(None),
    email: str = Form(None),
    file: UploadFile = File(None),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("sub")
        update_data = {}

    
        if username:
            update_data["username"] = username
        if email:
            update_data["email"] = email

        
        if file:
        
            allowed_types = [
                'image/jpeg',
                'image/jpg', 
                'image/png',
            ]
            
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            is_valid_content_type = (
                file.content_type and 
                (file.content_type.startswith('image/') or file.content_type in allowed_types)
            )
            is_valid_extension = (
                file.filename and 
                any(file.filename.lower().endswith(ext) for ext in allowed_extensions)
            )
            if not (is_valid_content_type or is_valid_extension):
                error_msg = f"Invalid file type. Received content-type: '{file.content_type}', filename: '{file.filename}'"
                print(f"VALIDATION FAILED: {error_msg}")
                raise HTTPException(status_code=400, detail=error_msg)
            import os
            import uuid
            from datetime import datetime
            
            file_extension = os.path.splitext(file.filename)[1] if file.filename else '.jpg'
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = f"{user_id}/{unique_filename}"

            try:
                file_bytes = await file.read()
                print(f"File read successfully, size: {len(file_bytes)} bytes")
                
                await file.seek(0)
            
                try:
                    current_profile = supabase.table("user_profiles").select("profile_pic_url").eq("id", user_id).single().execute()
                    
                    if current_profile.data and current_profile.data.get("profile_pic_url"):
                        old_url = current_profile.data["profile_pic_url"]
                        if "profile-images" in old_url:
                            old_file_path = old_url.split("profile-images/")[-1].split("?")[0]
                            if old_file_path.startswith(user_id):
                                supabase.storage.from_("profile-images").remove([old_file_path])
                                print(f"Deleted old profile image: {old_file_path}")
                except Exception as delete_error:
                    print(f"Could not delete old profile image: {delete_error}")

                print(f"Uploading to path: {file_path}")
                storage_resp = supabase.storage.from_("profile-images").upload(
                    file_path, 
                    file_bytes, 
                    {
                        "content-type": file.content_type or "image/jpeg",
                        "upsert": "true"
                    }
                )
                print(f"Storage upload response: {storage_resp}")

                if hasattr(storage_resp, 'error') and storage_resp.error:
                    print(f"Storage upload error: {storage_resp.error}")
                    raise HTTPException(status_code=400, detail=f"Failed to upload image: {storage_resp.error}")

                profile_pic_url = supabase.storage.from_("profile-images").get_public_url(file_path)
                
                if profile_pic_url:
                    timestamp = int(datetime.now().timestamp())
                    profile_pic_url = f"{profile_pic_url}?t={timestamp}"
                    update_data["profile_pic_url"] = profile_pic_url
                    print(f"New profile pic URL: {profile_pic_url}")
                else:
                    raise HTTPException(status_code=400, detail="Failed to get public URL for uploaded image")

            except Exception as upload_error:
                print(f"File upload error: {upload_error}")
                raise HTTPException(status_code=400, detail=f"Failed to upload file: {str(upload_error)}")
            
        if update_data:
            print(f"Updating user {user_id} with data: {update_data}")
            
            response = supabase.table("user_profiles").update(update_data).eq("id", user_id).execute()
            
            print(f"Database update response: {response}")
            
            if response.data:
                return {
                    "message": "Profile updated successfully", 
                    "data": response.data[0] if response.data else None
                }
            else:
                raise HTTPException(status_code=400, detail="Failed to update profile in database")
        else:
            raise HTTPException(status_code=400, detail="No data provided for update")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in update_user_profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")