from .labs import init_lab_categories
from .protocols import init_protocols
from .wings import init_wings
from .mci import init_mci_form


async def startup():
    await init_wings()
    await init_protocols()
    await init_lab_categories()
    await init_mci_form()
