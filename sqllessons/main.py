import os
import sys
import asyncio
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import SyncCore
from queries.orm import SyncOrm


SyncOrm.create_tables()
SyncOrm.insert_workers()

# SyncCore.select_workers()
# SyncCore.update_worker()

# SyncOrm.select_workers()
# SyncOrm.update_worker()

SyncOrm.insert_resumes()
SyncOrm.select_resumes_avg_compensation()