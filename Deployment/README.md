# 05- Deployment
---
# 5. Deploying Machine Learning Models
* 5.1 Intro / Session overview
* 5.2 Saving and loading the model
* 5.3 Web services: introduction to Flask
* 5.4 Serving the churn model with Flask
* 5.5 Python virtual environment: Pipenv
* 5.6 Environment management: Docker
* 5.7 Deployment to the cloud: AWS Elastic Beanstalk (optional)
* 5.8 Summary
* 5.9 Explore more
* 5.10 Homework


---


## Docker 

`Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker’s methodologies for shipping, testing, and deploying code quickly, you can significantly reduce the delay between writing code and running it in production.`

### The Docker platform

Docker provides the ability to package and run an application in a loosely isolated environment called a container. The isolation and security allow you to run many containers simultaneously on a given host. Containers are lightweight and contain everything needed to run the application, so you do not need to rely on what is currently installed on the host. You can easily share containers while you work, and be sure that everyone you share with gets the same container that works in the same way.

Docker provides tooling and a platform to manage the lifecycle of your containers:

* Develop your application and its supporting components using containers.
* The container becomes the unit for distributing and testing your application.
* When you’re ready, deploy your application into your production environment, as a container or an orchestrated service. This works the same whether your production environment is a local data center, a cloud provider, or a hybrid of the two.


### What can I use Docker for?
* #### Fast, consistent delivery of your applications
* #### Responsive deployment and scaling
* #### Running more workloads on the same hardware

### Docker architecture

![Dcoker Architecture](https://docs.docker.com/engine/images/architecture.svg)


#### Dockerfile

* A Dockerfile is a set of instructions used to create a Docker image. Each instruction is an operation used to package the application, such as installing dependencies, compile the code, or impersonate a specific user.
* A Docker image is composed of multiple layers, and each layer is represented by an instruction in the Dockerfile. All layers are cached and if an instruction is modified, then during the build process only the changed layer will be rebuild. As a result, building a Docker image using a Dockerfile is a lightweight and quick process.
* To construct a Dockerfile, it is necessary to use the pre-defined instructions, such as:

```Dockerfile
FROM           - to set the base image
RUN            - to execute a command
COPY & ADD     - to copy files from host to the container
CMD            - to set the default command to execute when the container starts
EXPOSE         - to expose an application port 

```

## Example : 

```Dockerfile
# Base image:
FROM agrigorev/zoomcamp-model:3.8.12-slim                

LABEL maintainer="Name of the Maintainer"

ENV PYTHONUNBUFFERED=TRUE

# -- Install Pipenv:
RUN pip --no-cache-dir install pipenv

# -- Install Application into container:
RUN set -ex && mkdir /app
WORKDIR /app

# COPY Pipfile.lock Pipfile.lock
COPY ["Pipfile", "Pipfile.lock", "./"]

# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system

# Copy files from host to the container
COPY ["*.py", "churn-model1.bin","churn-dv.bin", "./"]

# Port where the App will be Exposed
EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "churn_flask_serving:app"] 
```


#### Dockerimage

* Once a Dockerfile is constructed, these instructions are used to build a Docker image.
* A Docker image is a read-only template that enables the creation of a runnable instance of an application.
* In a nutshell, a Docker image provides the execution environment for an application, including any essential code, config files, and dependencies.
* A Docker image can be built from an existing Dockerfile using the docker build command. Below is the syntax for this command:

```bash
# build an image
# OPTIONS - optional;  define extra configuration
# PATH - required;  sets the location of the Dockefile and  any referenced files 

docker build [OPTIONS] PATH

# Where OPTIONS can be:
-t, --tag            - set the name and tag of the image
-f, --file           - set the name of the Dockerfile
--build-arg          - set build-time variables

# Find all valid options for this command 
docker build --help

```


## Example 

* Build the image
```bash
docker build -t churn-prediction .
```

* Run it 
```bash
docker run -it -p 9696:9696 churn-prediction:latest
```

#### Docker Registry
* The last step in packaging an application using Docker is to store and distribute it. So far, we have built and tested an image on the local machine, which does not ensure that other engineers have access to it. As a result, the image needs to be pushed to a public Docker image registry, such as DockerHub, Harbor, Google Container Registry, and many more. 
* To tag an existing image on the local machine, the docker tag command is available. Below is the syntax for this command:

```bash
# tag an image
# SOURCE_IMAGE[:TAG]  - required and the tag is optional; define the name of an image on the current machine 
# TARGET_IMAGE[:TAG] -  required and the tag is optional; define the repository, name, and version of an image
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
```

* Once the image is tagged, the final step is to push the image to a registry. For this purpose, the docker push command can be used. Below is the syntax for this command:
```bash
# push an image to a registry 
# NAME[:TAG] - required and the tag is optional; name, set the image name to be pushed to the registry
docker push NAME[:TAG]
```

* `OPTIONS`          - define extra configuration through flags
* `IMAGE`            - sets the name of the image
* `NAME`             - set the name of the image
* `COMMAND and ARG`  - instruct the container to run specific commands associated with a set of arguments

# Example : 
* tag it 
```bash
docker tag churn-prediction ayoubberd/churn-prediction:latest
```

* Push it
```bash
docker push ayoubberd/churn-prediction:latest
```



# The image can be pulled from 

```bash
docker pull ayoubberd/churn-prediction:latest
```
