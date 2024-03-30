""" Error codes used in different error messages. """


class ErrorSeverity:
    """Severity codes for errors"""
    ERROR = 1
    WARNING = 10


class ErrorContext:
    """Context this error took place in, each error potentially having multiple contexts. """
    # Use this one to display any passed in message without modification
    CUSTOM_TITLE = 'ec_title'
    FILE_NAME = 'ec_filename'
    SIDECAR_COLUMN_NAME = 'ec_sidecarColumnName'
    SIDECAR_KEY_NAME = 'ec_sidecarKeyName'
    ROW = 'ec_row'
    COLUMN = 'ec_column'
    LINE = "ec_line"
    HED_STRING = 'ec_HedString'
    SCHEMA_SECTION = 'ec_section'
    SCHEMA_TAG = 'ec_schema_tag'
    SCHEMA_ATTRIBUTE = 'ec_attribute'


class ValidationErrors:
    # General validation errors.
    CHARACTER_INVALID = 'CHARACTER_INVALID'
    COMMA_MISSING = 'COMMA_MISSING'
    DEF_EXPAND_INVALID = "DEF_EXPAND_INVALID"
    DEF_INVALID = "DEF_INVALID"
    DEFINITION_INVALID = "DEFINITION_INVALID"
    ELEMENT_DEPRECATED = "ELEMENT_DEPRECATED"
    NODE_NAME_EMPTY = 'NODE_NAME_EMPTY'
    TEMPORAL_TAG_ERROR = 'TEMPORAL_TAG_ERROR'
    PARENTHESES_MISMATCH = 'PARENTHESES_MISMATCH'
    PLACEHOLDER_INVALID = 'PLACEHOLDER_INVALID'
    REQUIRED_TAG_MISSING = 'REQUIRED_TAG_MISSING'
    SIDECAR_INVALID = 'SIDECAR_INVALID'
    SIDECAR_KEY_MISSING = 'SIDECAR_KEY_MISSING'
    STYLE_WARNING = "STYLE_WARNING"
    TAG_EMPTY = 'TAG_EMPTY'
    TAG_EXPRESSION_REPEATED = 'TAG_EXPRESSION_REPEATED'
    TAG_EXTENDED = 'TAG_EXTENDED'
    TAG_EXTENSION_INVALID = 'TAG_EXTENSION_INVALID'
    TAG_GROUP_ERROR = "TAG_GROUP_ERROR"
    TAG_INVALID = "TAG_INVALID"
    TAG_NOT_UNIQUE = 'TAG_NOT_UNIQUE'
    TAG_NAMESPACE_PREFIX_INVALID = 'TAG_NAMESPACE_PREFIX_INVALID'
    TAG_REQUIRES_CHILD = 'TAG_REQUIRES_CHILD'
    TILDES_UNSUPPORTED = 'TILDES_UNSUPPORTED'
    UNITS_INVALID = 'UNITS_INVALID'
    UNITS_MISSING = 'UNITS_MISSING'
    VERSION_DEPRECATED = 'VERSION_DEPRECATED'
    VALUE_INVALID = 'VALUE_INVALID'

    # Internal codes
    HED_DEF_UNMATCHED = "HED_DEF_UNMATCHED"
    HED_DEF_VALUE_MISSING = "HED_DEF_VALUE_MISSING"
    HED_DEF_VALUE_EXTRA = "HED_DEF_VALUE_EXTRA"

    HED_DEF_EXPAND_INVALID = "HED_DEF_EXPAND_INVALID"
    HED_DEF_EXPAND_UNMATCHED = "HED_DEF_EXPAND_UNMATCHED"
    HED_DEF_EXPAND_VALUE_MISSING = "HED_DEF_EXPAND_VALUE_MISSING"
    HED_DEF_EXPAND_VALUE_EXTRA = "HED_DEF_EXPAND_VALUE_EXTRA"

    HED_TAG_REPEATED = 'HED_TAG_REPEATED'
    HED_TAG_REPEATED_GROUP = 'HED_TAG_REPEATED_GROUP'

    INVALID_PARENT_NODE = "invalidParent"
    NO_VALID_TAG_FOUND = "invalidTag"

    HED_LIBRARY_UNMATCHED = "HED_LIBRARY_UNMATCHED"

    HED_TOP_LEVEL_TAG = "HED_TOP_LEVEL_TAG"
    HED_MULTIPLE_TOP_TAGS = "HED_MULTIPLE_TOP_TAGS"
    HED_TAG_GROUP_TAG = "HED_TAG_GROUP_TAG"

    HED_GROUP_EMPTY = 'HED_GROUP_EMPTY'
    # end internal codes

    # Still being worked on below this line
    HED_MISSING_REQUIRED_COLUMN = "HED_MISSING_REQUIRED_COLUMN"
    HED_UNKNOWN_COLUMN = "HED_UNKNOWN_COLUMN"
    SIDECAR_AND_OTHER_COLUMNS = "SIDECAR_AND_OTHER_COLUMNS"

    DUPLICATE_COLUMN_IN_LIST = "DUPLICATE_COLUMN_IN_LIST"
    DUPLICATE_COLUMN_BETWEEN_SOURCES = "DUPLICATE_COLUMN_BETWEEN_SOURCES"
    HED_BLANK_COLUMN = "HED_BLANK_COLUMN"

    # Below here shows what the given error maps to

    INVALID_TAG_CHARACTER = 'invalidTagCharacter'

    CURLY_BRACE_UNSUPPORTED_HERE = "CURLY_BRACE_UNSUPPORTED_HERE"
    ONSETS_OUT_OF_ORDER = "ONSETS_OUT_OF_ORDER"


