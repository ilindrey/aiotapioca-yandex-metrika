# flake8: noqa
from .parsers import LogsAPIParser, ReportsAPIParser


__all__ = (
    "MANAGEMENT_API_RESOURCE_MAPPING",
    "REPORTS_API_RESOURCE_MAPPING",
    "LOGS_API_RESOURCE_MAPPING",
)

MANAGEMENT_API_RESOURCE_MAPPING = {
    "counters": {
        "resource": "management/v1/counters",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/counters/counters-docpage/",
        "params": """
                [callback=<string>]
                & [favorite=<boolean>]
                & [field=<string>]
                & [label_id=<integer>]
                & [offset=<int>]
                & [per_page=<int>]
                & [permission=<string>]
                & [reverse=<boolean>]
                & [search_string=<string>]
                & [sort=<counters_sort>]
                & [status=<counter_status>]
                & [type=<counter_type>]
                """,
        "methods": ["GET", "POST"],
        "response_data_key": "counters",
    },
    "counter": {
        "resource": "management/v1/counter/{counter_id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/counters/counter-docpage/",
        "params": """[callback=<string>] & [field=<string>]""",
        "methods": ["GET", "DELETE", "PUT"],
    },
    "counter_undelete": {
        "resource": "management/v1/counter/{counter_id}/undelete",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/counters/undeletecounter-docpage/",
        "params": """""",
        "methods": ["POST"],
    },
    "goals": {
        "resource": "management/v1/counter/{counter_id}/goals",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/goals/goals-docpage/",
        "params": """[callback=<string>] & [useDeleted=<boolean>]""",
        "methods": ["GET", "POST"],
        "response_data_key": "goals",
    },
    "goal": {
        "resource": "management/v1/counter/{counter_id}/goal/{goal_id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/goals/goal-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "DELETE", "PUT"],
    },
    "accounts": {
        "resource": "management/v1/accounts",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/accounts/accounts-docpage/",
        "params": """[callback=<string>] & [user_login=<string>]""",
        "methods": ["GET", "DELETE", "PUT"],
        "response_data_key": "accounts",
    },
    "clients": {
        "resource": "management/v1/clients",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/direct_clients/getclients-docpage/",
        "params": """counters=<list>""",
        "methods": [
            "GET",
        ],
        "response_data_key": "clients",
    },
    "filters": {
        "resource": "management/v1/counter/{counter_id}/filters",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/filters/filters-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "POST"],
    },
    "filter": {
        "resource": "management/v1/counter/{counter_id}/filter/{filter_id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/filters/filter-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "DELETE", "PUT"],
    },
    "operations": {
        "resource": "management/v1/counter/{counter_id}/operations",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/operations/operations-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "POST"],
    },
    "operation": {
        "resource": "management/v1/counter/{counter_id}/operation/{operation_id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/operations/operation-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "DELETE", "PUT"],
    },
    "grants": {
        "resource": "management/v1/counter/{counter_id}/grants",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/grants/grants-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "POST"],
    },
    "grant": {
        "resource": "management/v1/counter/{counter_id}/grant",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/grants/grant-docpage/",
        "params": """user_login=<string>""",
        "methods": ["GET", "PUT", "DELETE"],
    },
    "public_grant": {
        "resource": "management/v1/counter/{counter_id}/public_grant",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/public-grants/addgrant-docpage/",
        "params": """""",
        "methods": ["POST", "DELETE"],
    },
    "delegates": {
        "resource": "management/v1/delegates",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/delegates/delegates-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "POST"],
    },
    "delegate": {
        "resource": "management/v1/delegate",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/delegates/deletedelegate-docpage/",
        "params": """user_login=<string>""",
        "methods": ["DELETE"],
    },
    "labels": {
        "resource": "management/v1/labels",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/labels/getlabels-docpage/",
        "params": None,
        "methods": ["GET", "POST"],
    },
    "label": {
        "resource": "management/v1/label/{label_id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/labels/getlabel-docpage/",
        "params": None,
        "methods": ["GET", "DELETE", "PUT"],
    },
    "set_counter_label": {
        "resource": "management/v1/counter/{counter_id}/label/{label_id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/links/setcounterlabel-docpage/",
        "params": None,
        "methods": ["POST", "DELETE"],
    },
    "segments": {
        "resource": "management/v1/counter/{counter_id}/apisegment/segments",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/segments/getsegmentsforcounter-docpage/",
        "params": None,
        "methods": ["GET", "POST"],
    },
    "segment": {
        "resource": "management/v1/counter/{counter_id}/apisegment/segment/{segment_id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/segments/getsegment-docpage/",
        "params": None,
        "methods": ["GET", "DELETE", "PUT"],
    },
    "user_params_uploadings": {
        "resource": "management/v1/counter/{counter_id}/user_params/uploadings",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/userparams/findall-docpage/",
        "params": None,
        "methods": ["GET"],
    },
    "user_params_uploading": {
        "resource": "management/v1/counter/{counter_id}/user_params/uploading/{uploading_id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/userparams/findbyid-docpage/",
        "params": None,
        "methods": ["GET", "PUT"],
    },
    "user_params_upload": {
        "resource": "management/v1/counter/{counter_id}/user_params/uploadings/upload",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/userparams/upload-docpage/",
        "params": """action=<user_params_uploading_action>""",
        "methods": ["POST"],
    },
    "user_params_uploading_confirm": {
        "resource": "management/v1/counter/{counter_id}/user_params/uploading/{uploading_id}/confirm",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/userparams/confirm-docpage/",
        "params": None,
        "methods": ["POST"],
    },
    "chart_annotations": {
        "resource": "management/v1/counter/{counter_id}/chart_annotations",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/chart_annotation/findall-docpage/",
        "params": None,
        "methods": ["GET", "POST"],
    },
    "chart_annotation": {
        "resource": "management/v1/counter/{counter_id}/chart_annotation/{id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/chart_annotation/get-docpage/",
        "params": None,
        "methods": ["GET", "DELETE", "PUT"],
    },
    "yclid_conversions_uploadings": {
        "resource": "management/v1/counter/{counter_id}/yclid_conversions/uploadings",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/yclid-conversion/findall-docpage/",
        "params": """[limit=<integer>] & [offset=<integer>""",
        "methods": ["GET"],
    },
    "yclid_conversions_uploading": {
        "resource": "management/v1/counter/{counter_id}/yclid_conversions/uploading/{id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/yclid-conversion/findbyid-docpage/",
        "params": None,
        "methods": ["GET"],
    },
    "yclid_conversions_upload": {
        "resource": "management/v1/counter/{counter_id}/yclid_conversions/upload",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/yclid-conversion/upload-docpage/",
        "params": """[comment=<string>]""",
        "methods": ["GET"],
    },
    "offline_conversions_uploadings": {
        "resource": "management/v1/counter/{counter_id}/offline_conversions/uploadings",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/offline_conversion/findall-docpage/",
        "params": None,
        "methods": ["GET"],
    },
    "offline_conversions_calls_uploadings": {
        "resource": "management/v1/counter/{counter_id}/offline_conversions/calls_uploadings",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/offline_conversion/findallcalluploadings-docpage/",
        "params": None,
        "methods": ["GET"],
    },
    "offline_conversions_uploading": {
        "resource": "management/v1/counter/{counter_id}/offline_conversions/uploading/{id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/offline_conversion/findbyid-docpage/",
        "params": None,
        "methods": ["GET"],
    },
    "offline_conversions_calls_uploading": {
        "resource": "management/v1/counter/{counter_id}/offline_conversions/calls_uploading/{id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/offline_conversion/findcalluploadingbyid-docpage/",
        "params": None,
        "methods": ["GET"],
    },
    "offline_conversions_upload": {
        "resource": "management/v1/counter/{counter_id}/offline_conversions/upload",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/offline_conversion/upload-docpage/",
        "params": """client_id_type=<offline_conversion_uploading_client_id_type> & [comment=<string>]""",
        "methods": ["POST"],
    },
    "offline_conversions_upload_calls": {
        "resource": "management/v1/counter/{counter_id}/offline_conversions/upload_calls",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/offline_conversion/uploadcalls-docpage/",
        "params": """
                client_id_type=<offline_conversion_uploading_client_id_type>
                & [comment=<string>]
                & [new_goal_name=<string>]
                """,
        "methods": ["POST"],
    },
    "offline_conversions_extended_threshold": {
        "resource": "management/v1/counter/{counter_id}/offline_conversions/extended_threshold",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/offline_conversion/enableextendedthreshold-docpage/",
        "params": None,
        "methods": ["POST", "DELETE"],
    },
    "offline_conversions_calls_extended_threshold": {
        "resource": "management/v1/counter/{counter_id}/offline_conversions/calls_extended_threshold",
        "docs": "https://yandex.com/dev/metrika/doc/api2/management/offline_conversion/enablecallsextendedthreshold-docpage/",
        "params": None,
        "methods": ["POST", "DELETE"],
    },
}

