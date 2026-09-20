"""
Domain-Specific Verification Exceptions
"""
class VerificationPlatformException(Exception):
    pass

class PluginNotFoundException(VerificationPlatformException):
    pass

class DatasetResolutionException(VerificationPlatformException):
    pass

class EvidenceTamperException(VerificationPlatformException):
    pass

class QualityGateFailureException(VerificationPlatformException):
    pass

class CertificationRevokedException(VerificationPlatformException):
    pass
