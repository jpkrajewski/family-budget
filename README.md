# Description
The application should allow for creating several users. Each user can create a list of
any number of budgets and share it with any number of users. The budget consists of
income and expenses. They are grouped into categories. It is required to create REST or
GraphQL API and a database. The project should contain authorisation, tests, fixtures,
filtering and pagination.

## Installation Docker
```
git clone https://github.com/jpkrajewski/family-budget.git
cd family-budget
make up
```

## Installation with VENV
```
git clone https://github.com/jpkrajewski/family-budget.git
python -m venv {{ venv_name }}
source {{ venv_name }}/bin/activate
cd family-budget
pip install -r requirements.txt
python src/manage.py migrate
python src/manage.py createsuperuser
python src/manage.py runserver
```

## Run tests
```
cd family-budget/src
python manage.py test
```

## Endpoints
![Alt text](images/image.png)


## Autehntication by session
Log to Django
- tester1/123
- tester2/123

## Autehntication by token
```
curl -X POST http://localhost:8000/api-token-auth/ -d '{"username":"tester1", "password":"123"}' -H "Content-Type: application/json"

{"token":"8b353c015bbd098de0deaaed1153e47121b3a62c"}

curl -X GET http://localhost:8000/budgets/ -H 'Authorization: Token 8b353c015bbd098de0deaaed1153e47121b3a62c'

{"count":2,"next":null,"previous":null,"results":[{"owner":"tester1","user":1,"name":"Family Budget 1","shared_with_users":[],"categories":["http://localhost:8000/categories/1/","http://localhost:8000/categories/2/","http://localhost:8000/categories/3/"],"created_at":"2023-10-07T20:43:15.280268Z","url":"http://localhost:8000/budgets/1/"},{"owner":"tester2","user":2,"name":"Fam....
```

## Budgets
Users can create budgets and share it with other users. You can filter by user and name. Pagination is also available. When budget is shared visitor can view every category and financial entry that belongs to this budget.

![Alt text](images/budgets.png)

## Categories
Users can create categories and assign it to budget. You can filter by budget and name. Pagination is also available. There is also a bilans of incomes and expenses.

![Alt text](images/categories.png)

## Financial Entry
Users can create financial entry and assign it to budget and category.

![Alt text](images/entry.png)

## Sharded Budget

![Alt text](images/shared.png)
