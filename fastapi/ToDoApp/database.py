from sqlalchemy import create_engine #create_engine: Veritabanı ile bağlantıyı kurar
from sqlalchemy.orm import sessionmaker #sessionmaker: Veritabanı ile etkileşim kurmak için session (oturum) oluşturur.
from sqlalchemy.ext.declarative import declarative_base #declarative_base: ORM taban sınıfıdır. Tüm modeller (tabloları temsil eden Python class’ları) bundan türetilir.

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

#Kullanılacak veritabanının adresini belirtir.
#'sqlite:///.todos.db' → Aynı klasörde todos.db adında bir SQLite veritabanı dosyası oluşturur veya kullanır.

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread': False})
#engine: Veritabanına bağlanmayı sağlayan motor (connection pool + driver).
#check_same_thread=False: SQLite için özel bir parametre.
#Normalde SQLite, aynı thread dışından erişime izin vermez.
#Bu ayarla, uygulama çoklu thread’lerde çalışırken de bağlantı kullanılabilir hale gelir.


SessionLocal = sessionmaker(autocommit = False, autoflush=False,bind=engine)
#sessionmaker: Veritabanı ile işlem yapmamızı sağlayan Session nesnesi üretir.
#autocommit=False: İşlemler otomatik commit edilmez → sen commit() çağırmazsan DB’de kalıcı olmaz.
#autoflush=False: ORM nesneleri her işlemde otomatik flush edilmez, yani veriler daha kontrollü işlenir.
#bind=engine: Bu session hangi veritabanına bağlı çalışacak → engine üzerinden DB’ye bağlanır.

#Uygulamada SessionLocal() çağırarak yeni bir session açarız, db.add(...) veya db.query(...) gibi işlemleri session üstünden yaparız.

#Flush ne demek
#Flush, SQLAlchemy’nin session içindeki değişiklikleri (INSERT, UPDATE, DELETE) veritabanına göndermesi işlemidir.
#flush demek commit demek değildir.
#Yani flush olduğunda:SQLAlchemy, session’da yaptığın değişiklikleri SQL cümleleri olarak veritabanına yollar.
#Ama transaction henüz kapanmaz, rollback yaparsan geri alınabilir.


Base =declarative_base()
#SQLAlchemy’de tabloları temsil eden sınıflar (ORM modelleri) bu Base’den türetilir.