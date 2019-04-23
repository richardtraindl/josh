
from .. engine2.match import cMatch
from .. engine2.helper import reverse_lookup


def fmttime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hour, minutes = divmod(minutes, 60)
    return "%02d:%02d:%02d" % (hour, minutes, seconds)


def mapstatus(status):
    mstatus = reverse_lookup(cMatch.STATUS, status)
    if(mstatus is not None):
        return mstatus
    else:
        if(STATUS['paused'] == status):
            return "paused"
        elif(STATUS['setup'] == status):
            return "setup"
        else:
            return "?"

