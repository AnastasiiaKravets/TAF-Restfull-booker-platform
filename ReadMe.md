Оскільки DummyJSON — це суто фейковий (mocked) API, де операції POST, PUT, DELETE лише імітують відповідь сервера (
повертають ID та передане тіло, але не зберігають зміни в базі), класичний підхід до E2E-тестування (Create -> Get ->
Update -> Delete) тут не спрацює.

Для Senior-рівня це чудовий шанс продемонструвати Contract Testing (валідацію схем), тестування бізнес-логіки обробки
відповідей та валідацію HTTP-статусів і крайових значень.

https://github.com/mwinteringham/restful-booker-platform/tree/trunk
https://automationintesting.online/api/auth/swagger-ui/index.html