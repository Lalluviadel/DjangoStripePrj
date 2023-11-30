<p><a name="readme-top"></a></p>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">Django Stripe Task</h1>

  <p align="center">
    Test simple Django App: Web application for Stripe features checking.
  </p>
</div>



<!-- ABOUT THE PROJECT -->
### About
<p><a name="about"></a></p>
Приложение предназначено для взаимодействия с платежной платформой Stripe.
Можно осуществлять оплату одной позиции или их совокупности (заказ).
При успешной оплате или возникновении проблем статус заказа изменяется (вебхук).

Для наглядности оснащено тестовыми данными для проверки 
работоспособности. В админ-панели доступны для взаимодйствия
сущности Item, Discount, Tax, Order.

![Example Screen Shot](https://github.com/Lalluviadel/DjangoStripePrj/blob/master/public/example.png?raw=true)


### Usage
<p><a name="usage"></a></p>

Для заполнения базы данных и тестирования приложения используйте команду:

```
python manage.py fill_db
```

Для запуска приложения и проверки корректности его работы выполните команду:

```
python manage.py runserver
```

Эндпойнты для тестирования приложения:

```
http://127.0.0.1:8000/item/1/
http://127.0.0.1:8000/item/2/
...
http://127.0.0.1:8000/item/6/

http://127.0.0.1:8000/order/1/
http://127.0.0.1:8000/order/2/
```

### Built With
<p><a name="built-with"></a></p>

[![Python][Python logo]][Python url]
[![Django][Django logo]][Django url]
[![Stripe][Stripe logo]][Stripe url]
[![SQLite][SQLite logo]][SQLite url]

<!-- CONTACT -->
### Contact
<p><a name="contact"></a></p>

Marina Marmalyukova - inspiracion@yandex.ru

Project Link: [https://github.com/Lalluviadel/DjangoStripePrj](https://github.com/Lalluviadel/DjangoStripePrj)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python logo]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python url]: https://www.python.org/?hl=RU
[Django logo]: https://img.shields.io/badge/Django-07405E?style=for-the-badge&logo=Django&logoColor=white
[Django url]: https://docs.djangoproject.com/
[Stripe logo]: https://img.shields.io/badge/Stripe-074345?style=for-the-badge&logo=Stripe&logoColor=white
[Stripe url]: https://stripe.com/docs
[SQLite logo]: https://img.shields.io/badge/SQLite-079854?style=for-the-badge&logo=SQLite&logoColor=white
[SQLite url]: https://www.sqlite.org/docs.html
