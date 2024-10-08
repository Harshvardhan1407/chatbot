# import os
# import json
# import logging
# import requests
# from dotenv import load_dotenv
# from openai import OpenAI
# import config
# import chatbot_prompt
# import config_toolcall

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='chatbot.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')

# class OpenAIBot:
#     def __init__(self, engine):
#         self.conversations = {}  # Stores conversations by session ID
#         self.engine = engine

#     def start_conversation(self, session_id):
#         if session_id not in self.conversations:
#             self.conversations[session_id] = chatbot_prompt.prompt.copy()  # Initialize conversation with a system message
#             logger.info(f"Started new conversation with session_id: {session_id}")
#         else:
#             self.conversations[session_id]= chatbot_prompt.prompt.copy()
#     def add_message(self, session_id, role, content):
#         if content is not None:
#             self.conversations[session_id].append({"role": role, "content": content})
#         else:
#             logger.info(f"Attempted to add a message with null content for role {role} in session {session_id}")

#     def save_conversation(self, filename, session_id):
#         try:
#             with open(filename, 'w') as file:
#                 json.dump({session_id: self.conversations[session_id]}, file, indent=4)
#             logger.info(f"Conversation saved to {filename}")
#         except Exception as e:
#             logger.error(f"Failed to save conversation: {e}")

#     def login_api(self):
#         try:
#             url = config.login_api
#             response = requests.get(url)
#             if response.status_code == 200:
#                 return response.json()['resource']
#             logger.info("login_api success")
#         except Exception as e:
#             logger.info("error fetching login api:", e)

#     def consumer_details(self):
#         try:
#             data = self.login_api()
#             keys_to_fetch = ['location_id', "flat_number", 'consumer_name', "consumer_mobile_no", "consumer_email_id", "balance_amount"]
#             output = {key: data[key] for key in keys_to_fetch}
#             output["login_id"] = output["location_id"]
#             del output["location_id"]
#             logger.info("consumer_details success")
#             return output
#         except Exception as e:
#             logger.info("error fetching consumer_details:", e)

#     def notifiation(self):
#         try:
#             data = self.login_api()
#             keys_to_fetch = ['notification_email', 'notification_sms', 'notification_ivrs', 'notification_app_load', 'notification_app_balance', 'low_bal_alert', 'notification_app_esource', 'notification_app_unit_consumption', 'alert_daily_consumption_grid', 'alert_daily_consumption_dg', 'power_cut_restore_notification', 'recharge_notification', 'last_reading_alert_notification']
#             output = {key: data[key] for key in keys_to_fetch}
#             logger.info("notification data success")
#             return output
#         except Exception as e:
#             logger.info("error fetching notification_details:", e)

#     def balance_recharge(self):
#         try:
#             data = self.login_api()
#             keys_to_fetch = ['balance_amount', 'last_recharge_time', 'last_coupon_amount']
#             output = {key: data[key] for key in keys_to_fetch}
#             logger.info("balance_recharge data success")
#             return output
#         except Exception as e:
#             logger.info("error fetching balance and recharge:", e)

#     def consumption(self):
#         try:
#             data = self.login_api()
#             keys_to_fetch = ['dg_reading', 'grid_reading', 'last_reading_updated', 'daily_dg_unit', 'daily_grid_unit', 'monthly_dg_unit', 'monthly_grid_unit', 'daily_dg_amount', 'daily_grid_amount', 'fix_charges_monthly', 'monthly_dg_amount', 'monthly_grid_amount', 'fix_charges', 'energy_source', 'last_reading_updated_dg']
#             output = {key: data[key] for key in keys_to_fetch}
#             logger.info("consumption data success")
#             return output
#         except Exception as e:
#             logger.info("error fetching consumption details:", e)

#     def site_details(self):
#         try:
#             data = self.login_api()
#             keys_to_fetch = ['site_id', 'site_name', 'site_address', 'site_city', 'site_state', 'site_country', 'site_zipcode', 'site_supervisor_name']
#             output = {key: data[key] for key in keys_to_fetch}
#             logger.info("site_details data success")
#             return output
#         except Exception as e:
#             logger.info("error fetching site details:", e)

