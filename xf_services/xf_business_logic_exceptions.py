class XFBusinessLogicExceptionBase(Exception):
    pass


class XFBusinessRuleViolationException(XFBusinessLogicExceptionBase):
    pass


class XFPermissionDefinedException(XFBusinessLogicExceptionBase):
    pass


class XFInvalidModelStateException(XFBusinessLogicExceptionBase):
    pass


class XFPermissionDeniedException(XFBusinessLogicExceptionBase):
    pass

class XFSaveException(XFBusinessLogicExceptionBase):
    pass