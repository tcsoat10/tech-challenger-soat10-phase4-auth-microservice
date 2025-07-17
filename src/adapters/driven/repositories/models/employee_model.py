from src.core.domain.entities.employee import Employee
from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.shared.identity_map import IdentityMap

from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.orm import relationship


class EmployeeModel(BaseModel):
    __tablename__ = 'employees'

    admission_date = Column(Date)
    termination_date = Column(Date)

    person_id = Column(ForeignKey('persons.id'), nullable=False)
    person = relationship('PersonModel')

    role_id = Column(ForeignKey('roles.id'), nullable=False)
    role = relationship('RoleModel')

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('UserModel')


    @classmethod
    def from_entity(cls, employee):
        if not employee:
            return None
        
        return cls(
            id=employee.id,
            admission_date=employee.admission_date,
            termination_date=employee.termination_date,
            person_id=employee.person.id,
            role_id=employee.role.id,
            user_id=employee.user.id,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
            inactivated_at=employee.inactivated_at
        )
        
    def to_entity(self):
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(Employee, self.id)
        if existing:
            return existing
        
        person = self._get_person(identity_map)
        role = self._get_role(identity_map)
        user = self._get_user(identity_map)        
        
        employee = Employee(
            id=self.id,
            admission_date=self.admission_date,
            termination_date=self.termination_date,
            person=person,
            role=role,
            user=user,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at
        )
        identity_map.add(employee)
        return employee

    def _get_person(self, identity_map: IdentityMap):
        from src.core.domain.entities.person import Person
        
        existing = identity_map.get(Person, self.person_id)
        if existing:
            return existing
        return self.person.to_entity()
    
    def _get_role(self, identity_map: IdentityMap):
        from src.core.domain.entities.role import Role
        
        existing = identity_map.get(Role, self.role_id)
        if existing:
            return existing
        return self.role.to_entity()

    def _get_user(self, identity_map: IdentityMap):
        from src.core.domain.entities.user import User
        
        existing = identity_map.get(User, self.user_id)
        if existing:
            return existing
        return self.user.to_entity()

__all__ = ['EmployeeModel']
