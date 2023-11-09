from enum import Enum

MCI_DEPARTMENT = 'mci'


class MCIIntakeWing(int, Enum):
    intake_red = 30
    intake_yellow = 29
    intake_green = 28
    er_imaging = 27
    operating_room = 26
    general_imaging = 25
    intensive_care = 24
    cardiac_intensive_care = 23
    trauma_unit = 22
    surgical_b = 21
    surgical_c = 20
    neurosurgical = 19
    orthopedics_a = 18
    orthopedics_b = 17
    hand_palm = 16
    mouth_and_jaw = 15
    ent = 14
    urology = 13
    cardiovascular = 12
    pediatric = 11
    pediatric_icu = 10
    internal_medicine_a = 9
    internal_medicine_b = 8
    internal_medicine_c = 7
    internal_medicine_d = 6
    internal_medicine_e = 5
    internal_medicine_f = 4
    internal_medicine_i = 3


MCI_INTAKE_MAPPING = {
    '30': str(MCIIntakeWing.intake_red.name),
    '29': str(MCIIntakeWing.intake_yellow.name),
    '28': str(MCIIntakeWing.intake_green.name),
    '17': str(MCIIntakeWing.intake_red.name),
    '3': str(MCIIntakeWing.intake_yellow.name),
    '20': str(MCIIntakeWing.intake_green.name),
}

MCI_NAMES = {
    MCIIntakeWing.intake_red: 'אדום - חדר הלם',
    MCIIntakeWing.intake_yellow: 'צהוב - אגף 3',
    MCIIntakeWing.intake_green: 'ירוק - אגף 4',
    MCIIntakeWing.operating_room: 'חדר ניתוח',
    MCIIntakeWing.er_imaging: 'הדמייה במלר"ד',
    MCIIntakeWing.general_imaging: 'אתר בירורים - מושהים',
    MCIIntakeWing.intensive_care: 'טיפול נמרץ כללי',
    MCIIntakeWing.cardiac_intensive_care: 'טיפול נמרץ לב',
    MCIIntakeWing.trauma_unit: 'יחידת הטראומה',
    MCIIntakeWing.surgical_b: 'כירוגיה ב',
    MCIIntakeWing.surgical_c: 'כירוגיה ג',
    MCIIntakeWing.neurosurgical: 'נוירוכירוגיה',
    MCIIntakeWing.orthopedics_a: 'אורתופדיה א',
    MCIIntakeWing.orthopedics_b: 'אורתופדיה ב',
    MCIIntakeWing.hand_palm: 'כף יד',
    MCIIntakeWing.mouth_and_jaw: 'פה ולסת',
    MCIIntakeWing.ent: 'אף אוזן גרון',
    MCIIntakeWing.urology: 'אורולוגיה',
    MCIIntakeWing.cardiovascular: 'חזה וכלי דם',
    MCIIntakeWing.pediatric: 'ילדים',
    MCIIntakeWing.pediatric_icu: 'טיפול נמרץ ילדים',
    MCIIntakeWing.internal_medicine_a: 'פנימית א',
    MCIIntakeWing.internal_medicine_b: 'פנימית ב',
    MCIIntakeWing.internal_medicine_c: 'פנימית ג',
    MCIIntakeWing.internal_medicine_d: 'פנימית ד',
    MCIIntakeWing.internal_medicine_e: 'פנימית ה',
    MCIIntakeWing.internal_medicine_f: 'פנימית ו',
    MCIIntakeWing.internal_medicine_i: 'פנימית ט',
}

MCI_COLORS = {
    MCIIntakeWing.intake_red: 'red',
    MCIIntakeWing.intake_yellow: '#faad14',
    MCIIntakeWing.intake_green: 'green',
}
