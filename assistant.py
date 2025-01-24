from modules.speech import SpeechHandler
from modules.commands import BasicCommands
from modules.notepad import NotepadHandler
from modules.weather import WeatherHandler
from modules.ai_query import AIQueryHandler
from modules.phone_display import PhoneDisplayHandler
from modules.utils import find_application
import subprocess

class AIAssistant:
    def __init__(self, window):
        self.window = window
        self.api_key = "your_api_key"  # Replace with your Hugging Face API key
        self.weather_api_key = "f9509fb5a6f0ffa45ca90b659d12eea5"  # Replace with your OpenWeather API key

        # Initialize handlers
        self.speech_handler = SpeechHandler()
        self.basic_commands = BasicCommands(self.speech_handler)
        self.notepad_handler = NotepadHandler(self.speech_handler)
        self.weather_handler = WeatherHandler(self.speech_handler, self.weather_api_key)
        self.ai_query_handler = AIQueryHandler(self.speech_handler, self.api_key)
        self.phone_display_handler = PhoneDisplayHandler(self.speech_handler)

    async def execute_command_async(self, command):
        if not command:
            return

        print(f"Executing: {command}")

        try:
            # Notepad-related commands
            if 'open notepad' in command:
                await self.notepad_handler.start_notepad_dictation()

            elif self.notepad_handler.is_dictating and any(word in command for word in ['save', 'save file', 'save it']):
                await self.notepad_handler.save_notepad_file()

            elif self.notepad_handler.is_dictating:
                # Handle special Notepad actions
                if 'add space' in command:
                    await self.notepad_handler.add_space()
                elif 'new line' in command or 'add line' in command:
                    await self.notepad_handler.add_new_line()
                elif 'add tab' in command or 'tab' in command:
                    await self.notepad_handler.add_tab()
                elif 'delete last character' in command or 'undo character' in command:
                    await self.notepad_handler.delete_last_character()
                elif 'clear notepad' in command or 'delete all' in command:
                    await self.notepad_handler.clear_notepad()
                elif 'go back' in command:
                    await self.notepad_handler.go_back()
                elif 'go next' in command:
                    await self.notepad_handler.go_next()
                else:
                    # Write regular text to Notepad
                    await self.notepad_handler.write_to_notepad(command)

            # Open applications
            elif 'open' in command:
                app_name = command.replace('open', '').strip().lower()
                app_path = find_application(app_name)
                if app_path:
                    subprocess.Popen([app_path])
                    self.speech_handler.speak(f"Opening {app_name}.")
                else:
                    self.speech_handler.speak(f"Sorry, I couldn't find an application named {app_name}.")

            # Web search
            elif "search for" in command:
                search_query = command.replace("search for", "").strip()
                if search_query:
                    subprocess.run(["start", f"https://www.google.com/search?q={search_query}"], shell=True)
                    self.speech_handler.speak(f"Searching for {search_query}.")
                else:
                    self.speech_handler.speak("Please specify what you'd like me to search for.")

            # Basic commands
            elif 'what time is it' in command or 'what is the date' in command or 'tell me a joke' in command:
                await self.basic_commands.execute_command(command)

            # Weather-related commands
            elif 'what\'s the weather' in command:
                await self.weather_handler.get_weather_async()

            # AI query commands
            elif any(keyword in command for keyword in ['explain', 'what is', 'who is', 'tell me about']):
                await self.ai_query_handler.process_ai_query(command)

            # Phone display commands
            elif 'display my phone' in command:
                await self.phone_display_handler.display_phone()

            elif 'stop display' in command:
                self.phone_display_handler.stop_display()

            # Unknown commands
            else:
                self.speech_handler.speak("Sorry, I don't understand that command.")

        except Exception as e:
            print(f"Command execution error: {e}")
            self.speech_handler.speak("Sorry, there was an error executing that command.")
