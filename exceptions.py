class WotMapExtractorError(Exception):
    pass


class XmlUnpackerError(WotMapExtractorError):
    pass


class PackageReaderError(WotMapExtractorError):
    pass


class StringUtilsError(WotMapExtractorError):
    pass
