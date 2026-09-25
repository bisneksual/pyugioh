from sqlalchemy import Table, Column, Integer, String, MetaData

md_obj = MetaData()

CardlistTable = Table(
    "cardlist",
    md_obj,
    # BaseCard
    Column("id",Integer,primary_key=True),
    Column("name",String,nullable=False),
    Column("frame",String,nullable=True),
    Column("desc",String,nullable=False),
    Column("race",String,nullable=True),
    Column("set_code",String,nullable=True),
    Column("archetype",String,nullable=True),

    #MonsterCard
    Column("type",String,nullable=True),
    Column("level",Integer,nullable=True),
    Column("atk",Integer,nullable=True),
    Column("def",Integer,nullable=True),

    # Pendulum
    Column("pend_desc",String,nullable=True),
    Column("scale",Integer,nullable=True),

    # Extra Deck
    Column("materials",String,nullable=True),
    
)