from dataclasses import dataclass

@dataclass
class SubscriptionType:
    subscription_type_id: int
    name: str
    price: int
    duration_days: int