#     def costumer_support(self):
#         try:
#             data = self.login_api()
#             keys_to_fetch = ['site_supervisor_name', 'site_supervisor_contact_no', 'site_supervisor_email_id', 'site_support_concern_name', 'site_support_contact_no', 'site_support_email_id']
#             output = {key: data[key] for key in keys_to_fetch}
#             logger.info("costumer support data success")
#             return output
#         except Exception as e:
#             logger.info("error fetching costumer support:", e)

#     def daily_data(self):
#         try:
#             url = config.daily_api
#             response = requests.get(url)
#             if response.status_code == 200:
#                 logger.info("daily data fetched")
#                 return response.json()
#         except Exception as e:
#             logger.info("error in daily data fetching", e)

#     def monthly_data(self):
#         try:
#             url = config.monthly_api
#             response = requests.get(url)
#             if response.status_code == 200:
#                 logger.info("monthly data fetched")
#                 return response.json()
#         except Exception as e:
#             logger.info("error in monthly data fetching", e)

#     def power_cut(self):
#         try:
#             output = self.login_api()
#             values = {}
#             if float(output['balance_amount']) < 0:
#                 values['balance'] = output['balance_amount']
#             if output['overload_grid'] in ["y", "Y"]:
#                 values["overload_grid"] = output['overload_grid']
#             elif output['overload_dg'] in ["y", "Y"]:
#                 values["overload_dg"] = output['overload_dg']
#             logger.info(values)
#             return values
#         except Exception as e:
#             logger.info("error in power cut details", e)

#     def generate_response(self, session_id, prompt):
#         self.start_conversation(session_id)
#         self.add_message(session_id, "user", prompt)
#         tools = config_toolcall.tools
#         try:
#             # Ensure that messages have the required role field
#             messages = self.conversations[session_id]
#             for message in messages:
#                 if 'role' not in message:
#                     logger.error(f"Missing 'role' in message: {message}")
#                     return "Error: Missing 'role' in message."

#             response = client.chat.completions.create(
#                 model=self.engine,
#                 messages=messages,
#                 tools=tools,
#                 tool_choice="auto"
#             )

#             # Log the entire response for debugging
#             logger.info(f"API response: {response}")

#             # Extract the response message
#             response_message = response.choices[0].message

#             self.add_message(session_id, "assistant", response_message.content)

#             # Handle tool calls if any
#             tool_calls = response_message.tool_calls
#             if tool_calls:
#                 available_functions = {
#                     "consumer_details": self.consumer_details,
#                     "power_cut": self.power_cut,
#                     "monthly_data": self.monthly_data,
#                     "daily_data": self.daily_data,
#                     "notifiation": self.notifiation,
#                     "balance_recharge": self.balance_recharge,
#                     "consumption": self.consumption,
#                     "site_details": self.site_details,
#                     "costumer_support": self.costumer_support,
#                 }
#                 for tool_call in tool_calls:
#                     function_name = tool_call.function.name
#                     function_to_call = available_functions.get(function_name)
#                     if function_to_call:
#                         function_response = function_to_call()
#                         if function_response is not None:
#                             self.conversations[session_id].append(
#                                 {
#                                     "role": "assistant",
#                                     "content": json.dumps({
#                                         "tool_call_id": tool_call.id,
#                                         "name": function_name,
#                                         "response": function_response,
#                                     })
#                                 }
#                             )
#                             logger.info(function_response)
#                         else:
#                             logger.info(f"Function {function_name} returned None")
#                     else:
#                         logger.info(f"No function found for tool_call: {function_name}")
                
#                 # Generate a second response if tool calls were present
#                 second_response = client.chat.completions.create(
#                     model=self.engine,
#                     messages=self.conversations[session_id]
#                 )
#                 assistant_response = second_response.choices[0].message.content
#                 self.add_message(session_id, "assistant", assistant_response)
#                 return assistant_response

#             return response_message.content

#         except Exception as e:
#             logger.error(f'Error Generating Response: {e}')
#             return None

