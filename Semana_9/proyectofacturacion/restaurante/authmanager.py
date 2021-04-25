from django.contrib.auth.models import BaseUserManager


class UsuarioManager(BaseUserManager):
    """Clase que sirve para modifcar el comportamiento del modelo Auth del proyecto de django """
    def create_user(self, email, nombre, apellido, tipo, password= None):
        """Creacion de un usuario comun y corriento"""
        if not email:
            #el raise es similar al return solo q se retornara si hay un error
            raise ValueError("El usuario debe tener obligatoria mente un correo")
        # normalizo el email que aparte de validar si hay un @ y un . esta funcionalidad lo lleva todo a lowecase
        # y quita todo los espacion que pudiesen haber
        email = self.normalize_email(email)
        # creo mi objeto de usuario pero aun no lo guardo en la bd
        usuario = self.model(personalCorreo = email, personalNombre = nombre,
                            personalApellido=apellido, personalTipo=tipo   )
        # ahora encriptamos la contraseña
        usuario.set_password(password)
        #guardamos en la bd
        usuario.save(using=self._db) # sirve para refenciar a la bd en el caso tengamos varias bd
        return usuario

    def create_superuser(self, personalCorreo, personalNombre, personalApellido, personalTipo, password):
        """ Creacion de un nuevo suoer usuario para que pueda acceder al panel administrativo  y algunas opciones adicionales """
        usuario = self.create_user(personalCorreo, personalNombre, personalApellido, personalTipo, password)
        # ahora como es un super usuario y para que pueda ingresar al panel administrativo tenemos que designar sus permisos
        # este campo se crea  automaticamente por la herencia del user model
        usuario.is_superuser = True # sirve para poder manipular a otros usuarios y tener permisos exclusivos en el panel administrativo
        usuario.is_taff = True
        usuario.save(using=self._db)