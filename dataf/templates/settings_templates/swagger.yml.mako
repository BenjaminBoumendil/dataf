prod:
    template:
        info:
            title: ${project_name.capitalize()} API
            contact:
                Slack: slack-channel

    config:
        headers: []
        specs: [{
            endpoint: apispec_1,
            route: /apispec_1.json,
            rule_filter: !!python/name:settings.settings.rule_filter ,
            model_filter: !!python/name:settings.settings.model_filter ,
        }]
        static_url_path: /flasgger_static
        swagger_ui: True
        specs_route: /api/docs/

dev:
    template:
        host: localhost:5000
