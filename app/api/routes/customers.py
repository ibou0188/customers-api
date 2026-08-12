from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.db.models import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse


router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customers"]
)


@router.get("/", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=201
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    existing_customer = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    new_customer = Customer(
        firstname=customer.firstname,
        lastname=customer.lastname,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    existing_email = db.query(Customer).filter(
        Customer.email == customer_data.email,
        Customer.id != customer_id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    customer.firstname = customer_data.firstname
    customer.lastname = customer_data.lastname
    customer.email = customer_data.email

    db.commit()
    db.refresh(customer)

    return customer


@router.delete(
    "/{customer_id}",
    status_code=204
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return None