import os
import json
import logging
import requests
from dotenv import load_dotenv
from openai import OpenAI
import chatbot_prompt
import config_toolcall

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logger = logging.getLogger(__name__)
logging.basicConfig(filename='chatbot.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')

class OpenAIBot:
    def __init__(self, engine):
        self.conversations = {}  # Stores conversations by session ID
        self.engine = engine

    def start_conversation(self, session_id):
        if session_id not in self.conversations:
            self.conversations[session_id] = chatbot_prompt.prompt.copy()  # Initialize conversation with a system message
            logger.info(f"Started new conversation with session_id: {session_id}")
        else:
            self.conversations[session_id] = chatbot_prompt.prompt.copy()

    def add_message(self, session_id, role, content):
        if content:
            self.conversations[session_id].append({"role": role, "content": content})
        else:
            logger.info(f"Attempted to add a message with null content for role {role} in session {session_id}")

    def save_conversation(self, filename, session_id):
        try:
            with open(filename, 'w') as file:
                json.dump({session_id: self.conversations[session_id]}, file, indent=4)
            logger.info(f"Conversation saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")

    def login_api(self):
        try:
            import config
            # url = os.getenv("LOGIN_API")
            url = config.login_api
            logger.info(url)
            logger.info("login_api called")
            response = requests.get(url)
            response.raise_for_status()
            logger.info("login_api success")
            return response.json().get('resource')
        except requests.RequestException as e:
            logger.error(f"Error fetching login API: {e}")
            return None

    def fetch_data(self, keys_to_fetch):
        try:
            data = self.login_api()
            if data:
                return {key: data.get(key) for key in keys_to_fetch}
            else:
                logger.error("No data returned from login API")
                return {}
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return {}

    def consumer_details(self):
        keys_to_fetch = ['location_id', "flat_number", 'consumer_name', "consumer_mobile_no", "consumer_email_id", "balance_amount"]
        details = self.fetch_data(keys_to_fetch)
        if details:
            details["login_id"] = details.pop("location_id", None)
            logger.info("consumer_details success")
        return details

    def notifiation(self):
        keys_to_fetch = ['notification_email', 'notification_sms', 'notification_ivrs', 'notification_app_load', 'notification_app_balance', 'low_bal_alert', 'notification_app_esource', 'notification_app_unit_consumption', 'alert_daily_consumption_grid', 'alert_daily_consumption_dg', 'power_cut_restore_notification', 'recharge_notification', 'last_reading_alert_notification']
        return self.fetch_data(keys_to_fetch)

    def balance_recharge(self):
        keys_to_fetch = ['balance_amount', 'last_recharge_time', 'last_coupon_amount']
        return self.fetch_data(keys_to_fetch)

    def consumption(self):
        keys_to_fetch = ['dg_reading', 'grid_reading', 'last_reading_updated', 'daily_dg_unit', 'daily_grid_unit', 'monthly_dg_unit', 'monthly_grid_unit', 'daily_dg_amount', 'daily_grid_amount', 'fix_charges_monthly', 'monthly_dg_amount', 'monthly_grid_amount', 'fix_charges', 'energy_source', 'last_reading_updated_dg']
        return self.fetch_data(keys_to_fetch)

    def site_details(self):
        keys_to_fetch = ['site_id', 'site_name', 'site_address', 'site_city', 'site_state', 'site_country', 'site_zipcode', 'site_supervisor_name']
        return self.fetch_data(keys_to_fetch)

    def costumer_support(self):
        keys_to_fetch = ['site_supervisor_name', 'site_supervisor_contact_no', 'site_supervisor_email_id', 'site_support_concern_name', 'site_support_contact_no', 'site_support_email_id']
        return self.fetch_data(keys_to_fetch)

    def daily_data(self):
        try:
            import config
            url = config.daily_api
            # url = os.getenv("DAILY_API")
            response = requests.get(url)
            response.raise_for_status()
            logger.info("daily data fetched")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching daily data: {e}")
            return None

    def monthly_data(self):
        try:
            import config
            # url = os.getenv("MONTHLY_API")
            url = config.monthly_api
            response = requests.get(url)
            response.raise_for_status()
            logger.info("monthly data fetched")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching monthly data: {e}")
            return None

    def power_cut(self):
        data = self.login_api()
        if data:
            values = {}
            try:
                if float(data.get('balance_amount', 0)) < 0:
                    values['balance'] = data['balance_amount']
                if data.get('overload_grid', "").lower() == "y":
                    values["overload_grid"] = data['overload_grid']
                if data.get('overload_dg', "").lower() == "y":
                    values["overload_dg"] = data['overload_dg']
                logger.info(values)
                return values
            except ValueError as e:
                logger.error(f"Error processing power cut data: {e}")
                return values
        else:
            logger.error("No data returned from login API for power cut")
            return {}

    def generate_response(self, session_id, prompt):
        self.start_conversation(session_id)
        self.add_message(session_id, "user", prompt)
        tools = config_toolcall.tools
        try:
            # Ensure that messages have the required role field
            messages = self.conversations[session_id]
            for message in messages:
                if 'role' not in message:
                    logger.error(f"Missing 'role' in message: {message}")
                    return "Error: Missing 'role' in message."

            # Determine if user query is broad and prompt for specifics
            broad_queries = ["current", "details", "information","electricity"]
            if any(broad_query in prompt.lower() for broad_query in broad_queries):
                prompt_for_specifics = (
                    "Please specify the information you are looking for:\n"
                    # "1. Consumer Details\n"
                    # "2. Balance Information\n"
                    # "3. Electricity Consumption\n"
                    # "4. Notifications\n"
                    # "5. Site Details\n"
                    # "6. Customer Support\n"
                    # "7. Daily Data\n"
                    # "8. Monthly Data\n"
                    # "9. Power Cut Details"
                )
                self.add_message(session_id, "assistant", prompt_for_specifics)
                return prompt_for_specifics

            response = client.chat.completions.create(
                model=self.engine,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            # Log the entire response for debugging
            # logger.info(f"API response: {response}")
            # Extract the response message
            response_message = response.choices[0].message
            logger.info(f"response message: {response_message}")

            # print("done1")
            # Clean up the response to avoid unwanted formatting
            # cleaned_response = response_message.content.replace("\\", "").replace("*", "")
            # print("done2")

            self.add_message(session_id, "assistant", response_message.content)
            # print(response_message)
            # Handle tool calls if any
            tool_calls = response_message.tool_calls
            if tool_calls:
                # print(4)
                available_functions = {
                    "consumer_details": self.consumer_details,
                    "power_cut": self.power_cut,
                    "monthly_data": self.monthly_data,
                    "daily_data": self.daily_data,
                    "notifiation": self.notifiation,
                    "balance_recharge": self.balance_recharge,
                    "consumption": self.consumption,
                    "site_details": self.site_details,
                    "costumer_support": self.costumer_support,
                }
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions.get(function_name)
                    # print(5, function_name)
                    if function_to_call:
                        function_response = function_to_call()
                        # print(6 , function_response)
                        if function_response:
                            # print(7)
                            self.conversations[session_id].append(
                                {
                                    "role": "assistant",
                                    "content": json.dumps({
                                        "tool_call_id": tool_call.id,
                                        "name": function_name,
                                        "response": function_response,
                                    })
                                }
                            )
                            logger.info("function response",function_response)
                        else:
                            logger.info(f"Function {function_name} returned None")
                    else:
                        logger.info(f"No function found for tool_call: {function_name}")
                # print("function response",function_response)
                # print("conver:", self.conversations[session_id])
                # Generate a second response if tool calls were present
                second_response = client.chat.completions.create(
                    model=self.engine,
                    messages=self.conversations[session_id]
                )
                # print("second_response",second_response)
                assistant_response = second_response.choices[0].message.content

                # Clean up the second response
                cleaned_second_response = assistant_response.replace("\\", "").replace("*", "").replace("###", "")

                self.add_message(session_id, "assistant", cleaned_second_response)
                return cleaned_second_response

            return response_message.content.replace("\\", "").replace("*", "").replace("###", "")

        except Exception as e:
            logger.error(f'Error Generating Response: {e}')
            return " there is as issue with output"
