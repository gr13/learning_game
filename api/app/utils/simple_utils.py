from api.app.utils.utils_temp import Utils


class SimpleUtils(Utils):
    def create_new_chat(self):
        system_prompt = "You are a German tutor."
        user_prompt = ""

        # Fresh conversation:
        # Only system + user are sent
        # No previous messages reused

        response = self.chat.send_message(system_prompt, user_prompt)

        return response
