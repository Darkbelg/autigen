docker build -t autogen .
docker run -it -v $PWD:/myapp --env-file .env autogen python /myapp/introduction.py