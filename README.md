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
