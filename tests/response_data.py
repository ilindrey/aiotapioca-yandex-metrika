from json import dumps


COUNTERS_DATA = dumps(
    {
        "rows": 2,
        "counters": [
            {
                "id": 12345678,
                "status": "Active",
                "owner_login": "Aaaaa",
                "code_status": "CS_ERR_UNKNOWN",
                "activity_status": "low",
                "name": "counter 1",
                "type": "simple",
                "favorite": 1,
                "hide_address": 0,
                "permission": "own",
                "webvisor": {
                    "urls": "",
                    "arch_enabled": 1,
                    "arch_type": "none",
                    "load_player_type": "proxy",
                    "wv_version": 2,
                    "allow_wv2": True,
                    "wv_forms": 1,
                },
                "code_options": {
                    "async": 1,
                    "informer": {
                        "enabled": 0,
                        "type": "ext",
                        "size": 3,
                        "indicator": "pageviews",
                        "color_start": "FFFFFFFF",
                        "color_end": "FFFFFFFF",
                        "color_text": 0,
                        "color_arrow": 0,
                    },
                    "visor": 0,
                    "track_hash": 1,
                    "xml_site": 0,
                    "clickmap": 1,
                    "in_one_line": 0,
                    "ecommerce": 0,
                    "alternative_cdn": 0,
                    "ecommerce_object": "dataLayer",
                },
                "create_time": "2018-09-29T11:06:04+04:00",
                "time_zone_name": "Europe/London",
                "time_zone_offset": 120,
                "partner_id": 0,
                "site": "test.com",
                "site2": {"site": "test.com", "domain": "test.com"},
                "gdpr_agreement_accepted": 0,
            },
            {
                "id": 87654321,
                "status": "Active",
                "owner_login": "Bbbb",
                "code_status": "CS_ERR_UNKNOWN",
                "activity_status": "high",
                "name": "counter 2",
                "type": "simple",
                "favorite": 1,
                "hide_address": 0,
                "permission": "own",
                "webvisor": {
                    "urls": "regexp:.*",
                    "arch_enabled": 0,
                    "arch_type": "none",
                    "load_player_type": "proxy",
                    "wv_version": 2,
                    "allow_wv2": True,
                    "wv_forms": 1,
                },
                "code_options": {
                    "async": 1,
                    "informer": {
                        "enabled": 0,
                        "type": "ext",
                        "size": 3,
                        "indicator": "pageviews",
                        "color_start": "FFFFFFFF",
                        "color_end": "EFEFEFFF",
                        "color_text": 0,
                        "color_arrow": 1,
                    },
                    "visor": 0,
                    "track_hash": 0,
                    "xml_site": 0,
                    "clickmap": 1,
                    "in_one_line": 0,
                    "ecommerce": 0,
                    "alternative_cdn": 0,
                    "ecommerce_object": "dataLayer",
                },
                "create_time": "2019-09-25T10:21:23+03:00",
                "time_zone_name": "Europe/London",
                "time_zone_offset": 120,
                "partner_id": 0,
                "site": "test2.com",
                "site2": {"site": "test2.com", "domain": "test2.com"},
                "gdpr_agreement_accepted": 0,
            },
        ],
    },
)

GOALS_DATA = dumps(
    {
        "goals": [
            {
                "id": 1234567,
                "name": "goal 1",
                "type": "url",
                "default_price": 0.0,
                "is_retargeting": 0,
                "goal_source": "user",
                "is_favorite": 0,
                "prev_goal_id": 0,
                "conditions": [{"type": "contain", "url": "#signup"}],
            },
            {
                "id": 7654321,
                "name": "goal 2",
                "type": "action",
                "default_price": 0.0,
                "is_retargeting": 0,
                "goal_source": "user",
                "is_favorite": 0,
                "prev_goal_id": 0,
                "conditions": [{"type": "exact", "url": "start_reg"}],
            },
        ]
    },
)

GOAL_DATA = dumps(
    {
        "goal": {
            "id": 1234567,
            "name": "goal 1",
            "type": "url",
            "default_price": 0.0,
            "is_retargeting": 0,
            "goal_source": "user",
            "is_favorite": 0,
            "prev_goal_id": 0,
            "conditions": [{"type": "contain", "url": "#signup"}],
        }
    },
)


REPORTS_DATA = dumps(
    {
        "query": {
            "ids": [100500],
            "dimensions": ["ym:s:date"],
            "metrics": ["ym:s:visits"],
            "sort": ["ym:s:date"],
            "date1": "2020-10-01",
            "date2": "2020-10-05",
            "filters": r"ym:s:startURL=.('https://rfgf.ru/map','https://rfgf.ru/map')",
            "limit": 1,
            "offset": 1,
            "group": "Day",
            "auto_group_size": "1",
            "attr_name": "",
            "quantile": "50",
            "offline_window": "21",
            "attribution": "LastSign",
            "currency": "RUB",
            "adfox_event_id": "0",
        },
        "data": [
            {"dimensions": [{"name": "2020-10-01"}], "metrics": [14234.0]},
            {"dimensions": [{"name": "2020-10-02"}], "metrics": [12508.0]},
            {"dimensions": [{"name": "2020-10-03"}], "metrics": [12365.0]},
            {"dimensions": [{"name": "2020-10-04"}], "metrics": [14588.0]},
            {"dimensions": [{"name": "2020-10-05"}], "metrics": [14579.0]},
        ],
        "total_rows": 5,
        "total_rows_rounded": False,
        "sampled": False,
        "contains_sensitive_data": False,
        "sample_share": 1.0,
        "sample_size": 68280,
        "sample_space": 68280,
        "data_lag": 4242,
        "totals": [68274.0],
        "min": [12365.0],
        "max": [14588.0],
    },
)

LOGS_DATA = (
    "col1\tcol2\tcol3\tcol4\tcol5\n"
    "val1\tval2\tval3\tval4\tval5\n"
    "val11\tval22\tval33\tval44\tval55\n"
    "val111\tval222\tval333\tval444\tval555\n"
    "val1111\tval2222\tval3333\tval4444\tval5555\n"
)
