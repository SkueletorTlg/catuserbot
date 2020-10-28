"""CoronaVirus LookUp
Syntax: .corona <country>"""
from covid import Covid

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(admin_cmd(pattern="covid(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="covid(?: |$)(.*)", allow_sudo=True))
async def corona(event):
    if event.pattern_match.group(1):
        country = event.pattern_match.group(1)
    else:
        country = "World"
    covid = Covid(source="worldometers")
    data = ""
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data += f"\n⚠️Casos Confirmados   : `{hmm1}`"
        data += f"\n😔Casos activos           : `{country_data['active']}`"
        data += f"\n⚰️Muertos         : `{hmm2}`"
        data += f"\n🤕Críticos          : `{country_data['critical']}`"
        data += f"\n😊Recuperados   : `{country_data['recovered']}`"
        data += f"\n💉Prueba total    : `{country_data['total_tests']}`"
        data += f"\n🥺New Casos   : `{country_data['new_cases']}`"
        data += f"\n😟New Muertos : `{country_data['new_deaths']}`"
    else:
        data += "\n¡Aún no hay información sobre este país!"
    await edit_or_reply(
        event,
        "**Información de CoronaVirus en {}:**\n{}".format(country.capitalize(), data),
    )


CMD_HELP.update(
    {
        "covid": "__**PLUGIN NAME :** Covid__\
   \n\n📌** CMD ➥** `.covid ` <country name>\
   \n**USAGE   ➥  **Obtenga información sobre los datos de covid-19 en el país indicado."
    }
)
