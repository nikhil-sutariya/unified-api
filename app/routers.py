from fastapi import APIRouter, status, BackgroundTasks, Path
from config import logger, get_settings
from datetime import datetime
from app.models import Project, UserRespnse, UserCreate, UserUpdate, StandardResponse
from app.messages import ErrorMessage, InfoMessage
from helpers.response import Response
from app.repository import get_all_projects, get_all_users, get_user_by_id, get_project_by_id, get_user_by_email, \
    get_user_by_username, create_user, update_user, delete_user_by_id
import json
from helpers import send_mail

settings = get_settings()

user_router = APIRouter()

@user_router.get("/get-projects", response_model=StandardResponse)
async def get_projects():
    try:
        project_instances = await get_all_projects()
        projects = []
        if project_instances:
            for project in project_instances:
                project_data = project.to_dict()
                projects.append(Project(**project_data).model_dump())

        return Response.success(InfoMessage.users_list, projects)
    except Exception as e:
        logger.error(str(e))
        return Response.error(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorMessage.server_error, str(e))

@user_router.get("/get-users", response_model=StandardResponse)
async def get_users():
    try:
        user_instances = await get_all_users()
        users = []
        if user_instances:
            for user in user_instances:
                user_data = user.to_dict()
                users.append(json.loads(UserRespnse(**user_data).model_dump_json()))

        return Response.success(InfoMessage.users_list, users)
    except Exception as e:
        logger.error(str(e))
        return Response.error(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorMessage.server_error, str(e))

@user_router.post("/add-users", response_model=StandardResponse)
async def add_users(payload: UserCreate):
    try:
        project_exists = await get_project_by_id(payload.project_id)
        if not project_exists:
            return Response.not_found(ErrorMessage.project_not_exists, None)
        
        email_exists = await get_user_by_email(payload.email)
        if email_exists:
            return Response.bad_request(ErrorMessage.email_address_exists, None)
        
        username_exits = await get_user_by_username(payload.username)
        if username_exits:
            return Response.bad_request(ErrorMessage.username_address_exists, None)
        
        user_data = await create_user(payload)
        user = UserRespnse(**user_data).model_dump_json()
        return Response.created(InfoMessage.user_created, json.loads(user))
    
    except Exception as e:
        logger.error(str(e))
        return Response.error(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorMessage.server_error, str(e))

@user_router.get("/get-user/{user_id}", response_model=StandardResponse)
async def get_user(user_id: str = Path(description="Id of the user")):
    try:
        user_instance = await get_user_by_id(user_id)
        if not user_instance:
            return Response.not_found(ErrorMessage.user_not_exists, None)
    
        user = UserRespnse(**user_instance).model_dump_json()
        return Response.success(InfoMessage.user_details, json.loads(user))
        
    except Exception as e:
        logger.error(str(e))
        return Response.error(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorMessage.server_error, str(e))

@user_router.put("/update-user/{user_id}")
async def update_users(user_id: str = Path(description="Id of the user"), payload: UserUpdate = None):
    try:
        user_instance = await get_user_by_id(user_id)
        if not user_instance:
            return Response.not_found(ErrorMessage.user_not_exists, None)
        
        payload_data = payload.model_dump(exclude_none=True)

        if not payload_data:
            return Response.bad_request(ErrorMessage.no_data, None)
        
        updated_user = await update_user(user_id, payload_data)

        if not updated_user:
            return Response.bad_request(ErrorMessage.user_not_updated, None)
        
        user = UserRespnse(**updated_user).model_dump_json()
        return Response.success(InfoMessage.user_created, json.loads(user))
        
    except Exception as e:
        logger.error(str(e))
        return Response.error(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorMessage.server_error, str(e))

@user_router.delete("/delete-user/{user_id}")
async def delete_users(user_id: str = Path(description="Id of the user")):
    try:
        user_instance = await get_user_by_id(user_id)
        if not user_instance:
            return Response.not_found(ErrorMessage.user_not_exists, None)
        
        user_deleted = await delete_user_by_id(user_id)
        if not user_deleted:
            return Response.bad_request(ErrorMessage.user_not_deleted, None)
        
        return Response.success(InfoMessage.user_deleted, {"user_id": user_id})
        
    except Exception as e:
        logger.error(str(e))
        return Response.error(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorMessage.server_error, str(e))

@user_router.get("/send-invite")
async def send_invite(background_tasks: BackgroundTasks):
    try:
        redoc_link = f"{settings.host_url}/redoc"
        swagger_link = f"{settings.host_url}/docs"
        github_link = "https://github.com/nikhil-sutariya/unified-api"

        context = {
            "redoc_link": redoc_link,
            "swagger_link": swagger_link,
            "github_link": github_link
        }

        emails = ["shraddha@aviato.consulting", "pooja@aviato.consulting", "prijesh@aviato.consulting", "hiring@aviato.consulting"]
        background_tasks.add_task(send_mail.send, "API Documentation Invitation", emails, "email_invite.html", context, 'firestore-fb.png')
        return Response.success(InfoMessage.invitation_mail_sent, None)
    
    except Exception as e:
        logger.error(str(e))
        return Response.error(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorMessage.server_error, str(e))
