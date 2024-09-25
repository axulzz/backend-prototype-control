from rest_framework.exceptions import ValidationError

class ValidationUser:
    def validate_number_phone(self, number):
        errors = []
        
        if number == None:
            errors.append({"number_phone":"El numero de telefono no puede ser nulo"})

        if len(number) != 10:
            errors.append(
                {"'number_phone'": "El numero de telefono debe tener 10 digitos"}
            )
        
        if len(errors) >0:
            raise ValidationError(errors)
        
        return number
    
    def validate_address(self, address):
        if address == None:
            raise ValidationError(["La direccion no puede ser nula"])

        return address
