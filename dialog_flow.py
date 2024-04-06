import os
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
import uuid

def dialog_flow(text_to_be_analyzed):
    # Set your project ID and session ID
    DIALOGFLOW_PROJECT_ID = 'coin-exchange-extension-d-lcks'
    SESSION_ID = str(uuid.uuid4())
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "coin-exchange-extension-d-lcks-58cf24687bc3.json"
    # Initialize the Dialogflow session client
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    # Create the text input
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)

    # Create the query input
    query_input = dialogflow.types.QueryInput(text=text_input)
    # Send the query to Dialogflow and get the response
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        tokenName = ""
        intent = response.query_result.intent.display_name.replace("assetInfo.", "").title()
        fulfillmentText = response.query_result.fulfillment_text
        # Assuming `response` is the DetectIntentResponse object you received from Dialogflow
        output_contexts = response.query_result.output_contexts
        # Check if there are any output contexts
        if output_contexts:
            # Get the first output context
            first_output_context = output_contexts[0]
            # Iterate through the items in the parameters of the first output context
            for key, value in first_output_context.parameters.items():
                # Check if the key is "crypto_assets.original"
                if key == "crypto_assets.original":
                    # Extract the string_value
                    tokenName = value.upper()
                    break # Exit the loop once the value is found
        else:
            print("No output contexts found.")
        return tokenName, intent, fulfillmentText
    except InvalidArgument:
        pass
    return "xxx", "xxx", "No response"
