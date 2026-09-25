**Card Models**
BaseCard
- id: int
- name: str
- frame: str
- desc: str
- race: str
- set_code: str
    - nullable
- archetype: str
    - nullable
MonsterCard (inherits BaseCard)
- atk: int
    - defaults to 0
- def: int
    - defaults to -1
- type: str
- 
**Card Sets Table**
- id: int
    - primary key
- name: str
- prefix: str
- price: float
**Setlist Table**
- set_id: int
    - foreign key
- card_id: int
    - foreign key
- setlist_id: str
- rarity: str
**Card Passcodes Table**
- passcode: int
- primary_id: int