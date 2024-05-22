from fastapi import APIRouter, Path, Security

from kairon.shared.utils import Utility
from kairon.shared.auth import Authentication
from kairon.api.models import (
    Response,
    HttpActionConfigRequest, SlotSetActionRequest, EmailActionRequest, GoogleSearchActionRequest, JiraActionRequest,
    ZendeskActionRequest, PipedriveActionRequest, HubspotFormsActionRequest, TwoStageFallbackConfigRequest,
    RazorpayActionRequest, PromptActionConfigRequest, DatabaseActionRequest, PyscriptActionRequest,
    WebSearchActionRequest, LiveAgentActionRequest
)
from kairon.shared.constants import TESTER_ACCESS, DESIGNER_ACCESS
from kairon.shared.models import User
from kairon.shared.data.processor import MongoProcessor

router = APIRouter()
mongo_processor = MongoProcessor()


@router.post("/httpaction", response_model=Response)
async def add_http_action(
        request_data: HttpActionConfigRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the http action config and story event
    """
    http_config_id = mongo_processor.add_http_action_config(request_data.dict(), current_user.get_user(),
                                                            current_user.get_bot())
    response = {"http_config_id": http_config_id}
    message = "Http action added!"
    return Response(data=response, message=message)


@router.get("/httpaction/{action}", response_model=Response)
async def get_http_action(action: str = Path(description="action name", examples=["http_action"]),
                          current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns configuration set for the HTTP action
    """
    http_action_config = mongo_processor.get_http_action_config(action_name=action, bot=current_user.get_bot())
    return Response(data=http_action_config)


@router.get("/httpaction", response_model=Response)
async def list_http_actions(current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns list of http actions for bot.
    """
    actions = mongo_processor.list_http_actions(bot=current_user.get_bot())
    return Response(data=actions)


@router.put("/httpaction", response_model=Response)
async def update_http_action(
        request_data: HttpActionConfigRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Updates the http action config and related story event
    """
    http_config_id = mongo_processor.update_http_config(request_data=request_data.dict(), user=current_user.get_user(),
                                                        bot=current_user.get_bot())
    response = {"http_config_id": http_config_id}
    message = "Http action updated!"
    return Response(data=response, message=message)


@router.post("/pyscript", response_model=Response)
async def add_pyscript_action(
        request_data: PyscriptActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the Pyscript action config
    """
    pyscript_config_id = mongo_processor.add_pyscript_action(request_data.dict(), current_user.get_user(),
                                                             current_user.get_bot())
    return Response(data={"_id": pyscript_config_id}, message="Action added!")


@router.get("/pyscript", response_model=Response)
async def list_pyscript_actions(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns list of pyscript actions for bot.
    """
    actions = list(mongo_processor.list_pyscript_actions(bot=current_user.get_bot()))
    return Response(data=actions)


@router.put("/pyscript", response_model=Response)
async def update_pyscript_action(
        request_data: PyscriptActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Updates the pyscript action config
    """
    action_id = mongo_processor.update_pyscript_action(request_data=request_data.dict(), user=current_user.get_user(),
                                                       bot=current_user.get_bot())
    return Response(data={"_id": action_id}, message="Action updated!")


@router.post("/db", response_model=Response)
async def add_db_action(
        request_data: DatabaseActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the vectordb action config and story event
    """
    action_id = mongo_processor.add_db_action(request_data.dict(), current_user.get_user(),
                                              current_user.get_bot())
    return Response(data={"_id": action_id}, message="Action added!")


@router.get("/db/{action}", response_model=Response)
async def get_vector_db_action(action: str = Path(description="name", examples=["database_action"]),
                               current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns configuration set for the VectorDb action
    """
    action_config = mongo_processor.get_db_action_config(action=action, bot=current_user.get_bot())
    return Response(data=action_config)


@router.get("/db", response_model=Response)
async def list_db_actions(current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns list of vectordb actions for bot.
    """
    actions = list(mongo_processor.list_db_actions(bot=current_user.get_bot()))
    return Response(data=actions)


@router.put("/db", response_model=Response)
async def update_db_action(
        request_data: DatabaseActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Updates the vectordb action config and related story event
    """
    action_id = mongo_processor.update_db_action(request_data=request_data.dict(), user=current_user.get_user(),
                                                 bot=current_user.get_bot())
    return Response(data={"_id": action_id}, message="Action updated!")


@router.post("/jira", response_model=Response)
async def add_jira_action(
        request_data: JiraActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores Jira action config.
    """
    mongo_processor.add_jira_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action added')


@router.get("/jira", response_model=Response)
async def list_jira_actions(current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns list of Jira actions for bot.
    """
    actions = list(mongo_processor.list_jira_actions(current_user.get_bot()))
    return Response(data=actions)


@router.put("/jira", response_model=Response)
async def edit_jira_action(
        request_data: JiraActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Edits the Jira action config.
    """
    mongo_processor.edit_jira_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action updated')


@router.post("/slotset", response_model=Response)
async def add_slot_set_action(
        request_data: SlotSetActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the slot set action config.
    """
    mongo_processor.add_slot_set_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action added')


@router.get("/slotset", response_model=Response)
async def list_slot_set_actions(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)
):
    """
    Returns list of slot set actions for bot.
    """
    actions = mongo_processor.list_slot_set_actions(current_user.get_bot())
    return Response(data=actions)


@router.put("/slotset", response_model=Response)
async def edit_slot_set_action(
        request_data: SlotSetActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Edits the slot set action config.
    """
    mongo_processor.edit_slot_set_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action updated')


@router.post("/googlesearch", response_model=Response)
async def add_google_search_action(
        request_data: GoogleSearchActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the google search action config.
    """
    action_id = mongo_processor.add_google_search_action(
        request_data.dict(), current_user.get_bot(), current_user.get_user()
    )
    return Response(data=action_id, message='Action added')


@router.get("/googlesearch", response_model=Response)
async def list_google_search_actions(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)
):
    """
    Returns list of google search actions for bot.
    """
    actions = list(mongo_processor.list_google_search_actions(bot=current_user.get_bot()))
    return Response(data=actions)


@router.put("/googlesearch", response_model=Response)
async def update_google_search_action(
        request_data: GoogleSearchActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Updates the google search action configuration.
    """
    mongo_processor.edit_google_search_action(
        request_data.dict(), current_user.get_bot(), current_user.get_user()
    )
    return Response(message='Action updated')


@router.post("/websearch", response_model=Response)
async def add_web_search_action(
        request_data: WebSearchActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the public search action config.
    """
    action_id = mongo_processor.add_web_search_action(
        request_data.dict(), current_user.get_bot(), current_user.get_user()
    )
    return Response(data=action_id, message='Action added')


@router.get("/websearch", response_model=Response)
async def list_web_search_actions(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)
):
    """
    Returns list of public search actions for bot.
    """
    actions = list(mongo_processor.list_web_search_actions(bot=current_user.get_bot()))
    return Response(data=actions)


@router.put("/websearch", response_model=Response)
async def update_web_search_action(
        request_data: WebSearchActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Updates the public search action configuration.
    """
    mongo_processor.edit_web_search_action(
        request_data.dict(), current_user.get_bot(), current_user.get_user()
    )
    return Response(message='Action updated')


@router.post("/email", response_model=Response)
async def add_email_action(
        request_data: EmailActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the email action config.
    """
    mongo_processor.add_email_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action added')


@router.get("/email", response_model=Response)
async def list_email_actions(current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns list of email actions for bot.
    """
    actions = list(mongo_processor.list_email_action(current_user.get_bot()))
    return Response(data=actions)


@router.put("/email", response_model=Response)
async def edit_email_action(
        request_data: EmailActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Edits the email action config.
    """
    mongo_processor.edit_email_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action updated')


@router.post("/zendesk", response_model=Response)
async def add_zendesk_action(
        request_data: ZendeskActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the zendesk action config.
    """
    mongo_processor.add_zendesk_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action added')


@router.get("/zendesk", response_model=Response)
async def list_zendesk_actions(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns list of zendesk actions for bot.
    """
    actions = list(mongo_processor.list_zendesk_actions(current_user.get_bot()))
    return Response(data=actions)


@router.put("/zendesk", response_model=Response)
async def edit_zendesk_action(
        request_data: ZendeskActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Edits the zendesk action config.
    """
    mongo_processor.edit_zendesk_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action updated')


@router.post("/pipedrive", response_model=Response)
async def add_pipedrive_action(
        request_data: PipedriveActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the pipedrive leads action config.
    """
    mongo_processor.add_pipedrive_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action added')


@router.get("/pipedrive", response_model=Response)
async def list_pipedrive_actions(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns list of pipedrive leads actions for bot.
    """
    actions = list(mongo_processor.list_pipedrive_actions(current_user.get_bot()))
    return Response(data=actions)


@router.put("/pipedrive", response_model=Response)
async def edit_pipedrive_action(
        request_data: PipedriveActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Edits the pipedrive leads action config.
    """
    mongo_processor.edit_pipedrive_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action updated')


@router.post("/hubspot/forms", response_model=Response)
async def add_hubspot_forms_action(
        request_data: HubspotFormsActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the hubspot forms action config.
    """
    mongo_processor.add_hubspot_forms_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action added')


@router.get("/hubspot/forms", response_model=Response)
async def list_hubspot_forms_actions(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns list of hubspot forms actions for bot.
    """
    actions = list(mongo_processor.list_hubspot_forms_actions(current_user.get_bot()))
    return Response(data=actions)


@router.put("/hubspot/forms", response_model=Response)
async def edit_hubspot_forms_action(
        request_data: HubspotFormsActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Edits the hubspot forms action config.
    """
    mongo_processor.edit_hubspot_forms_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message='Action updated')


@router.delete("/{action}", response_model=Response)
async def delete_action(
        action: str = Path(description="action name", examples=["action_pipedrive"]),
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Deletes the action config.
    """
    mongo_processor.delete_action(action, current_user.get_bot(), current_user.get_user())
    return Response(message='Action deleted')


@router.get("/fields/list", response_model=Response)
async def list_integration_fields(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)
):
    """
    List required and optional fields for integrated actions.
    """
    return Response(data=Utility.system_metadata['actions'])


@router.post("/fallback/two_stage", response_model=Response)
async def add_two_stage_fallback_action(
        request_data: TwoStageFallbackConfigRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the two stage fallback action config.
    """
    mongo_processor.add_two_stage_fallback_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message="Action added!")


@router.get("/fallback/two_stage", response_model=Response)
async def get_two_stage_fallback_action(current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns configuration for two stage fallback action.
    """
    config = list(mongo_processor.get_two_stage_fallback_action_config(bot=current_user.get_bot()))
    return Response(data=config)


@router.put("/fallback/two_stage", response_model=Response)
async def update_two_stage_fallback_action(
        request_data: TwoStageFallbackConfigRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Updates the two stage fallback action config.
    """
    mongo_processor.edit_two_stage_fallback_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message="Action updated!")


@router.post("/prompt", response_model=Response)
async def add_prompt_action(
        request_data: PromptActionConfigRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores Kairon FAQ Action
    """
    return {
        "message": "Action Added Successfully",
        "data": {
            "_id": mongo_processor.add_prompt_action(
                request_data.dict(),
                current_user.get_bot(),
                current_user.get_user()
            )
        }
    }


@router.put("/prompt/{faq_action_id}", response_model=Response)
async def update_prompt_action(
        faq_action_id: str,
        request_data: PromptActionConfigRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Updates kairon FAQ Action
    """
    mongo_processor.edit_prompt_action(faq_action_id, request_data.dict(),
                                       current_user.get_bot(), current_user.get_user())
    return Response(message="Action updated!")


@router.get("/prompt", response_model=Response)
async def get_prompt_action(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)
):
    """
    Retrieves kairon FAQ Action
    """
    action = mongo_processor.get_prompt_action(current_user.get_bot())
    return Response(data=action)


@router.post("/razorpay", response_model=Response)
async def add_razorpay_action(
        request_data: RazorpayActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Stores the razorpay action config.
    """
    mongo_processor.add_razorpay_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message="Action added!")


@router.get("/razorpay", response_model=Response)
async def get_razorpay_action(current_user: User = Security(Authentication.get_current_user_and_bot, scopes=TESTER_ACCESS)):
    """
    Returns configuration for razorpay action.
    """
    config = list(mongo_processor.get_razorpay_action_config(bot=current_user.get_bot()))
    return Response(data=config)


@router.put("/razorpay", response_model=Response)
async def update_razorpay_action(
        request_data: RazorpayActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Updates the razorpay action config.
    """
    mongo_processor.edit_razorpay_action(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message="Action updated!")


@router.get("/live_agent", response_model=Response)
async def get_live_agent(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Returns configuration for live agent action.
    """
    config = mongo_processor.get_live_agent(current_user.get_bot())
    return Response(data=config)


@router.post("/live_agent", response_model=Response)
async def enable_live_agent(
        request_data: LiveAgentActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    status = mongo_processor.enable_live_agent(request_data.dict(), current_user.get_bot(), current_user.get_user())
    msg = "Live Agent Action enabled!" if status else "Live Agent Action already enabled!"
    return Response(message=msg)


@router.put("/live_agent", response_model=Response)
async def update_live_agent(
        request_data: LiveAgentActionRequest,
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    """
    Updates the live agent action config.
    """

    mongo_processor.edit_live_agent(request_data.dict(), current_user.get_bot(), current_user.get_user())
    return Response(message="Action updated!")


@router.get("/live_agent/disable", response_model=Response)
async def disable_live_agent(
        current_user: User = Security(Authentication.get_current_user_and_bot, scopes=DESIGNER_ACCESS)
):
    mongo_processor.disable_live_agent(current_user.get_bot())
    return Response(message="Live Agent Action disabled!")

