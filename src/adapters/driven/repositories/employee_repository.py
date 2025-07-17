from src.adapters.driven.repositories.models.person_model import PersonModel
from src.adapters.driven.repositories.models.role_model import RoleModel
from src.adapters.driven.repositories.models.user_model import UserModel
from src.adapters.driven.repositories.models.employee_model import EmployeeModel
from src.core.shared.identity_map import IdentityMap
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.domain.entities.employee import Employee

from sqlalchemy.orm import Session
from typing import List


class EmployeeRepository(IEmployeeRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map: IdentityMap = IdentityMap.get_instance()

    def create(self, employee: Employee) -> Employee:
        if employee.id is not None:
            existing = self.identity_map.get(Employee, employee.id)
            if existing:
                self.identity_map.remove(existing)
        
        employee_model = EmployeeModel.from_entity(employee)
        self.db_session.add(employee_model)
        self.db_session.commit()
        self.db_session.refresh(employee_model)
        return employee_model.to_entity()
    
    def get_by_id(self, employee_id: int) -> Employee:
        employee_model = self.db_session.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
        if employee_model is None:
            return None
        return employee_model.to_entity()
    
    def get_by_person_id(self, person_id: int) -> Employee:
        employee_model = self.db_session.query(EmployeeModel).join(EmployeeModel.person).filter(PersonModel.id == person_id).first()
        if employee_model is None:
            return None
        return employee_model.to_entity()
    
    def get_by_user_id(self, user_id: int) -> Employee:
        employee_model = self.db_session.query(EmployeeModel).join(EmployeeModel.user).filter(UserModel.id == user_id).first()
        if employee_model is None:
            return None
        return employee_model.to_entity()
    
    def get_by_role_id(self, role_id: int) -> List[Employee]:
        employee_model = self.db_session.query(EmployeeModel).join(EmployeeModel.role).filter(RoleModel.id == role_id).all()
        return [employee.to_entity() for employee in employee_model]
    
    def get_by_username(self, username: str) -> Employee:
        employee_model = self.db_session.query(EmployeeModel).join(EmployeeModel.user).filter(UserModel.name == username).first()
        if employee_model is None:
            return None
        return employee_model.to_entity()

    def get_all(self, include_deleted: bool = False) -> List[Employee]:
        query = self.db_session.query(EmployeeModel)
        if not include_deleted:
            query = query.filter(EmployeeModel.inactivated_at.is_(None))
        employee_models = query.all()
        return [employee_model.to_entity() for employee_model in employee_models]
    
    def update(self, employee: Employee) -> Employee:
        if employee.id is not None:
            existing = self.identity_map.get(Employee, employee.id)
            if existing:
                self.identity_map.remove(existing)

        employee_model = EmployeeModel.from_entity(employee)
        employee_model.person = PersonModel.from_entity(employee.person)
        employee_model.role = RoleModel.from_entity(employee.role)
        employee_model.user = UserModel.from_entity(employee.user)

        self.db_session.merge(employee_model)
        self.db_session.commit()
        return employee_model.to_entity()
    
    def delete(self, employee_id: int) -> None:
        employee_model = (
            self.db_session
                .query(EmployeeModel)
                .filter(EmployeeModel.id == employee_id)
                .first()
        )
        if employee_model:
            self.db_session.delete(employee_model)
            self.db_session.commit()
            self.identity_map.remove(employee_model)
