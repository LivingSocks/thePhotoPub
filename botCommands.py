import fchat

from datetime import datetime

class EchoBot(fchat.FChatClient):
    log_filter = ["PIN", "NLN", "FLN", "LIS", "STA", "VAR", "HLO", "CON", "FRL", "IGN", "ADL", "TPN", "LRP"]

    def CUB(self, channel, character):
        character = character.lower()
        with open("report.json", "r+", encoding="utf-8") as file:
            report = json.load(file)
            profile = []
            for key in report.keys():
                profile.append(key)
            if character in profile:
                del report[character]
            file.seek(0)
            file.write(json.dumps(report, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()

    def on_CTU(self, operator, channel, length, character):
        character = character.lower()
        if channel == "ADH-b2a35a8f84b81b45834a":
            channel = "The Photo Pub"
        with open("report.json", "r+", encoding="utf-8") as file:
            report = json.load(file)
            profile = report.keys()
            if charcter not in profile:
                timeout = {}
                timeout[character] = {
                    "moderator": operator,
                    "action": "timeout",
                    "room": channel,
                    "length (in minutes)": length,
                    "date/time": now.strftime("%m/%d/%Y, %H:%M:%S"),
                    "reason": "Not Given"
                    }
                report.append(timeout)
            else:
                report[character]["action"] = "timeout"
            file.seek(0)
            file.write(json.dumps(report, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()



    def on_CKU(self, operator, channel, character):
        character = character.lower()
        if channel == "ADH-b2a35a8f84b81b45834a":
            channel = "The Photo Pub"
        with open("report.json", "r+", encoding="utf-8") as file:
            report = json.load(file)
            profile = report.keys()
            if character not in profile:
                kick = {}
                kick[character] = {
                    "moderator": operator,
                    "action": "kicked",
                    "room": channel,
                    "date/time": now.strftime("%m/%d/%Y, %H:%M:%S"),
                    "reason": "Not Given"
                    }
                report.append(kick)
            else:
                report[character]["action"] = "kicked"
            file.seek(0)
            file.write(json.dumps(report, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()


    def on_CBU(self, operator, channel, character):
        character = character.lower()
        if channel == "ADH-b2a35a8f84b81b45834a":
            channel = "The Photo Pub"
        with open("report.json", "r+", encoding="utf-8") as file:
            report = json.load(file)
            profile = report.keys()
            if character not in profile:
                banned = {}
                banned[character] = {
                    "moderator": operator,
                    "action": "banned",
                    "room": channel,
                    "date/time": now.strftime("%m/%d/%Y, %H:%M:%S"),
                    "reason": "Not Given"
                    }
                report.append(banned)
            else:
                report[character]["action"] = "banned"
            file.seek(0)
            file.write(json.dumps(report, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()

    # function dedicated to sending public messages to the chatroom
    def on_MSG(self, character, message, channel):
        super().on_MSG(character, message, channel)

        # open room.json and store that information in 'room' variable
        file = open("room.json", "r", encoding="utf-8")
        room = json.load(file)
        file.close()

        # open moderators.json and store that information in 'mods' variable
        file = open("moderators.json", "r", encoding="utf-8")
        mods = json.load(file)
        file.close()

        thePhotoPub = room['thePhotoPub']
        setWelcome = room['setWelcome']
        pubModerators = mods

        if message[:8] == "!welcome" and character in pubModerators:
            super().MSG(thePhotoPub, setWelcome)
        else:
            super().MSG(thePhotoPub,
                        '/me scans user name with database, then shakes her head. "Hmmm, nope. Doesn\'t'
                        ' check out. Sorry, only authorized personnel can use this command."')

    def on_PRI(self, character, message):
        super().on_PRI(character, message)
        # open room.json and store that information in 'room' variable
        file = open("room.json", "r", encoding="utf-8")
        room = json.load(file)
        file.close()

        # open moderators.json and store that information in 'mods' variable
        file = open("moderators.json", "r", encoding="utf-8")
        mods = json.load(file)
        file.close()

        thePhotoPub = room['thePhotoPub']
        pubModerators = mods["pubModerators"]
        myCharacters = mods["myCharacters"]

        if message[:11] == "!setwelcome" and character in myCharacters:
            with open('room.json', 'r+') as file:
                setWelcome = json.load(file)
                setWelcome['setWelcome'] = message[12:]
                file.seek(0)
                file.write(json.dumps(setWelcome, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()
            super().PRI(character, "Message Set!")

        if message[:7] == "!report" and character in pubModerators:
            words = message.split()
            if words[1].lower() != "test":
                with open("report.json", "r+", encoding="utf-8") as file:
                    report = json.load(file)
                    profile = report.keys()
                    if words[1].lower() in profile and report["reason"] == "Not Given":
                        report["reason"] = words[2]
                    elif words[1].lower() in profile and report["reason"] != "Not Given":
                        super().PRI(character, "Someone has already given a reason as to this action.")
                    else:
                        super().PRI(chracter, "That name does not exist in our records, or you did not use the command"
                                              "correctly. Please use following format: !report <profile name> <reason>")
                    file.seek(0)
                    file.write(json.dumps(report, ensure_ascii=False, indent=2))
                    file.truncate()
                    file.close()

        # --------------------------------------------------------DEVELOPER COMMANDS---------------------------------------------
        # change the description of the bar
        if message[:8] == "!descbar":
            if character in myCharacters:
                description = message[9:]
                super().CDS(thePhotoPub, description)
                super().MSG(thePhotoPub, "/warn Hey. That description tab at the top of the channel? The one no "
                                          "one bothers to look at? Yea, it's just been updated.")

file = open("credentials.json", "r", encoding="utf-8")
info = json.load(file)
file.close()

file = open("room.json", "r", encoding="utf-8")
room = json.load(file)
file.close()

website = info['website']
user = info['user']
password = info['password']
profile = info['profile']

thePhotoPub = room['thePhotoPub']

bot = EchoBot(website, user, password, profile)
bot.setup()
bot.connect()
bot.JCH(thePhotoPub)
bot.run_forever()
