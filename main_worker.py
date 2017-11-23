import redis
from dask import delayed
from dask.distributed import Client, as_completed, wait

from DataFrameHandler import chunker
from MetaReader.reader import meta_studies
from Dasktest import funcs as operation

client = Client('127.0.0.1:44923')


def main():

    # returns 'study' object with metadata as attributes
    studies, prefs = meta_studies(path="../config.json")

    def study_tasker(study):
        chnk_iterator = client.submit(chunker.init, study, pickle=False)
        corr_chnk = client.map(operation.check_n_correct, chnk_iterator)
        lift_chnk = client.map(operation.liftover, corr_chnk)
        ref_chnk = client.map(operation.reference, lift_chnk)
        client.map(operation.write_db, ref_chnk)

    start = client.map(study_tasker, studies)

    db = redis.StrictRedis(db=8)
    print(db.dbsize())


def alt_main():

    studies, prefs = meta_studies(path="../config.json")

    study = studies[0]

    chnk_iterator = chunker.init(study, pickle=False)
    corr_chnk = client.map(operation.check_n_correct, chnk_iterator)

    lift_chnk = client.map(operation.liftover, corr_chnk)
    ref_chnk = client.map(operation.reference, lift_chnk)

    for future in as_completed(ref_chnk):
        print(future)
        chnk = future.result()
        db_submit = client.submit(operation.write_db, chnk)

    db = redis.StrictRedis(db=8)
    print(db.dbsize())


def dif_main():
    # returns 'study' object with metadata as attributes
    studies, prefs = meta_studies(path="../config.json")

    for study in studies:
        chnk_iterator = chunker.init(study, pickle=False)
        corr_chnk = delayed(operation.check_n_correct)(chnk_iterator)
        lift_chnk = delayed(operation.liftover)(corr_chnk)
        ref_chnk = delayed(operation.reference)(lift_chnk)
        db_insert = delayed(operation.write_db)(ref_chnk)

    db_insert.compute()

    db = redis.StrictRedis(db=8)
    print(db.dbsize())


def add_main():
    # returns 'study' object with metadata as attributes
    studies, prefs = meta_studies(path="../config.json")

    for study in studies:
        chnk_iterator = chunker.init(study, pickle=False)
        for chnk in chnk_iterator:
            corr_chnk = operation.check_n_correct(chnk)
            lift_chnk = operation.liftover(corr_chnk)
            ref_chnk = operation.reference(lift_chnk)
            operation.write_db( ref_chnk)

    db = redis.StrictRedis(db=8)
    print(db.dbsize())


def an_main():

    studies, prefs = meta_studies(path="../config.json")
    indices = [[2,5,6],[1,3,4]]

    for study, idx in zip(studies, indices):
        print(idx)
        chnk_iterator = chunker.init(study, pickle=False)
        corr_chnk = client.map(operation.check_n_correct, chnk_iterator)

        lift_chnk = client.map(operation.liftover, corr_chnk)
        ref_chnk = client.map(operation.reference, lift_chnk)

        for future in as_completed(ref_chnk):
            print(future)
            chnk = future.result()
            client.submit(operation.write_db, chnk)

    db = redis.StrictRedis(db=8)
    print(db.dbsize())


def betameain():
    studies, prefs = meta_studies(path="../config.json")
    indices = [[2, 5, 6], [1, 3, 4]]

    for study, idx in zip(studies, indices):
        print(idx)
        chnk_iterator = chunker.init(study, pickle=False)
        corr_chnk = client.map(operation.check_n_correct, chnk_iterator)


def flush_db():
    db = redis.StrictRedis(db=8)
    db.flushdb()

flush_db()
dif_main()
