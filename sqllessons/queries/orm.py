from sqlalchemy import text, insert, select, func, cast, Integer, and_
from database import sync_engine, async_engine, session_factory, async_session_factory, Base
from models import WorkersOrm, ResumesOrm, Workload


class SyncOrm():
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_bobr = WorkersOrm(username="Bobr")
            worker_volk = WorkersOrm(username="Volk")
            session.add_all([worker_bobr, worker_volk])
            session.flush()
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkersOrm)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Lis"):
        with session_factory() as session:
            worker_volk = session.get(WorkersOrm, worker_id)
            worker_volk.username = new_username
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_volk1 = ResumesOrm(
                title="Python Junior Dev", compensation=50000, workload=Workload.fulltime, worker_id=1
            )
            resume_volk2 = ResumesOrm(
                title="Python Dev", compensation=150000, workload=Workload.fulltime, worker_id=1
            )
            resume_bobr1 = ResumesOrm(
                title="Python Data Engineer", compensation=250000, workload=Workload.parttime, worker_id=2
            )
            resume_bobr2 = ResumesOrm(
                title="Data Scientist", compensation=300000, workload=Workload.fulltime, worker_id=2
            )
            session.add_all([resume_volk1,resume_volk2,resume_bobr1,resume_bobr2])
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        with session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                )
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000)
            )
            result = session.execute(query)
            print(f"{result.all()=}")





# async def insert_data():
#     async with async_session_factory() as session:
#         worker_bobr = WorkersOrm(username="Bobr")
#         worker_volk = WorkersOrm(username="Volk")
#         session.add_all([worker_bobr, worker_volk])
#         await session.commit()




