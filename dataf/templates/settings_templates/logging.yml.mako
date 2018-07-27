log_dir: &LOG_DIR !get_directory [logs]
host_name: &HOST_NAME !!python/object/apply:socket.gethostname []

prod:
    version: 1
    disable_existing_loggers: False
    formatters:
        simple:
            format: !join ["%(asctime)s - %(name)s - ", *HOST_NAME, " - %(message)s"]

    filters:
        debug_lvl:
            (): dataf.LvlFilter
            low: 10
            high: 10
        info_lvl:
            (): dataf.LvlFilter
            low: 20
            high: 20
        error_lvl:
            (): dataf.LvlFilter
            low: 40
            high: 40
        slack_lvl:
            (): dataf.LvlFilter
            low: 30
            high: 60

    handlers:
        console:
            class: logging.StreamHandler
            formatter: simple
            stream: ext://sys.stdout

        info_file_handler:
            class: logging.handlers.TimedRotatingFileHandler
            formatter: simple
            filename: !!python/object/apply:os.path.join [*LOG_DIR, info.log]
            backupCount: 30
            when: midnight
            encoding: utf8
            filters: [info_lvl]

        error_file_handler:
            class: logging.handlers.TimedRotatingFileHandler
            formatter: simple
            filename: !!python/object/apply:os.path.join [*LOG_DIR, errors.log]
            backupCount: 30
            when: midnight
            encoding: utf8
            filters: [error_lvl]

        slack_handler:
            class: dataf.SlackHandler
            formatter: simple
            token: slack-token
            channel: '#channel'
            proxies:
                http: vpprx:3128
                https: vpprx:3128
            filters: [slack_lvl]

    root:
        level: DEBUG
        handlers: [info_file_handler, error_file_handler, slack_handler]

dev:
    handlers:
        info_file_handler:
            when: H

        error_file_handler:
            when: H

        slack_handler:
            channel: '#channel'
