from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,phone_number,password = None,**extra_fields):
        if not email or not phone_number:
            s = ""
            if not email and not phone_number:
                s = "Email and Phone Number are required!!"
            elif not email:
                s = "Email is required!!"
            else:
                s = "Phone Number is required!!"
            raise ValueError(s)

        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user
    
    def create_superuser(self,email,phone_number,password = None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        return self.create_user(email,phone_number,password,**extra_fields)

