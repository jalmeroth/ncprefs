#!/usr/bin/env python3
"""Read/Modify NotificationCenter Preferences."""
import logging
import plistlib
from os.path import expanduser

logging.basicConfig()
_LOGGER = logging.getLogger(__name__)
# _LOGGER.setLevel(logging.DEBUG)

DEFAULTS_DOMAIN = "com.apple.ncprefs"
USER_DESKTOP = "~/Desktop/{}.plist"
USER_PREFS = "~/Library/Preferences/{}.plist"
SYSTEM_CENTER = "_SYSTEM_CENTER_"


class NotificationSettings(object):
    """Represent Notification Settings."""

    def __init__(self, flags):
        """Initialize object."""
        _LOGGER.debug("Flags: {}".format(flags))
        self.flags = flags

    def get_flag(self, shift):
        """Return True/False depending on shift."""
        return False if self.flags & 1 << shift else True

    def set_flag(self, flag, shift):
        """Set Flag to True."""
        _LOGGER.debug("set_flag: {}/{}".format(flag, shift))
        _LOGGER.debug("Flags before: {}".format(self.flags))
        if flag:  # enable
            self.flags &= ~(1 << shift)
        else:  # disable
            self.flags |= 1 << shift
        _LOGGER.debug("Flags after: {}".format(self.flags))

    @property
    def show_on_lockscreen(self):
        """Return show_on_lockscreen setting."""
        return self.get_flag(12)

    @show_on_lockscreen.setter
    def show_on_lockscreen(self, flag):
        self.set_flag(flag, 12)


def without_keys(d, keys):
    """Return dict without keys."""
    return {k: v for k, v in d.items() if k not in keys}


def main():
    """Provide main routine."""
    with open(expanduser(USER_PREFS.format(DEFAULTS_DOMAIN)), "rb") as plist:
        data = plistlib.load(plist)

    new_data = without_keys(data, "apps")
    new_data["apps"] = []
    has_changes = False

    for app in data["apps"]:
        # ignore System's applications
        if not app["bundle-id"].startswith(SYSTEM_CENTER):
            _LOGGER.debug("bundle-id: {}".format(app["bundle-id"]))
            app_prefs = NotificationSettings(app.get("flags", 0))

            if app_prefs.show_on_lockscreen:
                has_changes = True
                print("Change for: {}".format(app["bundle-id"]))
                app_prefs.show_on_lockscreen = False

            app["flags"] = app_prefs.flags
        new_data["apps"].append(app)

    if has_changes:
        with open(expanduser(USER_DESKTOP.format(DEFAULTS_DOMAIN)), "wb") as plist:
            plistlib.dump(new_data, plist)

        print(
            "\nImport new preferences with:\n"
            "\tdefaults import com.apple.ncprefs - < {}\n\n"
            "Finally execute to reload:\n"
            "\tkillall NotificationCenter && killall usernoted".format(
                expanduser(USER_DESKTOP.format(DEFAULTS_DOMAIN))
            )
        )
    else:
        print("No changes - all good")


if __name__ == "__main__":
    main()
