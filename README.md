# Setting up venv

Make sure Python is installed. You can get it from Microsoft Store as well.
The store installs it here 'C:\Users\<User>\AppData\Local\Programs\Python\Python38\'

```cmd
cd where\ever\you\want\to\create\the\virtual_enviroment
set PYTHON_HOME=C:\Users\<User>\AppData\Local\Programs\Python\Python38
%PYTHON_HOME%\python -m venv secat\venv

cd secat

```

Activate the just created pythond environment
```console
C:\Users\<User>\source\secat>.\venv\Scripts\activate
(secat) C:\Users\<User>\source\secat>
```

Now install requirements
```cmd
pip install -r .\lab4\reqirements.txt
```