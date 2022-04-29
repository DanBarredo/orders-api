from email.policy import HTTP
from http.client import HTTPException
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

'''ORDER MODEL'''


class OrderItems(BaseModel):
    item_id: int
    item_qty: int


class Order(BaseModel):
    order_id: Optional[UUID] = uuid4()
    created_on: datetime = datetime.now()
    estimated_time: datetime
    order_status: Optional[str] = "in-progress"
    delivery_address: str
    billing_address: str
    customer_id: int
    order_items: List[OrderItems]


app = FastAPI()
# test database
db: List[Order] = [
    Order(
        order_id="57e9d4d6-1f12-4c25-8d0b-7a8dfcd228e1",
        estimated_time="2022-04-22T16:00:00",
        order_status="in-progress",
        delivery_address="london",
        billing_address="somewhere in london",
        customer_id=1,
        order_items=[OrderItems(item_id=23, item_qty=1)]
    ),
    Order(
        order_id="0e62d7cf-54ec-4444-92b6-8cdba4f16bf4",
        estimated_time="2022-09-15T15:00:00",
        order_status="delivered",
        delivery_address="london",
        billing_address="somewhere in london",
        customer_id=2,
        order_items=[OrderItems(item_id=4, item_qty=4)]
    ),
    Order(
        order_id="5ba335e8-be4a-41ea-935c-3a2852e274f9",
        estimated_time="2022-04-15T13:00:00",
        order_status="delayed",
        delivery_address="london",
        billing_address="somewhere in london",
        customer_id=3,
        order_items=[OrderItems(item_id=2, item_qty=2),
                     OrderItems(item_id=10, item_qty=10)]
    ),
    Order(
        order_id="1ba335e8-be4a-41ea-935c-3a2852e274f9",
        estimated_time="2022-03-15T13:00:00",
        order_status="delayed",
        delivery_address="london",
        billing_address="somewhere in london",
        customer_id=4,
        order_items=[OrderItems(item_id=3, item_qty=1)]
    )
]

# TODO: verify delayed orders function


def verify_delayed_orders():
    pass


'''API ENDPOINTS'''


@ app.get("/")
async def root():
    return {"message": "Hello World"}


@ app.get("/orders/v1/")
async def get_orders():
    return db


@ app.get("/orders/v1/{order_id}")
async def get_order_by_id(order_id: UUID):
    for order in db:
        if order.order_id == order_id:
            return order.dict()
    raise HTTPException(
        status_code=404,
        detail=f"Order with ID \'{order_id}\' does not exist."
    )


@app.get("/orders/v1/status/delayed")
async def get_delayed_orders():
    delayed = []
    for order in db:
        if order.order_status == "delayed":
            delayed.append(order.dict())
    return delayed


@ app.get("/orders/v1/status/{order_status}")
async def get_orders_by_status(order_status: str):
    statuses = ["in-progress", "delivered", "delayed"]
    if order_status not in statuses:
        raise HTTPException(
            status_code=404,
            detail=f"Order status \'{order_status}\' does not exist."
        )
    orders = []
    for order in db:
        if order.order_status == order_status:
            orders.append(order)
    if len(orders) >= 1:
        return orders
    else:
        raise HTTPException(status_code=204, detail="")


@ app.post("/orders/v1/")
def create_order(order: Order):
    db.append(order)
    return db[-1]

# TODO: patch
# @app.patch("/orders/v1/")
