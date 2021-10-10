FROM agrigorev/zoomcamp-model:3.8.12-slim                

LABEL maintainer="Ayoub Berdeddouch"

ENV PYTHONUNBUFFERED=TRUE

RUN pip --no-cache-dir install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system
# RUN pipenv install --deploy --system 

COPY ["*.py", "churn-model1.bin","churn-dv.bin", "./"]

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "churn_flask_serving:app"] 