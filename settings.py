import json
import logging

logger = logging.getLogger()


class Settings:
    def __init__(self, filename='settings.json'):
        self._filename = filename
        self._setting = self._load_setting()
        logger.info("Settings file loaded")

    @property
    def setting(self):
        return self._setting

    def update_or_insert(self, field_name, value):
        if self._setting.get(field_name) is None:
            self._setting.update({field_name: int(value)})
        else:
            self._setting[field_name] = int(value)

    def read(self, field_name):
        return int(self._setting.get(field_name, 0))

    def write(self):
        with open(self._filename, 'w') as setting:
            json.dump(self._setting, setting, sort_keys=True, indent=4)
        print("New setting successfully saved")

    def _load_setting(self):
        try:
            with open(self._filename) as setting:
                logger.debug("Opening ", self._filename)
                return json.load(setting)
        except FileNotFoundError:
            logger.info(self._filename, " not found, creating new file")
            with open(self._filename, "w+") as setting:
                setting.write("{}".format("{\"test\":1}"))
        except json.JSONDecodeError:
            with open(self._filename, "w+") as setting:
                setting.write("{}".format("{\"test\":1}"))
        self._load_setting()
