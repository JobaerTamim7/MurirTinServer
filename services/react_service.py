from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime
from database import supabase
from models.react import ReactCreate, ReactResponse, ComplaintWithReactions

async def toggle_like(complaint_id: int, is_like: bool, current_user: dict) -> ReactResponse:

    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )

    try:
        complaint_response = supabase.table('complaints').select("id").eq("id", complaint_id).single().execute()
        if not complaint_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found."
            )

        existing_reaction = supabase.table('complaint_likes') \
            .select("*") \
            .eq("complaint_id", complaint_id) \
            .eq("user_id", user_id) \
            .execute()

        if existing_reaction.data:
            # User already reacted
            current_reaction = existing_reaction.data[0]
            
            if current_reaction['is_like'] == is_like:
                # Same reaction - remove it
                supabase.table('complaint_likes') \
                    .delete() \
                    .eq("id", current_reaction['id']) \
                    .execute()
                message = "Reaction removed"
            else:
                # Opposite reaction - update it
                supabase.table('complaint_likes') \
                    .update({"is_like": is_like, "created_at": datetime.now().isoformat()}) \
                    .eq("id", current_reaction['id']) \
                    .execute()
                message = "Reaction updated"
        else:
            # No existing reaction - create new one
            supabase.table('complaint_likes') \
                .insert({
                    "complaint_id": complaint_id,
                    "user_id": user_id,
                    "is_like": is_like,
                    "created_at": datetime.now().isoformat()
                }) \
                .execute()
            message = "Reaction added"

        # Get updated counts and user's current reaction
        return await get_complaint_likes(complaint_id, current_user)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error toggling like: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to toggle reaction."
        )

async def get_complaint_likes(complaint_id: int, current_user: dict) -> ReactResponse:
    """
    Get like/dislike counts and current user's reaction for a complaint.
    """
    user_id = current_user.get("sub")
    
    try:
        # Get all reactions for this complaint
        reactions = supabase.table('complaint_likes') \
            .select("*") \
            .eq("complaint_id", complaint_id) \
            .execute()

        like_count = 0
        dislike_count = 0
        user_reaction = None

        if reactions.data:
            for reaction in reactions.data:
                if reaction['is_like']:
                    like_count += 1
                else:
                    dislike_count += 1
                
                # Check if this is the current user's reaction
                if user_id and reaction['user_id'] == user_id:
                    user_reaction = reaction['is_like']

        return ReactResponse(
            message="Success",
            like_count=like_count,
            dislike_count=dislike_count,
            user_reaction=user_reaction
        )

    except Exception as e:
        print(f"Error getting complaint likes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get reaction counts."
        )

async def get_complaints_with_likes(current_user: dict) -> List[ComplaintWithReactions]:
    """
    Get all complaints with like/dislike counts and current user's reactions.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )

    try:
        # Get all complaints
        complaints_response = supabase.table('complaints') \
            .select("*") \
            .order('created_at', desc=True) \
            .execute()

        if not complaints_response.data:
            return []

        # Get all likes for all complaints
        likes_response = supabase.table('complaint_likes') \
            .select("*") \
            .execute()

        # Process data
        complaints_with_likes = []
        
        for complaint in complaints_response.data:
            complaint_id = complaint['id']
            
            # Count likes and dislikes for this complaint
            like_count = 0
            dislike_count = 0
            user_reaction = None
            
            if likes_response.data:
                for like in likes_response.data:
                    if like['complaint_id'] == complaint_id:
                        if like['is_like']:
                            like_count += 1
                        else:
                            dislike_count += 1
                        
                        # Check user's reaction
                        if like['user_id'] == user_id:
                            user_reaction = like['is_like']
            
            # Convert ticket_id to string if it's not None
            ticket_id = complaint.get('ticket_id')
            if ticket_id is not None:
                ticket_id = str(ticket_id)
            
            complaints_with_likes.append(ComplaintWithReactions(
                id=complaint['id'],
                title=complaint['title'],
                description=complaint['description'],
                user_id=complaint['user_id'],
                company_id=complaint['company_id'],
                ticket_id=ticket_id,
                created_at=complaint['created_at'],
                status=complaint['status'],
                like_count=like_count,
                dislike_count=dislike_count,
                user_reaction=user_reaction
            ))

        return complaints_with_likes

    except Exception as e:
        print(f"Error getting complaints with likes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get complaints with likes."
        )
