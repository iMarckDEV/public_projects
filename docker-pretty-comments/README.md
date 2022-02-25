# Docker Deployment for Pretty Comment

This repository contains a Dockerized Python application that receives a comment as a command-line argument and prints it as a pretty comment. It is a simple example demonstrating Docker deployment.

Check out my blog post on [www.imarck.dev](https://www.imarck.dev) for a detailed explanation of the project.

## Example Pretty Comment Format

```python
pretty_text = '''
#########################################
#--This is a sample pretty comment!--#
#########################################
'''

print(pretty_text)
```

##Deploying the Docker Image
1. Clone this repository:

```batch
git clone <repository-url>
```


2.Navigate to the project directory:

```batch
cd docker-pretty-comment

```


3.Build the Docker image:

```batch
docker build -t pretty-comment .

```

4.Run the Docker continer in locally:

```batch
docker run -it --entrypoint python pretty-comment pretty_comment.py "This is a sample comment"

##############################
#--This is a sample comment--#
##############################
```

And now you can copy and paste the comment in your code, so easily.
