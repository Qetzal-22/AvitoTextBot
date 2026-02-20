from aiogram.fsm.state import State, StatesGroup


class RegisterUser(StatesGroup):
    username = State()

# + Car make
# + Model
# + Year of manufacture
# + Mileage
# + Number of owners
# + Number of accidents
# + Body condition
# + Engine condition
# + Equipment
# + Reason for sale
# + Additional
class GetDataForCar(StatesGroup):
    car_make = State()
    model = State()
    year_manufacture = State()
    mileage = State()
    count_owner = State()
    count_accidents = State()
    body_condition = State()
    engine_condition = State()
    equipment = State()
    reason_for_sale = State()
    additional = State()
