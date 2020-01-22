# Manage Mac OS NotificationCenter preferences

This tool will parse your users NotificationCenter preferences and disable „Show notifications on lock screen“ for all non-system apps.

## Usage

```
% ./main.py 
Change for: com.apple.iCal
Change for: com.apple.FaceTime
Change for: com.apple.mail
Change for: com.apple.iChat
Change for: com.apple.Safari
Change for: com.apple.gamecenter
Change for: com.apple.iBooksX
Change for: com.apple.Notes

Import new preferences with:
	defaults import com.apple.ncprefs - < /Users/jan/Desktop/com.apple.ncprefs.plist

Finally execute to reload:
	killall NotificationCenter && killall usernoted
```
