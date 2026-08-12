from datetime import datetime, timezone

from app.schemas.customer import CustomerCreate, CustomerResponse


customers_db: list[CustomerResponse] = []


def create_customer(customer: CustomerCreate) -> CustomerResponse:
    new_id = len(customers_db) + 1

    new_customer = CustomerResponse(
        id=new_id,
        created_at=datetime.now(timezone.utc),
        **customer.model_dump(),
    )

    customers_db.append(new_customer)

    return new_customer