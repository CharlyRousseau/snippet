# Snippet

Project made by :

- CUSMA Vincenzo
- LHUISSIER Flavien
- ROUSSEAU Charly
- ROUSSEAU Clément

## What's that ?

> A small educational project to demonstrate the use of Django in a 'real' project.

In this project, we can create our account to generate a 'snippet', a code snippet literally.
However, that's not all ! You can share your snippets to everyone you want, like and save other snippets made by others and more !

The snippet is generated thanks to an AI and after generating your snippet, you can save it by giving it a name, without forgetting that can specify the language used, if the method must be static (depending on the language used) and finally in the category that you want to describe it (Bug Fix, Algorithm, Project set up).

## Features

### User Creation
Users can register and create an account to start using the application. This involves providing basic information such as username, email, and password.

### User Edition
Once an account is created, users can edit their information. This includes updating their username, email, and password. The user-friendly interface ensures that users can easily manage their account details.

### Profile Edition
Each user has a profile that can be personalized. Users can edit their profiles to add more details about themselves, such as bio, profile picture, and other personal information. This helps in building a community feel within the application.

### AI-Assisted Snippet Creation
One of the standout features of this application is the AI-assisted snippet creation. Users can provide instructions, and the AI will generate a code snippet based on these instructions. This feature leverages artificial intelligence to help users quickly create and save code snippets, enhancing productivity and learning.

### Snippet Liking
Users can like snippets created by others. This feature allows users to appreciate the efforts and contributions of others, fostering a supportive community. Additionally, liked snippets can be used to highlight valuable solutions or innovative coding techniques.

### Snippet Favoriting
Apart from liking, users can also favorite snippets. This feature enables users to save their preferred snippets for easy access later. Favorited snippets are stored in a personalized list, making it convenient for users to revisit important or frequently used code snippets.

## Environment / Line commands

- Python (v. 3.12.0)
- Django (v. 5.0.6)
- PyEnv

After cloning this project and create your virtual environment, run the following command to install every packages in `requirements.txt` :

```bash
(virtualenv) pip install -r requirements.txt
```

> _I put **(virtualenv)** in the code block to tell that we have activated our virtual environment before installing our packages._

To run a server (development by default) :

```bash
(virtualenv) python manage.py runserver
```

To run tests :

```bash
(virtualenv) python manage.py test
```
