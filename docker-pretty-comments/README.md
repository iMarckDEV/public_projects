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

##Deploying the Docker Image
1. Clone this repository:
<pre>
```batch
git clone <repository-url>
```
</pre>

2.Navigate to the project directory:
<pre>
```batch
cd docker-pretty-comment

```
</pre>

3.Build the Docker image:
<pre>
```batch
docker build -t pretty-comment .

```
</pre>
4.Run the Docker continer in locally:
<pre>
```batch
docker run -it --entrypoint python pretty-comment pretty_comment.py "This is a sample comment"

```

