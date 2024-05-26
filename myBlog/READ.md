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
$source ~/django_py3.7(仮想環境)/bin/activate
$ pip list
Package                        Version
------------------------------ --------
asn1crypto                     0.24.0
beautifulsoup4                 4.6.3
cffi                           1.11.5
cryptography                   2.3
Django                         2.0.3
django-braces                  1.12.0
django-category                2.0.0
django-ckeditor                5.6.1
django-classy-tags             0.8.0
django-cors-headers            2.4.0
django-crispy-forms            1.7.2
django-csp                     3.4
django-debug-toolbar           1.10.1
django-elasticsearch-dsl       0.5.0
django-feedreader              2.0.0
django-froala-editor           2.8.5
django-hitcount                1.3.0
django-js-asset                1.1.0
django-js-reverse              0.8.2
django-markitup                3.0.0
django-object-tools            1.11.0
django-pandas                  0.5.1
django-taggit                  0.23.0
django-taggit-templatetags2    1.6.1
django-templatetag-sugar       1.0
django-webpack-loader          0.6.0
djangorestframework            3.8.2
djangorestframework-camel-case 0.2.0
elasticsearch                  6.3.1
elasticsearch-dsl              6.2.1
factory-boy                    2.10.0
Faker                          0.9.1
feedparser                     5.2.1
gunicorn                       19.9.0
idna                           2.7
ipaddress                      1.0.22
mysql-connector-python         8.0.12
mysqlclient                    1.3.13
numpy                          1.15.2
pandas                         0.23.4
Pillow                         5.2.0
pip                            24.0
protobuf                       3.6.0
pycparser                      2.18
PyMySQL                        0.9.2
python-dateutil                2.7.3
pytz                           2018.5
scipy                          1.1.0
setuptools                     39.0.1
six                            1.11.0
sqlparse                       0.2.4
text-unidecode                 1.2
urllib3                        1.23
uWSGI                          2.0.17.1


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
