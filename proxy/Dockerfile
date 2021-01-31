FROM nginx:1.19.0-alpine

WORKDIR /proxy
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /vol/static
RUN chmod 775 /vol/static

