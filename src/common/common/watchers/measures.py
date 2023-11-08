from common.data_models.base import Mode, AtomicUpdate
from common.data_models.measures import Effect
from common.data_models.medication import Medication
from common.data_models.patient import Patient


@Patient.watcher.callback('treatment', 'medications', '.*', mask=Mode.mask_new)
async def handle_treatment_medications_change_measures(new: Patient, new_value: Medication):
    if new_value.given:
        async for effect in AtomicUpdate.get_connection().get_medication_effects(new_value.label):
            if not (measure := getattr(new.measures, effect.measure)).effect or measure.effect.at_ < new_value.given_:
                getattr(new.measures, effect.measure).effect = Effect(
                    kind=effect.kind,
                    label=new_value.description,
                    at=new_value.given
                )
