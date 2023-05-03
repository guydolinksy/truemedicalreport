from fastapi import APIRouter, Body

from backend.logics.utils import post_dal_json, fetch_dal_json
from backend.routes.patient import logger
from common.data_models.patient import PatientInfoPluginConfig

plugins_router = APIRouter()


@plugins_router.post("/register")
async def register_plugin(plugin: PatientInfoPluginConfig = Body(..., embed=True)):
    current = await post_dal_json("/config/get", dict(key='plugins', default={}))
    if plugin.key not in current['value']:
        await post_dal_json("/config/set", dict(
            key='plugins',
            version=current['version'] + 1 if current['version'] is not None else 0,
            value={plugin.key: plugin.dict(exclude={'key'}), **current['value']},
        ))


async def get_plugins(patient, user, user_settings_):
    user_plugins = getattr(user_settings_, "plugins", {})
    data = {}
    for key, config in (await post_dal_json("/config/get", dict(key='plugins', default={})))['value'].items():
        try:
            if not user_plugins.get(key, {}).get("enabled", True):
                continue
            config = PatientInfoPluginConfig(key=key, **config)

            if config.api_version not in data:
                data[config.api_version] = await fetch_dal_json(f"/patients/{patient}/plugins/{config.api_version}")

            yield config.render(token=user.plugin_token, **data[config.api_version])
        except:
            logger.exception("Plugin Evaluation Failed")
