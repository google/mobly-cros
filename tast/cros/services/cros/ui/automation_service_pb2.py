# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tast/cros/services/cros/ui/automation_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'tast/cros/services/cros/ui/automation_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3tast/cros/services/cros/ui/automation_service.proto\x12\x0ctast.cros.ui\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1egoogle/protobuf/duration.proto\"8\n\x10LeftClickRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\"j\n\x11MousePressRequest\x12/\n\x0cmouse_button\x18\x01 \x01(\x0e\x32\x19.tast.cros.ui.MouseButton\x12$\n\x06\x66inder\x18\x02 \x01(\x0b\x32\x14.tast.cros.ui.Finder\"O\n\x12MouseMoveToRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\x12\x13\n\x0b\x64uration_ms\x18\x02 \x01(\x03\"F\n\x13MouseReleaseRequest\x12/\n\x0cmouse_button\x18\x01 \x01(\x0e\x32\x19.tast.cros.ui.MouseButton\"9\n\x11RightClickRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\":\n\x12\x44oubleClickRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\":\n\x12IsNodeFoundRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\"$\n\x13IsNodeFoundResponse\x12\r\n\x05\x66ound\x18\x01 \x01(\x08\"n\n\x1bMouseClickAtLocationRequest\x12+\n\nclick_type\x18\x01 \x01(\x0e\x32\x17.tast.cros.ui.ClickType\x12\"\n\x05point\x18\x02 \x01(\x0b\x32\x13.tast.cros.ui.Point\"<\n\x14\x45nsureFocusedRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\"\\\n\x1cWaitUntilCheckedStateRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\x12\x16\n\x0e\x65xpected_state\x18\x02 \x01(\x08\"j\n\x16WaitUntilExistsRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\x12*\n\x07timeout\x18\x02 \x01(\x0b\x32\x19.google.protobuf.Duration\"h\n\x14WaitUntilGoneRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\x12*\n\x07timeout\x18\x02 \x01(\x0b\x32\x19.google.protobuf.Duration\"v\n\x11\x45nsureGoneRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\x12/\n\x07timeout\x18\x02 \x01(\x0b\x32\x19.google.protobuf.DurationH\x00\x88\x01\x01\x42\n\n\x08_timeout\"3\n\x0bInfoRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\"9\n\x0cInfoResponse\x12)\n\tnode_info\x18\x01 \x01(\x0b\x32\x16.tast.cros.ui.NodeInfo\":\n\x12MakeVisibleRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\">\n\x16WaitForLocationRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\"P\n\x18\x43\x61ptureScreenshotRequest\x12)\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.FinderH\x00\x88\x01\x01\x42\t\n\x07_finder\"/\n\x19\x43\x61ptureScreenshotResponse\x12\x12\n\npng_base64\x18\x01 \x01(\x0c\"\x12\n\x10GetUITreeRequest\"$\n\x11GetUITreeResponse\x12\x0f\n\x07ui_tree\x18\x01 \x01(\t\"\x18\n\x16ResetAutomationRequest\"X\n\x1bSelectDropDownOptionRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\x12\x13\n\x0boption_name\x18\x02 \x01(\t\"8\n\x10\x44oDefaultRequest\x12$\n\x06\x66inder\x18\x01 \x01(\x0b\x32\x14.tast.cros.ui.Finder\"\xb7\x03\n\x08NodeInfo\x12&\n\x07\x63hecked\x18\x01 \x01(\x0e\x32\x15.tast.cros.ui.Checked\x12\x12\n\nclass_name\x18\x02 \x01(\t\x12\x43\n\x0fhtml_attributes\x18\x03 \x03(\x0b\x32*.tast.cros.ui.NodeInfo.HtmlAttributesEntry\x12$\n\x08location\x18\x04 \x01(\x0b\x32\x12.tast.cros.ui.Rect\x12\x0c\n\x04name\x18\x05 \x01(\t\x12.\n\x0brestriction\x18\x06 \x01(\x0e\x32\x19.tast.cros.ui.Restriction\x12 \n\x04role\x18\x07 \x01(\x0e\x32\x12.tast.cros.ui.Role\x12\x30\n\x05state\x18\x08 \x03(\x0b\x32!.tast.cros.ui.NodeInfo.StateEntry\x12\r\n\x05value\x18\t \x01(\t\x1a\x35\n\x13HtmlAttributesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a,\n\nStateEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x08:\x02\x38\x01\"4\n\x06\x46inder\x12*\n\nnode_withs\x18\x01 \x03(\x0b\x32\x16.tast.cros.ui.NodeWith\"\xd0\x06\n\x08NodeWith\x12\x13\n\thas_class\x18\x01 \x01(\tH\x00\x12\x0e\n\x04name\x18\x02 \x01(\tH\x00\x12\"\n\x04role\x18\x03 \x01(\x0e\x32\x12.tast.cros.ui.RoleH\x00\x12\r\n\x03nth\x18\x04 \x01(\x05H\x00\x12\x1c\n\x12\x61utofill_available\x18\x05 \x01(\x08H\x00\x12\x13\n\tcollapsed\x18\x06 \x01(\x08H\x00\x12\x14\n\nis_default\x18\x07 \x01(\x08H\x00\x12\x12\n\x08\x65\x64itable\x18\x08 \x01(\x08H\x00\x12\x12\n\x08\x65xpanded\x18\t \x01(\x08H\x00\x12\x13\n\tfocusable\x18\n \x01(\x08H\x00\x12\x11\n\x07\x66ocused\x18\x0b \x01(\x08H\x00\x12\x14\n\nhorizontal\x18\x0c \x01(\x08H\x00\x12\x11\n\x07hovered\x18\r \x01(\x08H\x00\x12\x11\n\x07ignored\x18\x0e \x01(\x08H\x00\x12\x13\n\tinvisible\x18\x0f \x01(\x08H\x00\x12\x10\n\x06linked\x18\x10 \x01(\x08H\x00\x12\x13\n\tmultiline\x18\x11 \x01(\x08H\x00\x12\x19\n\x0fmultiselectable\x18\x12 \x01(\x08H\x00\x12\x13\n\toffscreen\x18\x13 \x01(\x08H\x00\x12\x16\n\x0cis_protected\x18\x14 \x01(\x08H\x00\x12\x12\n\x08required\x18\x15 \x01(\x08H\x00\x12\x19\n\x0frichly_editable\x18\x16 \x01(\x08H\x00\x12\x12\n\x08vertical\x18\x17 \x01(\x08H\x00\x12\x11\n\x07visited\x18\x18 \x01(\x08H\x00\x12\x11\n\x07visible\x18\x19 \x01(\x08H\x00\x12\x12\n\x08onscreen\x18\x1a \x01(\x08H\x00\x12\x0f\n\x05\x66irst\x18\x1b \x01(\x08H\x00\x12\x0e\n\x04root\x18\x1c \x01(\x08H\x00\x12\x14\n\nname_regex\x18\x1d \x01(\tH\x00\x12\x1c\n\x12name_starting_with\x18\x1e \x01(\tH\x00\x12\x19\n\x0fname_containing\x18\x1f \x01(\tH\x00\x12\x32\n\x05state\x18  \x01(\x0b\x32!.tast.cros.ui.NodeWith.StateValueH\x00\x12(\n\x08\x61ncestor\x18! \x01(\x0b\x32\x14.tast.cros.ui.FinderH\x00\x1a?\n\nStateValue\x12\"\n\x05state\x18\x01 \x01(\x0e\x32\x13.tast.cros.ui.State\x12\r\n\x05value\x18\x02 \x01(\x08\x42\x07\n\x05value\"@\n\x04Rect\x12\x0c\n\x04left\x18\x01 \x01(\x05\x12\x0b\n\x03top\x18\x02 \x01(\x05\x12\r\n\x05width\x18\x03 \x01(\x05\x12\x0e\n\x06height\x18\x04 \x01(\x05\"\x1d\n\x05Point\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05*\x98\x01\n\tClickType\x12\x1a\n\x16\x43LICK_TYPE_UNSPECIFIED\x10\x00\x12\x19\n\x15\x43LICK_TYPE_LEFT_CLICK\x10\x01\x12\x1a\n\x16\x43LICK_TYPE_RIGHT_CLICK\x10\x02\x12\x1b\n\x17\x43LICK_TYPE_DOUBLE_CLICK\x10\x03\x12\x1b\n\x17\x43LICK_TYPE_MIDDLE_CLICK\x10\x04*h\n\x0bMouseButton\x12\x0f\n\x0bLEFT_BUTTON\x10\x00\x12\x10\n\x0cRIGHT_BUTTON\x10\x01\x12\x11\n\rMIDDLE_BUTTON\x10\x02\x12\x0f\n\x0b\x42\x41\x43K_BUTTON\x10\x03\x12\x12\n\x0e\x46ORWARD_BUTTON\x10\x04*Z\n\x07\x43hecked\x12\x17\n\x13\x43HECKED_UNSPECIFIED\x10\x00\x12\x10\n\x0c\x43HECKED_TRUE\x10\x01\x12\x11\n\rCHECKED_FALSE\x10\x02\x12\x11\n\rCHECKED_MIXED\x10\x03*u\n\x0bRestriction\x12\x1b\n\x17RESTRICTION_UNSPECIFIED\x10\x00\x12\x18\n\x14RESTRICTION_DISABLED\x10\x01\x12\x19\n\x15RESTRICTION_READ_ONLY\x10\x02\x12\x14\n\x10RESTRICTION_NONE\x10\x03*\xc7\x03\n\x05State\x12\x15\n\x11STATE_UNSPECIFIED\x10\x00\x12\x1c\n\x18STATE_AUTOFILL_AVAILABLE\x10\x01\x12\x13\n\x0fSTATE_COLLAPSED\x10\x02\x12\x11\n\rSTATE_DEFAULT\x10\x03\x12\x12\n\x0eSTATE_EDITABLE\x10\x04\x12\x12\n\x0eSTATE_EXPANDED\x10\x05\x12\x13\n\x0fSTATE_FOCUSABLE\x10\x06\x12\x11\n\rSTATE_FOCUSED\x10\x07\x12\x14\n\x10STATE_HORIZONTAL\x10\x08\x12\x11\n\rSTATE_HOVERED\x10\t\x12\x11\n\rSTATE_IGNORED\x10\n\x12\x13\n\x0fSTATE_INVISIBLE\x10\x0b\x12\x10\n\x0cSTATE_LINKED\x10\x0c\x12\x13\n\x0fSTATE_MULTILINE\x10\r\x12\x19\n\x15STATE_MULTISELECTABLE\x10\x0e\x12\x13\n\x0fSTATE_OFFSCREEN\x10\x0f\x12\x13\n\x0fSTATE_PROTECTED\x10\x10\x12\x12\n\x0eSTATE_REQUIRED\x10\x11\x12\x19\n\x15STATE_RICHLY_EDITABLE\x10\x12\x12\x12\n\x0eSTATE_VERTICAL\x10\x13\x12\x11\n\rSTATE_VISITED\x10\x14*\x91 \n\x04Role\x12\x14\n\x10ROLE_UNSPECIFIED\x10\x00\x12\r\n\tROLE_ABBR\x10\x01\x12\x0e\n\nROLE_ALERT\x10\x02\x12\x15\n\x11ROLE_ALERT_DIALOG\x10\x03\x12\x0f\n\x0bROLE_ANCHOR\x10\x04\x12\x14\n\x10ROLE_APPLICATION\x10\x05\x12\x10\n\x0cROLE_ARTICLE\x10\x06\x12\x0e\n\nROLE_AUDIO\x10\x07\x12\x0f\n\x0bROLE_BANNER\x10\x08\x12\x13\n\x0fROLE_BLOCKQUOTE\x10\t\x12\x0f\n\x0bROLE_BUTTON\x10\n\x12\x0f\n\x0bROLE_CANVAS\x10\x0b\x12\x10\n\x0cROLE_CAPTION\x10\x0c\x12\x0e\n\nROLE_CARET\x10\r\x12\r\n\tROLE_CELL\x10\x0e\x12\x12\n\x0eROLE_CHECK_BOX\x10\x0f\x12\x0f\n\x0bROLE_CLIENT\x10\x10\x12\r\n\tROLE_CODE\x10\x11\x12\x13\n\x0fROLE_COLOR_WELL\x10\x12\x12\x0f\n\x0bROLE_COLUMN\x10\x13\x12\x16\n\x12ROLE_COLUMN_HEADER\x10\x14\x12\x1b\n\x17ROLE_COMBO_BOX_GROUPING\x10\x15\x12\x1e\n\x1aROLE_COMBO_BOX_MENU_BUTTON\x10\x16\x12\x1a\n\x15ROLE_COMBO_BOX_SELECT\x10\xbe\x01\x12\x10\n\x0cROLE_COMMENT\x10\x17\x12\x16\n\x12ROLE_COMPLEMENTARY\x10\x18\x12\x19\n\x15ROLE_CONTENT_DELETION\x10\x19\x12\x1a\n\x16ROLE_CONTENT_INSERTION\x10\x1a\x12\x15\n\x11ROLE_CONTENT_INFO\x10\x1b\x12\r\n\tROLE_DATE\x10\x1c\x12\x12\n\x0eROLE_DATE_TIME\x10\x1d\x12\x13\n\x0fROLE_DEFINITION\x10\x1e\x12\x19\n\x15ROLE_DESCRIPTION_LIST\x10\x1f\x12 \n\x1cROLE_DESCRIPTION_LIST_DETAIL\x10 \x12\x1e\n\x1aROLE_DESCRIPTION_LIST_TERM\x10!\x12\x10\n\x0cROLE_DESKTOP\x10\"\x12\x10\n\x0cROLE_DETAILS\x10#\x12\x0f\n\x0bROLE_DIALOG\x10$\x12\x12\n\x0eROLE_DIRECTORY\x10%\x12\x1c\n\x18ROLE_DISCLOSURE_TRIANGLE\x10&\x12\x15\n\x11ROLE_DOC_ABSTRACT\x10\'\x12\x1c\n\x18ROLE_DOC_ACKNOWLEDGMENTS\x10(\x12\x16\n\x12ROLE_DOC_AFTERWORD\x10)\x12\x15\n\x11ROLE_DOC_APPENDIX\x10*\x12\x16\n\x12ROLE_DOC_BACK_LINK\x10+\x12\x19\n\x15ROLE_DOC_BIBLIO_ENTRY\x10,\x12\x19\n\x15ROLE_DOC_BIBLIOGRAPHY\x10-\x12\x17\n\x13ROLE_DOC_BIBLIO_REF\x10.\x12\x14\n\x10ROLE_DOC_CHAPTER\x10/\x12\x15\n\x11ROLE_DOC_COLOPHON\x10\x30\x12\x17\n\x13ROLE_DOC_CONCLUSION\x10\x31\x12\x12\n\x0eROLE_DOC_COVER\x10\x32\x12\x13\n\x0fROLE_DOC_CREDIT\x10\x33\x12\x14\n\x10ROLE_DOC_CREDITS\x10\x34\x12\x17\n\x13ROLE_DOC_DEDICATION\x10\x35\x12\x14\n\x10ROLE_DOC_ENDNOTE\x10\x36\x12\x15\n\x11ROLE_DOC_ENDNOTES\x10\x37\x12\x15\n\x11ROLE_DOC_EPIGRAPH\x10\x38\x12\x15\n\x11ROLE_DOC_EPILOGUE\x10\x39\x12\x13\n\x0fROLE_DOC_ERRATA\x10:\x12\x14\n\x10ROLE_DOC_EXAMPLE\x10;\x12\x15\n\x11ROLE_DOC_FOOTNOTE\x10<\x12\x15\n\x11ROLE_DOC_FOREWORD\x10=\x12\x15\n\x11ROLE_DOC_GLOSSARY\x10>\x12\x16\n\x12ROLE_DOC_GLOSS_REF\x10?\x12\x12\n\x0eROLE_DOC_INDEX\x10@\x12\x19\n\x15ROLE_DOC_INTRODUCTION\x10\x41\x12\x15\n\x11ROLE_DOC_NOTE_REF\x10\x42\x12\x13\n\x0fROLE_DOC_NOTICE\x10\x43\x12\x17\n\x13ROLE_DOC_PAGE_BREAK\x10\x44\x12\x18\n\x14ROLE_DOC_PAGE_FOOTER\x10\x45\x12\x18\n\x14ROLE_DOC_PAGE_HEADER\x10\x46\x12\x16\n\x12ROLE_DOC_PAGE_LIST\x10G\x12\x11\n\rROLE_DOC_PART\x10H\x12\x14\n\x10ROLE_DOC_PREFACE\x10I\x12\x15\n\x11ROLE_DOC_PROLOGUE\x10J\x12\x16\n\x12ROLE_DOC_PULLQUOTE\x10K\x12\x10\n\x0cROLE_DOC_QNA\x10L\x12\x15\n\x11ROLE_DOC_SUBTITLE\x10M\x12\x10\n\x0cROLE_DOC_TIP\x10N\x12\x10\n\x0cROLE_DOC_TOC\x10O\x12\x11\n\rROLE_DOCUMENT\x10P\x12\x18\n\x14ROLE_EMBEDDED_OBJECT\x10Q\x12\x11\n\rROLE_EMPHASIS\x10R\x12\r\n\tROLE_FEED\x10S\x12\x13\n\x0fROLE_FIGCAPTION\x10T\x12\x0f\n\x0bROLE_FIGURE\x10U\x12\x0f\n\x0bROLE_FOOTER\x10V\x12\x1f\n\x1bROLE_FOOTER_AS_NON_LANDMARK\x10W\x12\r\n\tROLE_FORM\x10X\x12\x1a\n\x16ROLE_GENERIC_CONTAINER\x10Y\x12\x1a\n\x16ROLE_GRAPHICS_DOCUMENT\x10Z\x12\x18\n\x14ROLE_GRAPHICS_OBJECT\x10[\x12\x18\n\x14ROLE_GRAPHICS_SYMBOL\x10\\\x12\r\n\tROLE_GRID\x10]\x12\x0e\n\nROLE_GROUP\x10^\x12\x0f\n\x0bROLE_HEADER\x10_\x12\x1f\n\x1bROLE_HEADER_AS_NON_LANDMARK\x10`\x12\x10\n\x0cROLE_HEADING\x10\x61\x12\x0f\n\x0bROLE_IFRAME\x10\x62\x12\x1e\n\x1aROLE_IFRAME_PRESENTATIONAL\x10\x63\x12\x10\n\x0cROLE_IGNORED\x10\x64\x12\x0e\n\nROLE_IMAGE\x10\x65\x12\x12\n\x0eROLE_IMAGE_MAP\x10\x66\x12\x16\n\x12ROLE_IME_CANDIDATE\x10g\x12\x18\n\x14ROLE_INLINE_TEXT_BOX\x10h\x12\x13\n\x0fROLE_INPUT_TIME\x10i\x12\x11\n\rROLE_KEYBOARD\x10j\x12\x13\n\x0fROLE_LABEL_TEXT\x10k\x12\x15\n\x11ROLE_LAYOUT_TABLE\x10l\x12\x1a\n\x16ROLE_LAYOUT_TABLE_CELL\x10m\x12\x19\n\x15ROLE_LAYOUT_TABLE_ROW\x10n\x12\x0f\n\x0bROLE_LEGEND\x10o\x12\x13\n\x0fROLE_LINE_BREAK\x10p\x12\r\n\tROLE_LINK\x10q\x12\r\n\tROLE_LIST\x10r\x12\x11\n\rROLE_LIST_BOX\x10s\x12\x18\n\x14ROLE_LIST_BOX_OPTION\x10t\x12\x12\n\x0eROLE_LIST_GRID\x10u\x12\x12\n\x0eROLE_LIST_ITEM\x10v\x12\x14\n\x10ROLE_LIST_MARKER\x10w\x12\x0c\n\x08ROLE_LOG\x10x\x12\r\n\tROLE_MAIN\x10y\x12\r\n\tROLE_MARK\x10z\x12\x10\n\x0cROLE_MARQUEE\x10{\x12\r\n\tROLE_MATH\x10|\x12\r\n\tROLE_MENU\x10}\x12\x11\n\rROLE_MENU_BAR\x10~\x12\x12\n\x0eROLE_MENU_ITEM\x10\x7f\x12\x1d\n\x18ROLE_MENU_ITEM_CHECK_BOX\x10\x80\x01\x12\x19\n\x14ROLE_MENU_ITEM_RADIO\x10\x81\x01\x12\x1a\n\x15ROLE_MENU_LIST_OPTION\x10\x82\x01\x12\x19\n\x14ROLE_MENU_LIST_POPUP\x10\x83\x01\x12\x0f\n\nROLE_METER\x10\x84\x01\x12\x14\n\x0fROLE_NAVIGATION\x10\x85\x01\x12\x0e\n\tROLE_NOTE\x10\x86\x01\x12\x0e\n\tROLE_PANE\x10\x87\x01\x12\x13\n\x0eROLE_PARAGRAPH\x10\x88\x01\x12\"\n\x1dROLE_PDF_ACTIONABLE_HIGHLIGHT\x10\x89\x01\x12\x17\n\x12ROLE_PLUGIN_OBJECT\x10\x8a\x01\x12\x17\n\x12ROLE_POP_UP_BUTTON\x10\x8b\x01\x12\x10\n\x0bROLE_PORTAL\x10\x8c\x01\x12\r\n\x08ROLE_PRE\x10\x8d\x01\x12\x18\n\x13ROLE_PRESENTATIONAL\x10\x8e\x01\x12\x1c\n\x17ROLE_PROGRESS_INDICATOR\x10\x8f\x01\x12\x16\n\x11ROLE_RADIO_BUTTON\x10\x90\x01\x12\x15\n\x10ROLE_RADIO_GROUP\x10\x91\x01\x12\x10\n\x0bROLE_REGION\x10\x92\x01\x12\x17\n\x12ROLE_ROOT_WEB_AREA\x10\x93\x01\x12\r\n\x08ROLE_ROW\x10\x94\x01\x12\x13\n\x0eROLE_ROW_GROUP\x10\x95\x01\x12\x14\n\x0fROLE_ROW_HEADER\x10\x96\x01\x12\x0e\n\tROLE_RUBY\x10\x97\x01\x12\x19\n\x14ROLE_RUBY_ANNOTATION\x10\x98\x01\x12\x14\n\x0fROLE_SCROLL_BAR\x10\x99\x01\x12\x15\n\x10ROLE_SCROLL_VIEW\x10\x9a\x01\x12\x10\n\x0bROLE_SEARCH\x10\x9b\x01\x12\x14\n\x0fROLE_SEARCH_BOX\x10\x9c\x01\x12\x11\n\x0cROLE_SECTION\x10\x9d\x01\x12\x10\n\x0bROLE_SLIDER\x10\x9e\x01\x12\x16\n\x11ROLE_SLIDER_THUMB\x10\x9f\x01\x12\x15\n\x10ROLE_SPIN_BUTTON\x10\xa0\x01\x12\x12\n\rROLE_SPLITTER\x10\xa1\x01\x12\x15\n\x10ROLE_STATIC_TEXT\x10\xa2\x01\x12\x10\n\x0bROLE_STATUS\x10\xa3\x01\x12\x10\n\x0bROLE_STRONG\x10\xa4\x01\x12\x14\n\x0fROLE_SUGGESTION\x10\xa5\x01\x12\x12\n\rROLE_SVG_ROOT\x10\xa6\x01\x12\x10\n\x0bROLE_SWITCH\x10\xa7\x01\x12\r\n\x08ROLE_TAB\x10\xa8\x01\x12\x12\n\rROLE_TAB_LIST\x10\xa9\x01\x12\x13\n\x0eROLE_TAB_PANEL\x10\xaa\x01\x12\x0f\n\nROLE_TABLE\x10\xab\x01\x12 \n\x1bROLE_TABLE_HEADER_CONTAINER\x10\xac\x01\x12\x0e\n\tROLE_TERM\x10\xad\x01\x12\x14\n\x0fROLE_TEXT_FIELD\x10\xae\x01\x12#\n\x1eROLE_TEXT_FIELD_WITH_COMBO_BOX\x10\xaf\x01\x12\x0e\n\tROLE_TIME\x10\xb0\x01\x12\x0f\n\nROLE_TIMER\x10\xb1\x01\x12\x13\n\x0eROLE_TITLE_BAR\x10\xb2\x01\x12\x17\n\x12ROLE_TOGGLE_BUTTON\x10\xb3\x01\x12\x11\n\x0cROLE_TOOLBAR\x10\xb4\x01\x12\x11\n\x0cROLE_TOOLTIP\x10\xb5\x01\x12\x0e\n\tROLE_TREE\x10\xb6\x01\x12\x13\n\x0eROLE_TREE_GRID\x10\xb7\x01\x12\x13\n\x0eROLE_TREE_ITEM\x10\xb8\x01\x12\x11\n\x0cROLE_UNKNOWN\x10\xb9\x01\x12\x0f\n\nROLE_VIDEO\x10\xba\x01\x12\x12\n\rROLE_WEB_AREA\x10\xbb\x01\x12\x12\n\rROLE_WEB_VIEW\x10\xbc\x01\x12\x10\n\x0bROLE_WINDOW\x10\xbd\x01\x32\xa9\r\n\x11\x41utomationService\x12?\n\x04Info\x12\x19.tast.cros.ui.InfoRequest\x1a\x1a.tast.cros.ui.InfoResponse\"\x00\x12\x45\n\tLeftClick\x12\x1e.tast.cros.ui.LeftClickRequest\x1a\x16.google.protobuf.Empty\"\x00\x12G\n\nRightClick\x12\x1f.tast.cros.ui.RightClickRequest\x1a\x16.google.protobuf.Empty\"\x00\x12I\n\x0b\x44oubleClick\x12 .tast.cros.ui.DoubleClickRequest\x1a\x16.google.protobuf.Empty\"\x00\x12T\n\x0bIsNodeFound\x12 .tast.cros.ui.IsNodeFoundRequest\x1a!.tast.cros.ui.IsNodeFoundResponse\"\x00\x12[\n\x14MouseClickAtLocation\x12).tast.cros.ui.MouseClickAtLocationRequest\x1a\x16.google.protobuf.Empty\"\x00\x12M\n\rEnsureFocused\x12\".tast.cros.ui.EnsureFocusedRequest\x1a\x16.google.protobuf.Empty\"\x00\x12]\n\x15WaitUntilCheckedState\x12*.tast.cros.ui.WaitUntilCheckedStateRequest\x1a\x16.google.protobuf.Empty\"\x00\x12Q\n\x0fWaitUntilExists\x12$.tast.cros.ui.WaitUntilExistsRequest\x1a\x16.google.protobuf.Empty\"\x00\x12M\n\rWaitUntilGone\x12\".tast.cros.ui.WaitUntilGoneRequest\x1a\x16.google.protobuf.Empty\"\x00\x12G\n\nEnsureGone\x12\x1f.tast.cros.ui.EnsureGoneRequest\x1a\x16.google.protobuf.Empty\"\x00\x12G\n\nMousePress\x12\x1f.tast.cros.ui.MousePressRequest\x1a\x16.google.protobuf.Empty\"\x00\x12K\n\x0cMouseRelease\x12!.tast.cros.ui.MouseReleaseRequest\x1a\x16.google.protobuf.Empty\"\x00\x12I\n\x0bMouseMoveTo\x12 .tast.cros.ui.MouseMoveToRequest\x1a\x16.google.protobuf.Empty\"\x00\x12I\n\x0bMakeVisible\x12 .tast.cros.ui.MakeVisibleRequest\x1a\x16.google.protobuf.Empty\"\x00\x12Q\n\x0fWaitForLocation\x12$.tast.cros.ui.WaitForLocationRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x66\n\x11\x43\x61ptureScreenshot\x12&.tast.cros.ui.CaptureScreenshotRequest\x1a\'.tast.cros.ui.CaptureScreenshotResponse\"\x00\x12N\n\tGetUITree\x12\x1e.tast.cros.ui.GetUITreeRequest\x1a\x1f.tast.cros.ui.GetUITreeResponse\"\x00\x12[\n\x14SelectDropDownOption\x12).tast.cros.ui.SelectDropDownOptionRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x45\n\tDoDefault\x12\x1e.tast.cros.ui.DoDefaultRequest\x1a\x16.google.protobuf.Empty\"\x00\x12Q\n\x0fResetAutomation\x12$.tast.cros.ui.ResetAutomationRequest\x1a\x16.google.protobuf.Empty\"\x00\x42\x32Z0go.chromium.org/tast-tests/cros/services/cros/uib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tast.cros.services.cros.ui.automation_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z0go.chromium.org/tast-tests/cros/services/cros/ui'
  _globals['_NODEINFO_HTMLATTRIBUTESENTRY']._loaded_options = None
  _globals['_NODEINFO_HTMLATTRIBUTESENTRY']._serialized_options = b'8\001'
  _globals['_NODEINFO_STATEENTRY']._loaded_options = None
  _globals['_NODEINFO_STATEENTRY']._serialized_options = b'8\001'
  _globals['_CLICKTYPE']._serialized_start=3312
  _globals['_CLICKTYPE']._serialized_end=3464
  _globals['_MOUSEBUTTON']._serialized_start=3466
  _globals['_MOUSEBUTTON']._serialized_end=3570
  _globals['_CHECKED']._serialized_start=3572
  _globals['_CHECKED']._serialized_end=3662
  _globals['_RESTRICTION']._serialized_start=3664
  _globals['_RESTRICTION']._serialized_end=3781
  _globals['_STATE']._serialized_start=3784
  _globals['_STATE']._serialized_end=4239
  _globals['_ROLE']._serialized_start=4242
  _globals['_ROLE']._serialized_end=8355
  _globals['_LEFTCLICKREQUEST']._serialized_start=130
  _globals['_LEFTCLICKREQUEST']._serialized_end=186
  _globals['_MOUSEPRESSREQUEST']._serialized_start=188
  _globals['_MOUSEPRESSREQUEST']._serialized_end=294
  _globals['_MOUSEMOVETOREQUEST']._serialized_start=296
  _globals['_MOUSEMOVETOREQUEST']._serialized_end=375
  _globals['_MOUSERELEASEREQUEST']._serialized_start=377
  _globals['_MOUSERELEASEREQUEST']._serialized_end=447
  _globals['_RIGHTCLICKREQUEST']._serialized_start=449
  _globals['_RIGHTCLICKREQUEST']._serialized_end=506
  _globals['_DOUBLECLICKREQUEST']._serialized_start=508
  _globals['_DOUBLECLICKREQUEST']._serialized_end=566
  _globals['_ISNODEFOUNDREQUEST']._serialized_start=568
  _globals['_ISNODEFOUNDREQUEST']._serialized_end=626
  _globals['_ISNODEFOUNDRESPONSE']._serialized_start=628
  _globals['_ISNODEFOUNDRESPONSE']._serialized_end=664
  _globals['_MOUSECLICKATLOCATIONREQUEST']._serialized_start=666
  _globals['_MOUSECLICKATLOCATIONREQUEST']._serialized_end=776
  _globals['_ENSUREFOCUSEDREQUEST']._serialized_start=778
  _globals['_ENSUREFOCUSEDREQUEST']._serialized_end=838
  _globals['_WAITUNTILCHECKEDSTATEREQUEST']._serialized_start=840
  _globals['_WAITUNTILCHECKEDSTATEREQUEST']._serialized_end=932
  _globals['_WAITUNTILEXISTSREQUEST']._serialized_start=934
  _globals['_WAITUNTILEXISTSREQUEST']._serialized_end=1040
  _globals['_WAITUNTILGONEREQUEST']._serialized_start=1042
  _globals['_WAITUNTILGONEREQUEST']._serialized_end=1146
  _globals['_ENSUREGONEREQUEST']._serialized_start=1148
  _globals['_ENSUREGONEREQUEST']._serialized_end=1266
  _globals['_INFOREQUEST']._serialized_start=1268
  _globals['_INFOREQUEST']._serialized_end=1319
  _globals['_INFORESPONSE']._serialized_start=1321
  _globals['_INFORESPONSE']._serialized_end=1378
  _globals['_MAKEVISIBLEREQUEST']._serialized_start=1380
  _globals['_MAKEVISIBLEREQUEST']._serialized_end=1438
  _globals['_WAITFORLOCATIONREQUEST']._serialized_start=1440
  _globals['_WAITFORLOCATIONREQUEST']._serialized_end=1502
  _globals['_CAPTURESCREENSHOTREQUEST']._serialized_start=1504
  _globals['_CAPTURESCREENSHOTREQUEST']._serialized_end=1584
  _globals['_CAPTURESCREENSHOTRESPONSE']._serialized_start=1586
  _globals['_CAPTURESCREENSHOTRESPONSE']._serialized_end=1633
  _globals['_GETUITREEREQUEST']._serialized_start=1635
  _globals['_GETUITREEREQUEST']._serialized_end=1653
  _globals['_GETUITREERESPONSE']._serialized_start=1655
  _globals['_GETUITREERESPONSE']._serialized_end=1691
  _globals['_RESETAUTOMATIONREQUEST']._serialized_start=1693
  _globals['_RESETAUTOMATIONREQUEST']._serialized_end=1717
  _globals['_SELECTDROPDOWNOPTIONREQUEST']._serialized_start=1719
  _globals['_SELECTDROPDOWNOPTIONREQUEST']._serialized_end=1807
  _globals['_DODEFAULTREQUEST']._serialized_start=1809
  _globals['_DODEFAULTREQUEST']._serialized_end=1865
  _globals['_NODEINFO']._serialized_start=1868
  _globals['_NODEINFO']._serialized_end=2307
  _globals['_NODEINFO_HTMLATTRIBUTESENTRY']._serialized_start=2208
  _globals['_NODEINFO_HTMLATTRIBUTESENTRY']._serialized_end=2261
  _globals['_NODEINFO_STATEENTRY']._serialized_start=2263
  _globals['_NODEINFO_STATEENTRY']._serialized_end=2307
  _globals['_FINDER']._serialized_start=2309
  _globals['_FINDER']._serialized_end=2361
  _globals['_NODEWITH']._serialized_start=2364
  _globals['_NODEWITH']._serialized_end=3212
  _globals['_NODEWITH_STATEVALUE']._serialized_start=3140
  _globals['_NODEWITH_STATEVALUE']._serialized_end=3203
  _globals['_RECT']._serialized_start=3214
  _globals['_RECT']._serialized_end=3278
  _globals['_POINT']._serialized_start=3280
  _globals['_POINT']._serialized_end=3309
  _globals['_AUTOMATIONSERVICE']._serialized_start=8358
  _globals['_AUTOMATIONSERVICE']._serialized_end=10063
# @@protoc_insertion_point(module_scope)
