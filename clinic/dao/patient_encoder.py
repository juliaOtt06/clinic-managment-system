import json
from clinic.patient import Patient

class PatientEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Patient):
            return {
                '__type__': 'Patient',
                'phn': obj.phn,
                'name': obj.name,
                'dob': obj.birth_date,
                'phone': obj.phone,
                'email': obj.email,
                'address': obj.address
            }
        return super().default(obj)
            