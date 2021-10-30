[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

![License](https://img.shields.io/github/license/S1riyS/GravitySimulation)
![Quality](https://img.shields.io/lgtm/grade/python/github/S1riyS/GravitySimulation)
![Alerts](https://img.shields.io/lgtm/alerts/github/S1riyS/GravitySimulation)

     ██████╗ ██████╗  █████╗ ██╗   ██╗██╗████████╗██╗   ██╗
    ██╔════╝ ██╔══██╗██╔══██╗██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
    ██║  ██╗ ██████╔╝███████║╚██╗ ██╔╝██║   ██║    ╚████╔╝ 
    ██║  ╚██╗██╔══██╗██╔══██║ ╚████╔╝ ██║   ██║     ╚██╔╝  
    ╚██████╔╝██║  ██║██║  ██║  ╚██╔╝  ██║   ██║      ██║   
     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝   ╚═╝      ╚═╝   
    
     ██████╗██╗███╗   ███╗██╗   ██╗██╗      █████╗ ████████╗██╗ █████╗ ███╗  ██╗
    ██╔════╝██║████╗ ████║██║   ██║██║     ██╔══██╗╚══██╔══╝██║██╔══██╗████╗ ██║
    ╚█████╗ ██║██╔████╔██║██║   ██║██║     ███████║   ██║   ██║██║  ██║██╔██╗██║
     ╚═══██╗██║██║╚██╔╝██║██║   ██║██║     ██╔══██║   ██║   ██║██║  ██║██║╚████║
    ██████╔╝██║██║ ╚═╝ ██║╚██████╔╝███████╗██║  ██║   ██║   ██║╚█████╔╝██║ ╚███║
    ╚═════╝ ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚════╝ ╚═╝  ╚══╝

## 📝 About project

[Gravity Simulation](https://github.com/S1riyS/GravitySimulation) is little PyGame project where simulating 
gravitational interaction

## 💡 Usage
To create a "planet", you have to click **Mouse1** and drag the mouse, then you will see a line 
that indicates the direction and speed at which the "planet" will fly. 
Also in the upper right corner it is written with what specific speed the object will fly.

To create star only thing you should do is press **Mouse2**.

In the middle of left side of window you can set mass and color of stars and planets.
Also there you can turn on/off **background grid**, **objects' glow** and **traces of planets**.

*New features will be added later...*

## ⬇ Installation
* First off all you have to install **[Python 3.x](https://www.python.org/)**.

* Then **clone repository** to your local machine. 
To do this write following command in the console:

    `git clone https://github.com/S1riyS/GravitySimulation.git`

* Install all the necessary modules: 

    `pip install -r requirements.txt`

Now you can start `app/main.py` file :
```python
if __name__ == "__main__":
    print('Simulation has been started!')
    game = Game()
    game.run()
```

## 💻 Modules
* **[PyGame](https://pypi.org/project/pygame/)** -  is a free and open-source cross-platform library for 
the development of multimedia applications like video games using Python.
* **[PyGame GUI](https://pygame-gui.readthedocs.io/en/latest/)** - is a module to help you make graphical user interfaces in 
for games written in PyGame.


## 🎞 Preview
![GIF 1](https://i.postimg.cc/pV1b9kpg/Gravity-Simulation-24-10.gif)
![Image 1](https://i.postimg.cc/LskGHcjr/30-10-2021-125222.png)

## 👨‍ Developer
* **[GitHub Profile](https://github.com/S1riyS)**
* **Discord - S1riyS#0261**
* **Email - kirill.ankudinov.94@mail.ru**