class SidecarErrors:
    # These are for json sidecar validation errors(sidecars can also produce most normal validation errors)
    BLANK_HED_STRING = 'blankValueString'
    WRONG_HED_DATA_TYPE = 'wrongHedDataType'
    INVALID_POUND_SIGNS_VALUE = 'invalidNumberPoundSigns'
    INVALID_POUND_SIGNS_CATEGORY = 'tooManyPoundSigns'
    UNKNOWN_COLUMN_TYPE = 'sidecarUnknownColumn'
    SIDECAR_HED_USED_COLUMN = 'SIDECAR_HED_USED_COLUMN'
    SIDECAR_NA_USED = 'SIDECAR_NA_USED'
    SIDECAR_HED_USED = 'SIDECAR_HED_USED'
    SIDECAR_BRACES_INVALID = "SIDECAR_BRACES_INVALID"


class SchemaErrors:
    SCHEMA_DUPLICATE_NODE = 'SCHEMA_DUPLICATE_NODE'

    SCHEMA_DUPLICATE_FROM_LIBRARY = "SCHEMA_LIBRARY_INVALID"


class SchemaWarnings:
    SCHEMA_INVALID_CHARACTERS_IN_DESC = "SCHEMA_INVALID_CHARACTERS_IN_DESC"
    SCHEMA_INVALID_CHARACTERS_IN_TAG = "SCHEMA_INVALID_CHARACTERS_IN_TAG"

    # The actual reported error for the above two
    SCHEMA_CHARACTER_INVALID = "SCHEMA_CHARACTER_INVALID"
    SCHEMA_INVALID_CAPITALIZATION = 'invalidCaps'
    SCHEMA_NON_PLACEHOLDER_HAS_CLASS = 'SCHEMA_NON_PLACEHOLDER_HAS_CLASS'
    SCHEMA_PROLOGUE_CHARACTER_INVALID = "SCHEMA_PROLOGUE_CHARACTER_INVALID"


