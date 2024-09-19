import enum
import os
from typing import Annotated
from livekit.agents import llm
import logging
import wikipedia
import webbrowser
import subprocess

logger = logging.getLogger("tempreature-control")
logger.setLevel(logging.INFO)


class Zone(enum.Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"


class AssistantFnc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()

        self._tempreature = {
            Zone.LIVING_ROOM: 23,
            Zone.BEDROOM: 23,
            Zone.KITCHEN: 23,
            Zone.BATHROOM: 23,
            Zone.OFFICE: 23,
        }

    @llm.ai_callable(description="get the tempreature in a specific room")
    def get_tempreature(self, zone: Annotated[Zone, llm.TypeInfo(description="The specific Zone")]):
        logger.info("get temp -zone %s", zone)
        temp = self._tempreature[Zone(zone)]
        return f"The tempreature in the {zone} is {temp} C"

    @llm.ai_callable(description="set the tempreature in a specific room")
    def set_tempreature(self, zone: Annotated[Zone, llm.TypeInfo(description="The specific Zone")], temp: Annotated[int, llm.TypeInfo(description="The tempreature in C")]):
        logger.info("set temp -zone %s, temp %s", zone, temp)
        self._tempreature[Zone(zone)] = temp
        return f"The tempreature in the {zone} is set to {temp} C"

    @llm.ai_callable(description="check Wikipedia and give a short summary about any topic")
    def check_wikipedia(self, topic: Annotated[str, llm.TypeInfo(description="The topic to search on Wikipedia")]):
        logger.info("Checking Wikipedia for topic: %s", topic)
        try:
            summary = wikipedia.summary(topic, sentences=3)
            return f"Summary for {topic}: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Topic {topic} is ambiguous, possible options: {e.options}"
        except wikipedia.exceptions.PageError:
            return f"Topic {topic} not found on Wikipedia"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @llm.ai_callable(description="open the YouTube website")
    def open_youtube(self):
        logger.info("Opening YouTube website")
        try:
            webbrowser.open("https://www.youtube.com")
            return "YouTube website opened successfully"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @llm.ai_callable(description="create a new Python project and open it in Visual Studio Code")
    def create_python_project(self, folder_name: Annotated[str, llm.TypeInfo(description="The name of the new project folder")]):
        logger.info("Creating new Python project: %s", folder_name)
        base_path = "C:\\Users\\ASUS\\OneDrive\\Desktop\\Python_projects\\"
        project_path = os.path.join(base_path, folder_name)
        try:
            os.makedirs(project_path, exist_ok=True)
            subprocess.Popen(["code", project_path],  shell=True)
            return f"Cooked up the Python project '{folder_name}' and opened in Visual Studio Code"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @llm.ai_callable(description="create a new React or a web development project and open it in Visual Studio Code")
    def create_react_project(self, folder_name: Annotated[str, llm.TypeInfo(description="The name of the new project folder")]):
        logger.info("Cooking up a new React project: %s", folder_name)
        base_path = "C:\\Users\\ASUS\\OneDrive\\Desktop\\reactjs_prots\\"
        project_path = os.path.join(base_path, folder_name)
        try:
            os.makedirs(project_path, exist_ok=True)
            subprocess.Popen(["code", project_path], shell=True)
            return f"Cooked up the React project '{folder_name}'  and opened in Visual Studio Code"
        except Exception as e:
            return f"An error occurred: {str(e)}"
