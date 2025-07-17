class IsCustomerUsecase:
    @classmethod
    def is_customer(cls, current_user: dict) -> bool:
        return current_user['profile']['name'] in ['customer']