from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, Enum, create_engine, MetaData, select, inspect

if __name__=="__main__":
    ngin = create_engine("sqlite:///db/pygo.db",echo=True)
    session = sessionmaker(bind=ngin).Session()

    md_obj = MetaData()
    card = BaseCard(
        name="Baby Dragon",
        passcode=88819587,
        frame="",
        desc="Much more powerful than just a child, this dragon is gifted with untappeed power.",
        race=None
    )

    orm_card = CardListRow(**card.model_dump())
    print(orm_card.name)

    CardListRow.metadata.drop_all(ngin,checkfirst=True)

    CardListRow.metadata.create_all(ngin)

    print(inspect(ngin).get_table_names())
    
    session.add(card)
    session.commit()

    for row in session.query(CardListRow).all():
        print(row.id,":",row.name, ",", row.desc)