1,myBlog
=
このブログは日付ベースでアーカイブ検索を容易にする日誌タイプに特化しています。

現在はグローバルに開かれたURLサイトとしてSEOの観点からあまり推奨されていませんが、

社内や社内部署内部の日誌目的、例えば保守記録やカスタマーサポート記録などとしてならば

何らかどなたかのお役に立てる価値があるかもしれないので、ソースコードを残しておきます。



2,前準備
=
```
#Python 3.7.0 環境

pip3 install django-ckeditor, 

```

3,Nginx settings
=
```
#/etc/nginx/nginx.conf
#新しいバージョンでは/etc/nginx/conf.d/default.confかもしれません。

user  adminuser;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    keepalive_timeout  300;

    server {

        listen       80;
        server_name  my_domain_name;
        charset     utf-8;

        # admin is served at port 443, return 404 on port 80
        root   /home/totinoki/Desktop/frontend/public/;
        set $upstream_server 127.0.0.1:40001;
         location / {
         
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header Host $http_host;
           proxy_pass http://$upstream_server$request_uri;
        }
       location /admin {

           return 301 https://$host$request_uri;

        }
        location /members {

           return 301 https://$host$request_uri;

        }
        location /api/ {
          proxy_pass http://127.0.0.1:40001/api/;
        }

        location /frontend {
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_pass "http://127.0.0.1:3001/";
        }
        location /static/ {
          autoindex  on;
          alias /home/totinoki/testApp/static/;


               location = /static/ckeditor/plugins/locationmap/ {                              
               proxy_http_version 1.1;
               proxy_set_header Upgrade $http_upgrade;
               proxy_set_header Connection "upgrade";
               rewrite ^(.*)$ http://$upstream_server/locationmap/$request_uri break;               
               root /home/totinoki/Desktop/testApp/static/ckeditor/plugins/locationmap/;
               index index.html;
               }

        }

        location /static/admin/ {
          autoindex  on;
          alias /home/totinoki/testApp/static/admin/;
        }

        location /static/vendor/ {
          autoindex  on;
          alias /home/totinoki/testApp/static/vendor/;
        }
        location /static/posts/ {
          autoindex  on;
          alias /home/totinoki/testApp/static/posts/;
        }
        location /static/js/ {
          autoindex  on;
          alias /home/totinoki/Desktop/frontend/build/static/js/;
        }
        location /static/css/ {
          autoindex  on;
          alias /home/totinoki/Desktop/frontend/build/static/css/;
        }

        location /static/ckeditor/ckeditor/plugins/locationmap/ {

           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header Host $http_host;
           proxy_pass http://$upstream_server$request_uri;
           #return 301 https://$host$request_uri;
        }

        location /media/ {
            alias /home/your_account/myBlog/media/;

        }     
    }

    server {

        listen       443 ssl http2;
        server_name  my_domain_name;
        charset     utf-8;
        ssl_certificate      /etc/ssl/imap/imapserver.pem;
        ssl_certificate_key  /etc/ssl/imap/imapserver.key;
        ssl_protocols       TLSv1.2;
        ssl_session_cache    shared:SSL:1m;
        ssl_session_timeout  5m;

        ssl_ciphers  HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers  on;
        location / {

          proxy_pass http://127.0.0.1:40001;
         
         
           proxy_set_header X-Real-IP $remote_addr;
       
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       
           proxy_set_header Host $http_host;
        }



         location /frontend/ {
          autoindex on;
          proxy_pass http://127.0.0.1:3001;

         }
        location /static/vendor/ {
          autoindex  on;
          alias /home/your_account/myBlog/static/vendor/;
        }
        location /static/ckeditor/ckeditor/plugins/locationmap/ {
           root   /home/your_account/myBlog/static/ckeditor/ckeditor/plugins/locationmap/;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_pass "http://127.0.0.1:40001/static/ckeditor/plugins/locationmap/";

        }

        location /static/posts/ {
          autoindex  on;
          alias /home/your_account/myBlog/static/posts/;
        }

        location /media/ {

          alias /home/your_account/myBlog/media/;

        }
       location /static/admin/ {
          autoindex  on;
          alias /home/your_account/myBlog/static/admin/;
        }
    }
 }
```



4,起動のさせ方
=
サーバー内のターミナルで以下の操作をします。

```

source ~/django_py3.7(仮想環境)/bin/activate
gunicorn myBlog.wsgi -b 127.0.0.1:40001 &

```
