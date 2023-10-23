from enum import Enum

MCI_DEPARTMENT = 'mci'


class MCIIntakeWing(int, Enum):
    intake = 10
    intake_red = 9
    intake_yellow = 8
    intake_green = 7
    operating_room = 6
    er_imaging = 5
    imaging_department = 4


MCI_NAMES = {
    MCIIntakeWing.intake: 'מלרד חירום',
    MCIIntakeWing.intake_red: 'אדום - חדר הלם',
    MCIIntakeWing.intake_yellow: 'צהוב - אגף 3',
    MCIIntakeWing.intake_green: 'ירוק - אגף 4',
    MCIIntakeWing.operating_room: 'חדר ניתוח',
    MCIIntakeWing.er_imaging: 'דימות חדר מיון',
    MCIIntakeWing.imaging_department: 'אגף דימות',
}
MCI_COLORS = {
    MCIIntakeWing.intake_red: 'red',
    MCIIntakeWing.intake_yellow: '#faad14',
    MCIIntakeWing.intake_green: 'green',
}
