root_dir: &ROOT_DIR !!python/name:settings.settings.ROOT_DIR

prod:
    logs: /var/opt/${project_name}/logs

dev:
    logs: !!python/object/apply:os.path.join [*ROOT_DIR, ../logs]
