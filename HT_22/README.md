# Tasks:
## HT #22
Базуючись на попередній ДЗ, реалізувати наступний функціонал:

1. Додати Django REST Framework в свій магазин для всих своїх моделей.
   1. Уточнення по моделям:
   2. Модель категорії - тільки `ListView` Модель Продукта - `ListView + Update / Delete`, додати валідацію на апдейт / деліт продукта - його може зробити тільки суперюзер. `(authentication_classes = (authentication.SessionAuthentication, ) )`
2. Додавання до корзини, зміну кількості, очищення корзини або видалення одного продукта з неї 
   зробити з використанням ajax запитів.
# Solution:

[//]: # (Form and access:)

[//]: # (![products]&#40;docs/img/1.png&#41;)

[//]: # (![img.png]&#40;docs/img/4.png&#41;)

[//]: # (User:)

[//]: # (![products]&#40;docs/img/2.png&#41;)

[//]: # (User:)

[//]: # (![products]&#40;docs/img/3.png&#41;)

[//]: # (Superuser:)

[//]: # (![products]&#40;docs/img/5.png&#41;)