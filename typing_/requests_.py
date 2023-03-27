from .types_ import FriendlyDict


class RequestMetaInterfaces(FriendlyDict):
    screen: dict
    account_linking: dict
    audio_player: dict


class Meta(FriendlyDict):
    locale: str
    timezone: str
    client_id: str
    interfaces: RequestMetaInterfaces


class RequestField(FriendlyDict):
    type: str
    command: str


class User(FriendlyDict):
    user_id: str
    access_token: str


class Application(FriendlyDict):
    application_id: str


class Session(FriendlyDict):
    message_id: int
    session_id: str
    skill_id: str
    user_id: str
    user: User
    application: Application
    new: bool


class YaSessionState(FriendlyDict):
    value: int


class YaUserState(FriendlyDict):
    value: int


class YaApplicationState(FriendlyDict):
    value: int


class YaState(FriendlyDict):
    session: YaSessionState
    user: YaUserState
    application: YaApplicationState


class AliceUserRequest(FriendlyDict):
    meta: Meta
    request: RequestField
    session: Session
    state: YaState
    version: str


class RespCard(FriendlyDict):
    type: str
    image_id: str
    title: str
    description: str


class RespButton(FriendlyDict):
    title: str
    hide: bool


class Response(FriendlyDict):
    text: str
    card: RespCard
    buttons: list[RespButton]


# req = AliceUserRequest('''{
#   "meta": {
#     "locale": "ru-RU",
#     "timezone": "Europe/Moscow",
#     "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
#     "interfaces": {
#       "screen": {},
#       "account_linking": {},
#       "audio_player": {}
#     }
#   },
#   "request": {
#     "type": "..."
#   },
#   "session": {
#     "message_id": 0,
#     "session_id": "2eac4854-fce721f3-b845abba-20d60",
#     "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
#     "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8",
#     "user": {
#       "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
#       "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT"
#     },
#     "application": {
#       "application_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8"
#     },
#     "new": true
#   },
#   "state": {
#     "session": {
#       "value": 10
#     },
#     "user": {
#       "value": 42
#     },
#     "application": {
#       "value": 37
#     }
#   },
#   "version": "1.0"
# }''')
# print(type(req))
# print(type(req.request))


__all__ = tuple(map(lambda cls: cls.__name__, reversed((
    RequestMetaInterfaces,
    Meta,
    RequestField,
    User,
    Application,
    Session,
    YaSessionState,
    YaUserState,
    YaApplicationState,
    YaState,
    AliceUserRequest
))))
