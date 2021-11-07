[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

![License](https://img.shields.io/github/license/S1riyS/GravitySimulation)
[![PEP8](https://img.shields.io/badge/code%20style-PEP8-green?logo=python&logoColor=fff)](https://www.python.org/dev/peps/pep-0008/)
![Quality](https://img.shields.io/lgtm/grade/python/github/S1riyS/GravitySimulation?logo=LGTM)
![Alerts](https://img.shields.io/lgtm/alerts/github/S1riyS/GravitySimulation?logo=LGTM)
![Last commit](https://img.shields.io/github/last-commit/S1riyS/GravitySimulation?logo=GitHub)
![GitHub repo size](https://img.shields.io/github/repo-size/S1riyS/GravitySimulation)

![Gravity-Simulation-Logo](https://i.postimg.cc/j2DPRJDC/Gravity-Simulation-Logo.png)

*Документация на других языках: 
[English](https://github.com/S1riyS/GravitySimulation/blob/master/README.md), 
[Русский](https://github.com/S1riyS/GravitySimulation/blob/master/README.ru.md)*

## 📝 О проекте
**[GravitySimulation](https://github.com/S1riyS/GravitySimulation)** - это небольшой проект, 
в котором стимулируется гравитационное взаимодействие.

## 🤔 Как это работает?
Моя симуляция основана на **двух формулах Ньютона**:

![Newton's second law](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20%5Ctext%7BNewton%27s%5C%20second%5C%20law:%7D%5Cmathit%7B%5C%20%5Cvec%7Ba%7D%20=%5Cfrac%7B%5Csum%20%5Cvec%7BF%7D%7D%7Bm%7D%7D%7D}&mode=inline)

![Universal gravitation](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20%5Ctext%7BNewton%27s%5C%20law%5C%20of%5C%20universal%5C%20gravitation:%7D%5Cmathit%7B%5C%20%5Coverrightarrow%7BF_%7Bg%7D%7D%20%5C%20=%5C%20G%5Cfrac%7Bm_%7B1%7D%20m_%7B2%7D%7D%7BR%5E%7B2%7D%7D%5Cvec%7BR%7D%7D%7D}&mode=inline)

Сумма всех гравитационных сил, действующих на тело:

![Formula 1](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20%5Csum%20%5Cmathit%7B%5Coverrightarrow%7B%5Cmathit%7B%7B%5Cdisplaystyle%20F_%7Bg%7D%7D%7D%7D%20%5C%20=%7B%5Cdisplaystyle%20%5Csum%20_%7Bi=1%7D%5E%7Bn%7D%20G%5Cfrac%7Bm_%7Bobj%7D%20*m_%7Bi%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%5Coverrightarrow%7BR_%7Bi%7D%7D%7D%7D%7D})

Вынесем за скобки **G** и 
![Object's mass](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20m_%7Bobj%7D%7D}):

![Formula 2](https://render.githubusercontent.com/render/math?math={\large\color{white}\%7B%5Cdisplaystyle%20%5Csum%20%5Cmathit%7B%5Coverrightarrow%7B%5Cmathit%7B%7B%5Cdisplaystyle%20F_%7Bg%7D%7D%7D%7D%20%5C%20=Gm_%7Bobj%7D%7D%5Csum%20_%7B%20%5Cbegin%7Barray%7D%7Bl%7D%20i=1%5C%5C%20%5Cend%7Barray%7D%7D%5E%7Bn%7D%5Cmathit%7B%5Cfrac%7Bm_%7Bi%7D%5Cmathit%7B%7B%5Cdisplaystyle%20%5Coverrightarrow%7BR_%7Bi%7D%7D%7D%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%7D%7D})

Наконец мы можем объединить формулы:

![Uniting formulas](https://render.githubusercontent.com/render/math?math={\large\color{white}\%5Cmathit%7B%7B%5Cdisplaystyle%20%5Coverrightarrow%7Ba_%7Bobj%7D%7D%20=%5Cfrac%7B%5Csum%20%5Cvec%7BF%7D%7D%7Bm_%7Bobj%7D%7D%20%5C%20=%5Cfrac%7B%5Cmathit%7BGm_%7Bobj%7D%7B%5Cdisplaystyle%20%5Csum%20_%7B%20%5Cbegin%7Barray%7D%7Bl%7D%20i=1%5C%5C%20%5Cend%7Barray%7D%7D%5E%7Bn%7D%7D%5Cfrac%7Bm_%7Bi%7D%5Cmathit%7B%5Coverrightarrow%7BR_%7Bi%7D%7D%20%5C%20%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%7D%7D%7Bm_%7Bobj%7D%7D%20=G%5Csum%20_%7B%20%5Cbegin%7Barray%7D%7Bl%7D%20i=1%5C%5C%20%5Cend%7Barray%7D%7D%5E%7Bn%7D%5Cfrac%7Bm_%7Bi%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%20*%5Coverrightarrow%7BR_%7Bi%7D%7D%7D%7D})

И в результате мы получаем:

![Final formula](https://render.githubusercontent.com/render/math?math={\Large\color{white}\%7B%5Cdisplaystyle%20%5Cmathit%7B%5Coverrightarrow%7Ba_%7Bobj%7D%7D%7D%20=%5Cmathit%7BG%5Csum%20_%7B%20%5Cbegin%7Barray%7D%7Bl%7D%20i=1%5C%5C%20%5Cend%7Barray%7D%7D%5E%7Bn%7D%5Cfrac%7Bm_%7Bi%7D%7D%7BR_%7Bi%7D%5E%7B2%7D%7D%20*%5Coverrightarrow%7BR_%7Bi%7D%7D%7D%7D})

Чтобы увидеть как все это работает в коде, перейдите к функции
[`update_position(self, dt)`](https://github.com/S1riyS/GravitySimulation/blob/master/app/objects.py#L161)
в файле [`app/objects.py`](https://github.com/S1riyS/GravitySimulation/blob/master/app/objects.py) 

## 💡 Использование
Чтобы создать *"планету"*, кликните на **Mouse1** и перетащите мышь, тогда вы увидите линию, 
которая показывает направление и скорость с которой полетит *"планета"*. 
Также, в правом верхнем улгу будет написанно, с какой конкретно скоростью полетит объект

Чтобы создать *"звезду"*, единственное что вам нужно сделать - это нажать **Mouse2**.

**В настройках вы можете**: 
* Настроить массу и цвет звезд и планет.
* Включать/Выключать **фоновую сетку**, **свечение объектов** и **след, который оставляют планеты**.
* Поставить на паузу/Продолжить или увеличить скорость (2X, 3X) симуляции 
* Перезапустить симуляцию

*Новые возможности будут добавлены позднее...*

## ⬇ Установка
* Прежде всего нужно установить **[Python 3.x](https://www.python.org/)**.

* Затем **клонировать этот репозиторый** к себе на ПК. 
Чтобы сделать это, пропишите следующую команду в консоль:

    `git clone https://github.com/S1riyS/GravitySimulation.git`

* Установите все необходимые модули: 

    `pip install -r requirements.txt`

Теперь вы можете запустить файл `app/main.py` :
```python
if __name__ == "__main__":
    print('Simulation has been started!')
    game = Game()
    game.run()
```

## 💻 Модули
* **[PyGame](https://pypi.org/project/pygame/)** -  это бесплатная кроссплатформенная библиотека 
с открытым исходным кодом для разработки мультимедийных приложений, 
таких как видеоигры, с использованием Python.
* **[PyGame GUI](https://pygame-gui.readthedocs.io/en/latest/)** - это модуль, который поможет вам 
создавать GUI для игр, написанных на PyGame.


## 🎞 Предпросмотр:
![GIF 1](https://i.postimg.cc/pV1b9kpg/Gravity-Simulation-24-10.gif)
![Image 1](https://i.postimg.cc/9QFPWkWm/06-11-2021-132003.png)

## 👨‍ Разработчик
* **[GitHub Profile](https://github.com/S1riyS)**
* **Discord - S1riyS#0261**
* **[ВК](https://vk.com/s1riys)**
* **Email - kirill.ankudinov.94@mail.ru**
