English | [Russian](https://github.com/S1riyS/GravitySimulation/blob/master/README.ru.md)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

![License](https://img.shields.io/github/license/S1riyS/GravitySimulation)
![Quality](https://img.shields.io/lgtm/grade/python/github/S1riyS/GravitySimulation)
![Alerts](https://img.shields.io/lgtm/alerts/github/S1riyS/GravitySimulation)

![Gravity-Simulation-Logo](https://i.postimg.cc/j2DPRJDC/Gravity-Simulation-Logo.png)
⭐ Star me on GitHub — it motivates me a lot!

## 📝 About project
[Gravity Simulation](https://github.com/S1riyS/GravitySimulation) is little PyGame project where simulating 
gravitational interaction

## 🤔 How it works?
My simulation is based on **2 Newton formulas**:

![Newton's second law](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20%5Ctext%7BNewton%27s%5C%20second%5C%20law:%7D%5Cmathit%7B%5C%20%5Cvec%7Ba%7D%20=%5Cfrac%7B%5Csum%20%5Cvec%7BF%7D%7D%7Bm%7D%7D%7D}&mode=inline)

![Universal gravitation](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20%5Ctext%7BNewton%27s%5C%20law%5C%20of%5C%20universal%5C%20gravitation:%7D%5Cmathit%7B%5C%20%5Coverrightarrow%7BF_%7Bg%7D%7D%20%5C%20=%5C%20G%5Cfrac%7Bm_%7B1%7D%20m_%7B2%7D%7D%7BR%5E%7B2%7D%7D%5Cvec%7BR%7D%7D%7D}&mode=inline)

In this simulation all bodies interact with each other, so formulas are beginning more complicated.

Here is sum of all gravitational forces acting on the body:

![Formula 1](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20%5Csum%20%5Cmathit%7B%5Coverrightarrow%7B%5Cmathit%7B%7B%5Cdisplaystyle%20F_%7Bg%7D%7D%7D%7D%20%5C%20=%7B%5Cdisplaystyle%20%5Csum%20_%7Bi=1%7D%5E%7Bn%7D%20G%5Cfrac%7Bm_%7Bobj%7D%20*m_%7Bi%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%5Coverrightarrow%7BR_%7Bi%7D%7D%7D%7D%7D})

Then take out *G (gravitational const)* and 
*![Object's mass](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20m_%7Bobj%7D%7D}) 
(object's mass)* from under the sign of sum:

![Formula 2](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20%5Csum%20%5Cmathit%7B%5Coverrightarrow%7B%5Cmathit%7B%7B%5Cdisplaystyle%20F_%7Bg%7D%7D%7D%7D%20%5C%20=Gm_%7Bobj%7D%7D%5Csum%20_%7B%20%5Cbegin%7Barray%7D%7Bl%7D%20i=1%5C%5C%20%5Cend%7Barray%7D%7D%5E%7Bn%7D%5Cmathit%7B%5Cfrac%7Bm_%7Bi%7D%5Cmathit%7B%7B%5Cdisplaystyle%20%5Coverrightarrow%7BR_%7Bi%7D%7D%7D%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%7D%7D})

Finally, we can unite formulas:

![Uniting formulas](https://render.githubusercontent.com/render/math?math={\large\color{white}\%5Cmathit%7B%7B%5Cdisplaystyle%20%5Coverrightarrow%7Ba_%7Bobj%7D%7D%20=%5Cfrac%7B%5Csum%20%5Cvec%7BF%7D%7D%7Bm_%7Bobj%7D%7D%20%5C%20=%5Cfrac%7B%5Cmathit%7BGm_%7Bobj%7D%7B%5Cdisplaystyle%20%5Csum%20_%7B%20%5Cbegin%7Barray%7D%7Bl%7D%20i=1%5C%5C%20%5Cend%7Barray%7D%7D%5E%7Bn%7D%7D%5Cfrac%7Bm_%7Bi%7D%5Cmathit%7B%5Coverrightarrow%7BR_%7Bi%7D%7D%20%5C%20%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%7D%7D%7Bm_%7Bobj%7D%7D%20=G%5Csum%20_%7B%20%5Cbegin%7Barray%7D%7Bl%7D%20i=1%5C%5C%20%5Cend%7Barray%7D%7D%5E%7Bn%7D%5Cfrac%7Bm_%7Bi%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%20*%5Coverrightarrow%7BR_%7Bi%7D%7D%7D%7D})

And the final formula is:

![Final formula](https://render.githubusercontent.com/render/math?math={\Large\color{white}\%7B%5Cdisplaystyle%20%5Cmathit%7B%5Coverrightarrow%7Ba_%7Bobj%7D%7D%7D%20=%5Cmathit%7BG%5Csum%20_%7B%20%5Cbegin%7Barray%7D%7Bl%7D%20i=1%5C%5C%20%5Cend%7Barray%7D%7D%5E%7Bn%7D%5Cfrac%7Bm_%7Bi%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%20*%5Coverrightarrow%7BR_%7Bi%7D%7D%7D%7D})

To see how it works in the code go to to the *Planet's class*
[`update_position(self, dt)`](https://github.com/S1riyS/GravitySimulation/blob/master/app/objects.py#L161) function
in [`app/objects.py`](https://github.com/S1riyS/GravitySimulation/blob/master/app/objects.py) 

## 💡 Usage
To create a "planet", you have to click **Mouse1** and drag the mouse, then you will see a line 
that indicates the direction and speed at which the "planet" will fly. 
Also in the upper right corner it is written with what specific speed the object will fly.

To create star only thing you should do is press **Mouse2**.

**In settings you can**: 
* Set mass and color of stars and planets.
* Turn on/off **background grid**, **objects' glow** and **traces of planets**.
* Pause/Continue or speed up (2X, 3X) simulation 
* Restart simulation

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
![Image 1](https://i.postimg.cc/9QFPWkWm/06-11-2021-132003.png)

## 👨‍ Developer
* **[GitHub Profile](https://github.com/S1riyS)**
* **Discord - S1riyS#0261**
* **[VK - Kirill Ankudinov](https://vk.com/s1riys)**
* **Email - kirill.ankudinov.94@mail.ru**
