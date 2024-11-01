from database import Users, Projects
from config import logger
from datetime import datetime, timezone
from app.models import UserCreate, UserUpdate
from google.cloud.firestore import FieldFilter


async def get_all_projects() -> list | None:
    """Retrive all projects from collection.

    Returns:
        list | None: A list of dictionaries with project details or none if there 
        is no document stored in db.
    """
    
    try:
        projects = Projects.stream()
        return [project for project in projects]

    except Exception as e:
        logger.error(str(e))
        return None

async def get_all_users() -> list | None:
    """Retrive all users from collection.

    Returns:
        list | None: A list of dictionaries with user details or none if there 
        is no document stored in db.
    """
    
    try:
        users = Users.stream()
        return [user for user in users]

    except Exception as e:
        logger.error(str(e))
        return None

async def get_user_by_id(user_id: str) -> dict | None:
    """Retrive user by id from collection.

    Args:
        user_id: Id of the user.

    Returns:
        dict | None: A dictionary with user details or none.
    """

    try:
        user_document = Users.document(user_id).get()
        if user_document.exists:
            return user_document.to_dict()
        return None

    except Exception as e:
        logger.error(str(e))
        return None

async def get_user_by_email(email: str) -> dict | None:
    """Retrive user by email from collection.

    Args:
        email: Email address of the user of the user.

    Returns:
        dict | None: A dictionary with user details or none.
    """

    try:
        users_query = Users.where(filter=FieldFilter("email", "==", email)).limit(1).stream()
        user_document = next(users_query, None)
        
        if user_document:
            return user_document.to_dict()
        return None

    except Exception as e:
        logger.error(str(e))
        return None
    
async def get_user_by_username(username: str) -> dict | None:
    """Retrive user by username from collection.

    Args:
        username: username of the user.

    Returns:
        dict | None: A dictionary with user details or none.
    """

    try:
        users_query = Users.where(filter=FieldFilter("username", "==", username)).limit(1).stream()
        user_document = next(users_query, None)
        
        if user_document:
            return user_document.to_dict()
        return None

    except Exception as e:
        logger.error(str(e))
        return None

async def get_project_by_id(project_id: int) -> dict | None:
    """Retrive user by id from collection.

    Args:
        project_id: Id of the project.

    Returns:
        dict | None: A dictionary with user details or none.
    """

    try:
        project_document = Projects.document(str(project_id)).get()
        if project_document.exists:
            return project_document.to_dict()
        return None

    except Exception as e:
        logger.error(str(e))
        return None

async def create_user(user_data: UserCreate) -> dict:
    """Add a new user to the Firestore collection.

    Args:
        user_data (UserCreate): The data for the new user.

    Returns:
        dict: A dictionary with the created user details.
    """
    try:
        current_timestamp = datetime.now(timezone.utc)
        user_document = Users.document()
        user_data = user_data.model_dump()
        user_data['id'] = user_document.id
        user_data['created_at'] = current_timestamp
        user_data['updated_at'] = current_timestamp
        user_document.set(user_data)
        return user_data
    
    except Exception as e:
        logger.error(str(e))
        return None

async def update_user(user_id: str, user_data: dict) -> dict:
    """Update user to the Firestore collection.

    Args:
        user_data: The data for the user.
        user_id: Id of the user

    Returns:
        dict: A dictionary with the created user details.
    """
    try:
        current_timestamp = datetime.now(timezone.utc)
        user_document = Users.document(user_id)
        user_data['updated_at'] = current_timestamp
        user_document.update(user_data)
        updated_user = user_document.get().to_dict()
        return updated_user
    
    except Exception as e:
        logger.error(str(e))
        return None

async def delete_user_by_id(user_id: str) -> str:
    """Delete specific user from the Firestore collection.

    Args:
        user_id: Id of the existing user.

    Returns:
        str: User id of the user
    """
    try:
        Users.document(user_id).delete()
        return user_id
    
    except Exception as e:
        logger.error(str(e))
        return None

