Get the same frontend used on Golang url shortener. Change the styling to suit python better.

## How dbs are done in FastAPI / sqlalchemy

    class Base(DeclarativeBase):
    pass

    class User(Base):
        __tablename__: "user"

        id: Mapped[int] = mapped_column(primary_key=True)
        created_at: Mapped[datetime.datetime] = mapped_column(
            server_default=func.now()
        )
        username: Mapped[str] = mapped_column()
        password: Mapped[str] = mapped_column()

    class Url(Base):
        __tablename__: "url"

        id: Mapped[int] = mapped_column(primary_key=True)
        created_at: Mapped[datetime.datetime] = mapped_column(
            server_default=func.now()
        )
        short_url: Mapped[str] = mapped_column()
        long_url: Mapped[str] = mapped_column()

    DATABASE_URL = "sqlite:///test.db"

    engine = create_engine(DATABASE_URL)

    SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @app.on_event("startup")
    async def startup():
        Base.metadata.create_all(bind=engine)

How to test dbs I want write tests for everything
Do an sqlite db. Host server on a container with static html frontend.

## Redirects on FastAPI

    @app.get("/teleport")
    async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

## Middlewares on FastAPI for authmiddleware

    def get_current_user(authorization: str = Header(None)):
        if authorization is None or not validate_authorization(authorization):
            raise HTTPException(status_code=401, detail="Unauthorized")
        user = decode_user_from_auth(authorization)
        return user

    def validate_authorization(auth_header: str) -> bool:
        # Implement your validation logic here
        # Example: Check if the token is valid
        return auth_header == "ValidToken"  # Simplified example

    def decode_user_from_auth(auth_header: str):
        # Decode and return the user based on the authorization header
        # Example: Extract user information from the token
        return "decoded_user"

    app = FastAPI()

    @app.get("/secure")
    def secure_route(user: str = Depends(get_current_user)):
        return {"message": "Hello, Secure World", "user": user}
        
## Jsonwebtoken on FastAPI

    >>> import jwt
    >>> encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
    >>> print(encoded_jwt)
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg
    >>> jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    {'some': 'payload'}

# Example routing stuff

    https://fastapi.tiangolo.com/tutorial/bigger-applications/
    
    @app.post("/items")
    def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Item:
        return db_create_item(item, db)


    @app.get("/items/{item_id}")
    def read_item(item_id: int, db: Session = Depends(get_db)) -> Item:
        try:
            return db_read_item(item_id, db)
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Item not found")


    @app.put("/items/{item_id}")
    def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)) -> Item:
        try:
            return db_update_item(item_id, item, db)
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Item not found")


    @app.delete("/items/{item_id}")
    def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
        try:
            return db_delete_item(item_id, db)
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Item not found")

    Example db stuff

    def db_find_item(item_id: int, db: Session) -> DBItem:
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise NotFoundError()
    return db_item


    def db_create_item(item: ItemCreate, session: Session) -> Item:
        db_item = DBItem(**item.model_dump())
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return Item(**db_item.__dict__)


    def db_read_item(item_id: int, session: Session) -> Item:
        db_item = db_find_item(item_id, session)
        return Item(**db_item.__dict__)


    def db_update_item(item_id: int, session: Session) -> Item:
        db_item = db_find_item(item_id, session)

        for key, value in db_item.__dict__.items():
            setattr(db_item, key, value)

        session.commit()
        session.refresh(db_item)

        return Item(**db_item.__dict__)


    def db_delete_item(item_id: int, session: Session) -> Item:
        db_item = db_find_item(item_id, session)
        session.delete(db_item)
        session.commit()
        return Item(**db_item.__dict__)
