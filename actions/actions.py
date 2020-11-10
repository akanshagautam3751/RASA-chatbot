# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

total_rooms, type_room = None, None


class ActionBookRoom(Action):
    def name(self) -> Text:
        return "action_book_room_request"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global total_rooms
        global type_room
        total_rooms, type_room = None, None

        dispatcher.utter_message(text="How many rooms would you like to book?")
        return []


class ActionNumberOfRooms(Action):
    def name(self) -> Text:
        return "action_number_of_rooms"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'num_rooms':
                global total_rooms
                total_rooms = e['value']

        print("Total number of rooms: ", total_rooms)
        dispatcher.utter_message(
            text="What type of room would you want to book? Button1 - Simple; Button 2 - Deluxe")
        return []


class ActionTypeOfRoom(Action):
    def name(self) -> Text:
        return "action_type_room"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        print(entities)
        r_t = None

        for e in entities:
            if e['entity'] == 'room_type':
                global type_room
                type_room = e['value']

            if type_room == '1':
                r_t = 'Simple'
                message = "You have chosen to book " + total_rooms + " " + r_t + " rooms"
            elif type_room == '2':
                r_t = 'Deluxe'
                message = "You have chosen to book " + total_rooms + " " + r_t + " rooms"
            else:
                message = "Please click correct buttons. Press Button 1 for Simple room(s) and Button 2 for Deluxe room(s)"

        print("Room(s) type: ", r_t)

        dispatcher.utter_message(
            text=message)
        return []


class ActionScheduleClearningRelativeTime(Action):
    def name(self) -> Text:
        return "action_schedule_cleaning_relative_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        print(entities)
        current_time = datetime.datetime.now()
        fetch_time = ''

        for e in entities:
            if e['entity'] == 'schedule_time':
                fetch_time = e['value']

        time = current_time.hour + int(fetch_time)
        print("Time: ", time)
        am_or_pm = ''

        if time > 12:
            time = time-12
            am_or_pm = 'pm'
        else:
            am_or_pm = 'am'

        dispatcher.utter_message(
            text="Sure, I have scheduled a cleaning for " + str(time) + " " + am_or_pm + " today")
        return []