REPORTS_API_RESOURCE_MAPPING = {
    "reports": {
        "resource": "stat/v1/data",
        "docs": "https://yandex.com/dev/metrika/doc/api2/api_v1/intro-docpage/",
        "params": [
            "direct_client_logins=<string,_string,...>",
            "ids=<int,int,...>",
            "metrics=<string>",
            "accuracy=<string>",
            "callback=<string>",
            "date1=<string>",
            "date2=<string>",
            "dimensions=<string>",
            "filters=<string>",
            "include_undefined=<boolean>",
            "lang=<string>",
            "limit=<integer>",
            "offset=<integer>",
            "preset=<string>",
            "pretty=<boolean>",
            "proposed_accuracy=<boolean>",
            "sort=<string>",
            "timezone=<string>",
        ],
        "parsers": {
            "headers": ReportsAPIParser.headers,
            "values": ReportsAPIParser.values,
            "dicts": ReportsAPIParser.dicts,
            "columns": ReportsAPIParser.columns,
        },
    },
}

LOGS_API_RESOURCE_MAPPING = {
    "all_info": {
        "resource": "management/v1/counter/{counter_id}/logrequests",
        "docs": "https://yandex.com/dev/metrika/doc/api2/logs/queries/getlogrequests-docpage/",
        "params": None,
        "methods": ["GET"],
    },
    "info": {
        "resource": "management/v1/counter/{counter_id}/logrequest/{request_id}",
        "docs": "https://yandex.com/dev/metrika/doc/api2/logs/queries/getlogrequest-docpage/",
        "params": None,
        "methods": ["GET"],
    },
    "download": {
        "resource": "management/v1/counter/{counter_id}/logrequest/{request_id}/part/{part_number}/download",
        "docs": "https://yandex.com/dev/metrika/doc/api2/logs/queries/download-docpage/",
        "params": None,
        "methods": ["GET"],
        "parsers": {
            "headers": LogsAPIParser.headers,
            "lines": LogsAPIParser.lines,
            "values": LogsAPIParser.values,
            "dicts": LogsAPIParser.dicts,
            "columns": LogsAPIParser.columns,
        },
    },
    "clean": {
        "resource": "management/v1/counter/{counter_id}/logrequest/{request_id}/clean",
        "docs": "https://yandex.com/dev/metrika/doc/api2/logs/queries/clean-docpage/",
        "params": None,
        "methods": ["POST"],
    },
    "cancel": {
        "resource": "management/v1/counter/{counter_id}/logrequest/{request_id}/cancel",
        "docs": "https://yandex.com/dev/metrika/doc/api2/logs/queries/cancel-docpage/",
        "params": None,
        "methods": ["POST"],
    },
    "create": {
        "resource": "management/v1/counter/{counter_id}/logrequests",
        "docs": "https://yandex.com/dev/metrika/doc/api2/logs/queries/createlogrequest-docpage/",
        "params": ["date1", "date2", "fields", "source"],
        "methods": ["POST"],
    },
    "evaluate": {
        "resource": "management/v1/counter/{counter_id}/logrequests/evaluate",
        "docs": "https://yandex.com/dev/metrika/doc/api2/logs/queries/evaluate-docpage/",
        "params": ["date1", "date2", "fields", "source"],
        "methods": ["GET"],
    },
}
