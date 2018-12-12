FROM python:3
ADD . ./workdir
RUN pip install --user -r ./workdir/requirements.txt
RUN python ./workdir/manage.py migrate
EXPOSE 8000
CMD ["python", "./workdir/manage.py", "runserver", "0.0.0.0:8000"]