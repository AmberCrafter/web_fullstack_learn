# Virtual Private Server

## [Heroku](https://www.heroku.com/home)

 - [Index](https://ideasky-fullstack-frontend.herokuapp.com/)
 - [Control](https://ideasky-fullstack-frontend.herokuapp.com/control.html)

---
## Setup
1. Seperate system into frontend and backend
 - [Frontend](https://github.com/AmberCrafter/web_fullstack_learn/tree/heroku_frontend)
 - [Backend](https://github.com/AmberCrafter/web_fullstack_learn/tree/heroku_backend)

2. Backend
    - add Proc file in root path (/Proc)
        ```Proc
        web: uvicorn app:app --host=0.0.0.0 --port=${PORT:-5000}
        ```
        > Notice `Proc` is capitalize.

    - add runtime file in root path (/runtime)
        ```runtime
        python-3.10.5
        ```

    - setup buildpack ()
        - heroku/python

    - setup addon of Postgresql, due to sqlite3 is invalid in heroku right now
        - Heroku Postgres 

    - get sql url form os environment ($DATABASE_URL)
        ```python
        # /database/interface_pg.py
        import os
        ...
        class Database(metaclass = Singleton_meta):
            '''
            In release product, database need to change into other PaaS,
            which will advoid missing the data when rebuild the product.
            Recommand to use the firebase.
            '''

            def __init__(self):
                # database_path = os.getenv("QUEST_DATABASE")
                database_path = os.getenv("DATABASE_URL")
                ...
        ```

3. Frontend
    - setup buildpack
        - https://buildpack-registry.s3.amazonaws.com/buildpacks/heroku-community/nginx.tgz
    
    - add Proc file in root path (/Proc)
        ```Proc
        web: bin/start-nginx-solo 
        ```
        > Notice `Proc` is capitalize.

    - setup nginx config (/config/nginx.conf.erb)
        ```erb
        daemon off;
        # Heroku dynos have at least 4 cores.
        worker_processes <%= ENV['NGINX_WORKERS'] || 1 %>;

        events {
            use epoll;
            accept_mutex on;
            worker_connections <%= ENV['NGINX_WORKER_CONNECTIONS'] || 1024 %>;
        }

        http {
            gzip on;
            gzip_comp_level 2;
            gzip_min_length 512;
            gzip_proxied any; # Heroku router sends Via header

            server_tokens off;

            log_format l2met 'measure#nginx.service=$request_time request_id=$http_x_request_id';
            access_log <%= ENV['NGINX_ACCESS_LOG_PATH'] || 'logs/nginx/access.log' %> l2met;
            error_log <%= ENV['NGINX_ERROR_LOG_PATH'] || 'logs/nginx/error.log' %>;


            include mime.types;
            default_type application/octet-stream;
            sendfile on;

            # Must read the body in 5 seconds.
            client_body_timeout <%= ENV['NGINX_CLIENT_BODY_TIMEOUT'] || 5 %>;

            server {
                listen <%= ENV["PORT"] %>;
                server_name _;
                keepalive_timeout 5;
                client_max_body_size <%= ENV['NGINX_CLIENT_MAX_BODY_SIZE'] || 1 %>M;

                location / {
                    root /app/frontend; # path to your app
                }
            }
        }
        ```

4. Deploy on Heroku

5. Update Frontend `DATABASE_URL_BASE`, depended on your backend url.