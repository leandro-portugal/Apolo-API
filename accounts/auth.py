from rest_framework.exceptions import AuthenticationFailed, APIException
from django.contrib.auth.hashers import check_password, make_password
from accounts.models import User
from companies.models import Enterprise, Employee


class Authentication:

    def signin(self, email = None, password = None) -> User:
        exception_auth = AuthenticationFailed('E-mail e ou senha incorreto(s)')
        user_exists = User.objects.filter(email = email).exists()

        if not user_exists:
            raise exception_auth
        
        user = User.objects.filter(email = email).first()

        if not check_password(password, user.password):
            raise exception_auth

        return user

    def sigup(self, email,name, password, account_type='owner', company_id = False):

        if not name or name == '':
            raise APIException('O nome deve ser informado')
        
        if not email or email == '':
            raise APIException('O e-mail deve ser informado')
        
        if not password or password == '':
            raise APIException('A senha deve ser informada')
        
        if account_type == 'employee' and not company_id:
            raise APIException('O Id da empresa deve ser informado')
        
        user = User
        if user.objects.filter(email = email).exists():
            raise APIException('Este e-mail já esta cadastrado na plataforma')
        
        password_hashed =  make_password(password)

        created_user = user.objects.create(
            name = name,
            email = email,
            password = password_hashed,
            is_owner = 0 if account_type =='employee' else 1
        )

        if account_type == 'owner':
            created_enterprise = Enterprise.objects.create(
                name = 'Nome da Empresa',
                user_id = created_user.id
            )
        if account_type == 'employee':
            Employee.objects.create(
                enterprise_id = company_id or created_enterprise.id,
                user_id = created_user.id

            )

        return created_user