class SchemaAttributeErrors:
    SCHEMA_ATTRIBUTE_INVALID = 'SCHEMA_ATTRIBUTE_INVALID'
    SCHEMA_ATTRIBUTE_VALUE_INVALID = 'SCHEMA_ATTRIBUTE_VALUE_INVALID'
    SCHEMA_DEPRECATION_ERROR = 'SCHEMA_DEPRECATION_ERROR'
    SCHEMA_DEPRECATED_INVALID = "SCHEMA_DEPRECATED_INVALID"
    SCHEMA_CHILD_OF_DEPRECATED = "SCHEMA_CHILD_OF_DEPRECATED"
    SCHEMA_ATTRIBUTE_VALUE_DEPRECATED = "SCHEMA_ATTRIBUTE_VALUE_DEPRECATED"
    SCHEMA_SUGGESTED_TAG_INVALID = "SCHEMA_SUGGESTED_TAG_INVALID"

    SCHEMA_UNIT_CLASS_INVALID = "SCHEMA_UNIT_CLASS_INVALID"
    SCHEMA_VALUE_CLASS_INVALID = "SCHEMA_VALUE_CLASS_INVALID"
    SCHEMA_ALLOWED_CHARACTERS_INVALID = "SCHEMA_ALLOWED_CHARACTERS_INVALID"
    SCHEMA_IN_LIBRARY_INVALID = "SCHEMA_IN_LIBRARY_INVALID"

    SCHEMA_DEFAULT_UNITS_INVALID = "SCHEMA_DEFAULT_UNITS_INVALID"
    SCHEMA_DEFAULT_UNITS_DEPRECATED = "SCHEMA_DEFAULT_UNITS_DEPRECATED"
    SCHEMA_CONVERSION_FACTOR_NOT_POSITIVE = "SCHEMA_CONVERSION_FACTOR_NOT_POSITIVE"


class DefinitionErrors:
    # These are all DEFINITION_INVALID errors
    WRONG_NUMBER_PLACEHOLDER_TAGS = 'wrongNumberPlaceholderTags'
    DUPLICATE_DEFINITION = 'duplicateDefinition'
    INVALID_DEFINITION_EXTENSION = 'invalidDefExtension'
    DEF_TAG_IN_DEFINITION = 'DEF_TAG_IN_DEFINITION'
    NO_DEFINITION_CONTENTS = "NO_DEFINITION_CONTENTS"
    PLACEHOLDER_NO_TAKES_VALUE = 'PLACEHOLDER_NO_TAKES_VALUE'

    WRONG_NUMBER_TAGS = 'WRONG_NUMBER_TAGS'
    WRONG_NUMBER_GROUPS = 'WRONG_NUMBER_GROUPS'
    BAD_PROP_IN_DEFINITION = 'BAD_PROP_IN_DEFINITION'

    BAD_DEFINITION_LOCATION = 'BAD_DEFINITION_LOCATION'


class TemporalErrors:
    # These are all TEMPORAL_TAG_ERROR
    OFFSET_BEFORE_ONSET = "OFFSET_BEFORE_ONSET"
    ONSET_DEF_UNMATCHED = "ONSET_DEF_UNMATCHED"
    ONSET_WRONG_NUMBER_GROUPS = "ONSET_WRONG_NUMBER_GROUPS"
    ONSET_NO_DEF_TAG_FOUND = "ONSET_NO_DEF_TAG_FOUND"
    ONSET_PLACEHOLDER_WRONG = "ONSET_PLACEHOLDER_WRONG"
    ONSET_TOO_MANY_DEFS = "ONSET_TOO_MANY_DEFS"
    ONSET_TAG_OUTSIDE_OF_GROUP = "ONSET_TAG_OUTSIDE_OF_GROUP"
    INSET_BEFORE_ONSET = "INSET_BEFORE_ONSET"
    ONSET_SAME_DEFS_ONE_ROW = "ONSET_SAME_DEFS_ONE_ROW"
    HED_ONSET_WITH_NO_COLUMN = 'HED_ONSET_WITH_NO_COLUMN'

    DURATION_HAS_OTHER_TAGS = "DURATION_HAS_OTHER_TAGS"
    DURATION_WRONG_NUMBER_GROUPS = "DURATION_WRONG_NUMBER_GROUPS"


class ColumnErrors:
    INVALID_COLUMN_REF = "INVALID_COLUMN_REF"
    SELF_COLUMN_REF = "SELF_COLUMN_REF"
    NESTED_COLUMN_REF = "NESTED_COLUMN_REF"
    MALFORMED_COLUMN_REF = "MALFORMED_COLUMN_REF"
