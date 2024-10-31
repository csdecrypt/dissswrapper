docker build -t whisper-flask-app .
docker run --rm -p 5000:5000 whisper-flask-app
docker tag local-image:tagname new-repo:tagname

docker build --platform linux/amd64 -t csdecrypt/disss:amd644 .
 docker build --platform linux/arm64 -t csdecrypt/disss:arm64 .