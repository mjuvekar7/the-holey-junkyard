"""Common exceptions."""

class IPStopped(BaseException):
    """IP has been stopped."""

class IPQuitted(BaseException):
    """Program terminated."""

    def __init__(self, exitcode=0):
        BaseException.__init__(self, exitcode)

    @property
    def exitcode(self):
        return self.args[0]

